function setTheme(themeName) {
    localStorage.setItem('theme', themeName);
    document.body.className = themeName;
}

function toggleTheme() {
    if (localStorage.getItem('theme') === 'theme-blue') {
        setTheme('theme-red');
    } else if (localStorage.getItem('theme') === 'theme-red') {
        setTheme('theme-green');
    } else {
        setTheme('theme-blue');
    }
}

// Immediately invoked function to set the theme on initial load
(function () {
    if (localStorage.getItem('theme') === 'theme-red') {
        setTheme('theme-red');
    } else if (localStorage.getItem('theme') === 'theme-green') {
        setTheme('theme-green');
    } else {
        setTheme('theme-blue');
    }
})();