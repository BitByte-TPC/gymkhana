import styles from './styles.module.scss';
import {logo, moonIcon, sunIcon} from '../../assets';
import {useEffect, useState} from 'react';
interface TopBarProps {
  setSidebarVisibility: (isSidebarOpenOnMobile: boolean) => void;
}

export const TopBar: React.FC<TopBarProps> = ({setSidebarVisibility}) => {
  const menuClickHandler = () => {
    setSidebarVisibility(true);
  };

  const lightModeValue = 'light_mode';
  const DarkModeValue = 'dark_mode';
  const websiteTheme = 'website_theme';

  const [currentTheme, setCurrentTheme] = useState(lightModeValue);

  const toggleMode = () => {
    const darkTheme = document.body.classList.toggle(DarkModeValue);
    if (darkTheme) {
      localStorage.setItem(websiteTheme, DarkModeValue);
      setCurrentTheme(DarkModeValue);
    } else {
      localStorage.setItem(websiteTheme, lightModeValue);
      setCurrentTheme(lightModeValue);
    }
  };

  function retrieveTheme() {
    let theme = localStorage.getItem(websiteTheme) || lightModeValue;
    setCurrentTheme(theme);
    document.body.classList.add(theme);
  }

  useEffect(() => {
    retrieveTheme();
  }, []);

  return (
    <div className={styles.container}>
      <img
        src={currentTheme === lightModeValue ? moonIcon : sunIcon}
        className={styles.themeIcon}
        onClick={() => toggleMode()}
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
