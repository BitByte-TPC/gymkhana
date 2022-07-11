import React, {useEffect, useRef} from 'react';
import {
  logo,
  googleChromeIcon,
  wallClockIcon,
  calenderIcon,
  desktopTowerIcon,
  theatreIcon,
  sportsIcon,
  settingsIcon,
  signoutIcon,
} from '../../assets';
import {SidebarRow} from './SidebarRow';
import {useNavigate} from 'react-router-dom';
import styles from './styles.module.scss';

interface SidebarProps {
  isSidebarOpenOnMobile: boolean;
  setIsSidebarOpenOnMobile: (isSidebarOpenOnMobile: boolean) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  isSidebarOpenOnMobile,
  setIsSidebarOpenOnMobile,
}) => {
  const sidebarRef = useRef<HTMLDivElement>(null);

  const navigate = useNavigate();
  const logoutHandler = () => {
    window.sessionStorage.removeItem('token');
    navigate('/login', {replace: true});
  };
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        sidebarRef.current &&
        !sidebarRef.current.contains(event.target as Node)
      ) {
        setIsSidebarOpenOnMobile(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  });
  return (
    <div
      ref={sidebarRef}
      className={`${styles.container} ${
        isSidebarOpenOnMobile ? styles.openSidebar : ''
      }`}
    >
      <div className={styles.menuContainer}>
        <div className={styles.container_row_heading}>
          <div>
            <img className={styles.icon} src={logo} alt="logo" />
          </div>
          <div className={styles.text}>Gymkhana</div>
        </div>
        <div>
          <div className={styles.container_text_row}>Menu</div>
        </div>

        <SidebarRow icon={googleChromeIcon} text="Browse" />
        <SidebarRow icon={wallClockIcon} text="Recents" />
        <SidebarRow icon={calenderIcon} text="Upcoming" />

        <div>
          <div className={styles.container_text_row}>Clubs</div>
        </div>

        <SidebarRow icon={desktopTowerIcon} text="Technical" />
        <SidebarRow icon={theatreIcon} text="Cultural" />
        <SidebarRow icon={sportsIcon} text="Sports" />

        <div>
          <div className={styles.container_text_row}>General</div>
        </div>

        <SidebarRow icon={settingsIcon} text="Settings" />
        <SidebarRow icon={signoutIcon} text="Log out" onClick={logoutHandler} />
      </div>
    </div>
  );
};
