import React from 'react';
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

import styles from './styles.module.scss';

export const Sidebar: React.FC<{}> = () => {
  return (
    <div className={styles.container}>
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
      <SidebarRow icon={signoutIcon} text="Log out" />
    </div>
  );
};
