import { useState, useEffect } from 'react';
import { THEME_CONSTANTS } from '../constants';

const ThemeToggle = () => {
  const [theme, setTheme] = useState<string>(THEME_CONSTANTS.LIGHT_MODE);
  
  useEffect(() => {
    // Get initial theme from localStorage or system preference
    const savedTheme = localStorage.getItem(THEME_CONSTANTS.THEME_KEY);
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme) {
      setTheme(savedTheme);
      document.documentElement.classList.toggle('dark', savedTheme === THEME_CONSTANTS.DARK_MODE);
    } else if (prefersDark) {
      setTheme(THEME_CONSTANTS.DARK_MODE);
      document.documentElement.classList.add('dark');
    }
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === THEME_CONSTANTS.LIGHT_MODE 
      ? THEME_CONSTANTS.DARK_MODE 
      : THEME_CONSTANTS.LIGHT_MODE;
    
    setTheme(newTheme);
    document.documentElement.classList.toggle('dark');
    localStorage.setItem(THEME_CONSTANTS.THEME_KEY, newTheme);
  };

  return (
    <button 
      onClick={toggleTheme}
      className="dark-mode-toggle transition-all duration-300"
      aria-label={`Switch to ${theme === THEME_CONSTANTS.LIGHT_MODE ? 'dark' : 'light'} mode`}
    >
      {theme === THEME_CONSTANTS.LIGHT_MODE ? THEME_CONSTANTS.DARK_ICON : THEME_CONSTANTS.LIGHT_ICON}
    </button>
  );
};

export default ThemeToggle;
