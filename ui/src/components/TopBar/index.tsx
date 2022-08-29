import styles from './styles.module.scss';
import {logo, moonIcon, sunIcon} from '../../assets';
import {useEffect, useState} from 'react';
interface TopBarProps {
  setSidebarVisibility: (isSidebarOpenOnMobile: boolean) => void;
}
const LIGHT_MODE_VALUE = 'light_mode';
const DARK_MODE_VALUE = 'dark_mode';
const WEBSITE_THEME = 'website_theme';

export const TopBar: React.FC<TopBarProps> = ({setSidebarVisibility}) => {
  const menuClickHandler = () => {
    setSidebarVisibility(true);
  };

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
    <div className={styles.container}>
      <img
        src={currentTheme === LIGHT_MODE_VALUE ? moonIcon : sunIcon}
        className={styles.themeIcon}
        onClick={toggleMode}
      />
      <div className={styles.logoContainer} onClick={menuClickHandler}>
        <img className={styles.logo} src={logo} alt="logo" />
      </div>
      <div className={styles.profileInfoContainer}>
        <img
          src="https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_960_720.png"
          alt="profile-img"
        />
        <div className={styles.profileName}>Name</div>
      </div>
    </div>
  );
};
