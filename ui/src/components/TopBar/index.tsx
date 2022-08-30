import styles from './styles.module.scss';
import {logo} from '../../assets';
import {ThemeButton} from '../Theme';
interface TopBarProps {
  setSidebarVisibility: (isSidebarOpenOnMobile: boolean) => void;
}

export const TopBar: React.FC<TopBarProps> = ({setSidebarVisibility}) => {
  const menuClickHandler = () => {
    setSidebarVisibility(true);
  };

  return (
    <div className={styles.container}>
      <ThemeButton />
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
