FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir yt-dlp

COPY server.py /app/server.py

EXPOSE 7860

CMD ["python", "server.py"]
