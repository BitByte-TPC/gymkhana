import {moonIcon, sunIcon} from '../../assets';
import {useEffect, useState} from 'react';
import styles from './styles.module.scss';

const LIGHT_MODE_VALUE = 'light_mode';
const DARK_MODE_VALUE = 'dark_mode';
const WEBSITE_THEME = 'website_theme';

export const Theme: any = () => {
  const [currentTheme, setCurrentTheme] = useState(LIGHT_MODE_VALUE);

  const toggleMode = () => {
    const darkTheme = document.body.classList.toggle(DARK_MODE_VALUE);
    if (darkTheme) {
      localStorage.setItem(WEBSITE_THEME, DARK_MODE_VALUE);
      setCurrentTheme(DARK_MODE_VALUE);
    } else {
      localStorage.setItem(WEBSITE_THEME, LIGHT_MODE_VALUE);
      setCurrentTheme(LIGHT_MODE_VALUE);
    }
  };

  const retrieveTheme = () => {
    const theme = localStorage.getItem(WEBSITE_THEME) || LIGHT_MODE_VALUE;
    setCurrentTheme(theme);
    document.body.classList.add(theme);
  };

  useEffect(() => {
    retrieveTheme();
  }, []);

  return (
    <div>
      <img
        src={currentTheme === LIGHT_MODE_VALUE ? moonIcon : sunIcon}
        className={styles.themeIcon}
        onClick={toggleMode}
      />
    </div>
  );
};
