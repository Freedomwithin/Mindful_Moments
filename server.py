#!/usr/bin/env python3
import os
import sys
import json
import re
import subprocess
import urllib.request
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("PORT", 7860))
DOWNLOAD_DIR = "/tmp/music"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def search_youtube_scrape(query, max_results=10):
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    })
    try:
        html = urllib.request.urlopen(req, timeout=12).read().decode('utf-8', errors='ignore')
        match = re.search(r'var ytInitialData = ({.*?});</script>', html)
        if not match:
            match = re.search(r'window\["ytInitialData"\] = ({.*?});', html)
        if not match:
            return []

        data = json.loads(match.group(1))
        # Navigate search contents
        primary = data.get('contents', {}).get('twoColumnSearchResultsRenderer', {}).get('primaryContents', {}).get('sectionListRenderer', {}).get('contents', [])
        results = []
        for section in primary:
            items = section.get('itemSectionRenderer', {}).get('contents', [])
            for it in items:
                vr = it.get('videoRenderer')
                if vr:
                    vid = vr.get('videoId')
                    title = vr.get('title', {}).get('runs', [{}])[0].get('text', 'Unknown')
                    uploader = vr.get('ownerText', {}).get('runs', [{}])[0].get('text', 'YouTube')
                    length_text = vr.get('lengthText', {}).get('simpleText', '')
                    dur_sec = 0
                    if length_text:
                        parts = length_text.split(':')
                        try:
                            if len(parts) == 2:
                                dur_sec = int(parts[0]) * 60 + int(parts[1])
                            elif len(parts) == 3:
                                dur_sec = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
                        except Exception:
                            dur_sec = 0
                    results.append({
                        "id": vid,
                        "title": title,
                        "uploader": uploader,
                        "duration": dur_sec,
                        "url": f"https://www.youtube.com/watch?v={vid}"
                    })
                    if len(results) >= max_results:
                        break
            if len(results) >= max_results:
                break
        return results
    except Exception as e:
        print(f"Scrape search exception: {e}")
        return []

def search_youtube_ytdlp(query, max_results=5):
    try:
        cmd = [
            "yt-dlp",
            "--extractor-args", "youtube:player_client=android",
            f"ytsearch{max_results}:{query}",
            "--dump-single-json",
            "--flat-playlist",
            "--no-warnings",
            "--default-search", "ytsearch"
        ]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=20)
        if proc.returncode != 0:
            return []
        data = json.loads(proc.stdout)
        entries = data.get('entries', [])
        results = []
        for entry in entries:
            if entry:
                results.append({
                    "id": entry.get('id'),
                    "title": entry.get('title', 'Unknown'),
                    "uploader": entry.get('uploader') or entry.get('channel', 'Unknown'),
                    "duration": entry.get('duration', 0),
                    "url": f"https://www.youtube.com/watch?v={entry.get('id')}"
                })
        return results
    except Exception as e:
        print(f"yt-dlp search exception: {e}")
        return []

class CloudMediaHandler(BaseHTTPRequestHandler):
    def _send_json(self, status, payload):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode('utf-8'))

    def do_OPTIONS(self):
        self._send_json(200, {"status": "ok"})

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if parsed.path == '/' or parsed.path == '/health':
            self._send_json(200, {"status": "healthy", "service": "Maya Sovereign Cloud Music Bridge v1.1"})
            return

        elif parsed.path == '/search':
            query = params.get('q', [''])[0].strip()
            if not query:
                self._send_json(400, {"error": "Missing query 'q'"})
                return

            results = search_youtube_scrape(query, max_results=10)
            if not results:
                results = search_youtube_ytdlp(query, max_results=5)

            if results:
                self._send_json(200, {"query": query, "results": results})
            else:
                self._send_json(200, {"query": query, "results": []})

        elif parsed.path.startswith('/file/'):
            filename = os.path.basename(parsed.path)
            file_path = os.path.join(DOWNLOAD_DIR, filename)
            if os.path.exists(file_path):
                self.send_response(200)
                self.send_header('Content-Type', 'audio/mpeg')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
                self.send_header('Content-Length', str(os.path.getsize(file_path)))
                self.end_headers()
                with open(file_path, 'rb') as f:
                    while chunk := f.read(65536):
                        self.wfile.write(chunk)
            else:
                self._send_json(404, {"error": "File not found or expired"})
        else:
            self._send_json(404, {"error": "Not found"})

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path in ['/convert', '/download']:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                payload = json.loads(body)
            except Exception:
                payload = {}

            video_id = payload.get('id') or payload.get('url')
            if not video_id:
                self._send_json(400, {"error": "Missing 'id' or 'url'"})
                return

            try:
                url = video_id if video_id.startswith("http") else f"https://www.youtube.com/watch?v={video_id}"
                out_template = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
                cmd = [
                    "yt-dlp",
                    "--extractor-args", "youtube:player_client=android,ios,web",
                    "--no-check-certificates",
                    "--no-warnings",
                    "-x",
                    "--audio-format", "mp3",
                    "--audio-quality", "320K",
                    "--embed-thumbnail",
                    "--add-metadata",
                    "-o", out_template,
                    url
                ]
                proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=180)
                
                mp3_files = [os.path.join(DOWNLOAD_DIR, f) for f in os.listdir(DOWNLOAD_DIR) if f.endswith(".mp3")]
                if not mp3_files:
                    self._send_json(500, {
                        "error": "Conversion produced no file",
                        "stderr": proc.stderr,
                        "stdout": proc.stdout
                    })
                    return
                
                newest = max(mp3_files, key=os.path.getctime)
                filename = os.path.basename(newest)
                safe_name = re.sub(r'[^\w\s\-\.\(\)]', '', filename).strip()
                if not safe_name.endswith('.mp3'): safe_name += '.mp3'
                safe_path = os.path.join(DOWNLOAD_DIR, safe_name)
                if safe_path != newest:
                    os.rename(newest, safe_path)

                download_url = f"/file/{urllib.parse.quote(safe_name)}"
                self._send_json(200, {
                    "status": "ready",
                    "filename": safe_name,
                    "download_url": download_url
                })
            except Exception as e:
                self._send_json(500, {"error": str(e)})
        else:
            self._send_json(404, {"error": "Not found"})

def run():
    server = HTTPServer(('0.0.0.0', PORT), CloudMediaHandler)
    print(f"Cloud Media Bridge listening on port {PORT}...")
    server.serve_forever()

if __name__ == '__main__':
    run()
