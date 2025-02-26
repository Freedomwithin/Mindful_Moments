const themes = [
    'theme-blue', 'theme-red', 'theme-green', 'theme-purple', 'theme-orange', 
    'theme-teal', 'theme-pink', 'theme-gray', 'theme-indigo', 'theme-yellow'
];

function setTheme(themeName) {
    localStorage.setItem('theme', themeName);
    document.body.className = themeName;
}

function toggleTheme() {
    const currentTheme = localStorage.getItem('theme') || 'theme-blue';
    const currentIndex = themes.indexOf(currentTheme);
    const nextIndex = (currentIndex + 1) % themes.length;
    setTheme(themes[nextIndex]);
}

// Immediately invoked function to set the theme on initial load
(function () {
    const savedTheme = localStorage.getItem('theme');
    if (themes.includes(savedTheme)) {
        setTheme(savedTheme);
    } else {
        setTheme('theme-blue');
    }
})();
