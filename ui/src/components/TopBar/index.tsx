import styles from './styles.module.scss';
import {logo} from '../../assets';
import {useContext} from 'react';
import {DarkModeContext} from '../Contexts/DarkModeContext';
interface TopBarProps {
  setSidebarVisibility: (isSidebarOpenOnMobile: boolean) => void;
}

export const TopBar: React.FC<TopBarProps> = ({setSidebarVisibility}) => {
  const menuClickHandler = () => {
    setSidebarVisibility(true);
  };

  const {darkMode, toggleDarkMode} = useContext(DarkModeContext);

  return (
    <div className={styles.container}>
      <button
        className={styles.btn}
        data-testid="enabledarkmode"
        onClick={() => toggleDarkMode()}
      >
        {darkMode ? 'Dark Mode' : 'Light Mode'}
      </button>
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
