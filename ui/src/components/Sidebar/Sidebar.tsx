import React from 'react';
import {
  logo,
  googleChromeLogo,
  wallClockLogo,
  calenderLogo,
  desktopTower,
  theatreLogo,
  sportsLogo,
  settingsLogo,
  signoutLogo,
} from '../../assets';

import styles from './styles.module.css';

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

      <div className={styles.container_row}>
        <div className={styles.row_content}>
          <div className={styles.icondesign}>
            <img src={googleChromeLogo} alt="logo" />
          </div>
          <div className={styles.icontext} style={{color: 'black'}}>
            Browse
          </div>
        </div>
      </div>

      <div className={styles.container_row}>
        <div className={styles.row_content}>
          <div className={styles.icondesign}>
            <img src={wallClockLogo} alt="logo" />
          </div>
          <div className={styles.icontext}>Recents</div>
        </div>
      </div>

      <div className={styles.container_row}>
        <div className={styles.row_content}>
          <div className={styles.icondesign}>
            <img src={calenderLogo} alt="logo" />
          </div>
          <div className={styles.icontext}>Upcoming</div>
        </div>
      </div>

      <div>
        <div className={styles.container_text_row}>Clubs</div>
      </div>

      <div className={styles.container_row}>
        <div className={styles.row_content}>
          <div className={styles.icondesign}>
            <img src={desktopTower} alt="logo" />
          </div>
          <div className={styles.icontext}>Technical</div>
        </div>
      </div>

      <div className={styles.container_row}>
        <div className={styles.row_content}>
          <div className={styles.icondesign}>
            <img src={theatreLogo} alt="logo" />
          </div>
          <div className={styles.icontext}>Cultural</div>
        </div>
      </div>

      <div className={styles.container_row}>
        <div className={styles.row_content}>
          <div className={styles.icondesign}>
            <img src={sportsLogo} alt="logo" />
          </div>
          <div className={styles.icontext}>Sports</div>
        </div>
      </div>

      <div>
        <div className={styles.container_text_row}>General</div>
      </div>

      <div className={styles.container_row}>
        <div className={styles.row_content}>
          <div className={styles.icondesign}>
            <img src={settingsLogo} alt="logo" />
          </div>
          <div className={styles.icontext}>Settings</div>
        </div>
      </div>

      <div className={styles.container_row}>
        <div className={styles.row_content}>
          <div className={styles.icondesign}>
            <img src={signoutLogo} alt="logo" />
          </div>
          <div className={styles.icontext}>Log out</div>
        </div>
      </div>
    </div>
  );
};
