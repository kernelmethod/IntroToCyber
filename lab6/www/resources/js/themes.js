// Get the selected theme from the user's cookies
function getConfiguredTheme() {
    return document.cookie
        .split('; ')
        .find((cookie) => cookie.startsWith('TICKTOCK_WHOST_THEME'))
        ?.split('=')[1];
}

// Set the theme in the user's cookies
function setConfiguredTheme(themeName, themeMap) {
    document.cookie = `TICKTOCK_WHOST_THEME=${themeName}; SameSite=Strict;`;
}

// Set the page theme.
function useTheme(themeName, defaultThemeName, themeMap) {
    let el = document.getElementById('pageTheme');
    let theme = themeMap.get(themeName);

    if (theme === undefined) {
        console.error(`Unknown theme ${themeName}. Defaulting to ${defaultThemeName}`);
        theme = themeMap.get(defaultThemeName);
    }
    el.href = theme;
}

export { getConfiguredTheme, setConfiguredTheme, useTheme };
