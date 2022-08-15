import React, {useContext} from 'react';
import styles from './styles.module.scss';
import {DarkModeContext} from '../Contexts/DarkModeContext';

interface Props {
  icon: string;
  text: string;
  onClick?: () => void;
  //   isActive: boolean;
}

export const SidebarRow: React.FC<Props> = props => {
  //@ts-ignore
  const {darkMode} = useContext(DarkModeContext);

  return (
    <div
      className={
        darkMode ? styles.container_row : styles.container_row_dark_theme
      }
      onClick={() => props.onClick && props.onClick()}
    >
      <div className={styles.row_content}>
        <div className={styles.icondesign}>
          <img src={props.icon} alt="icon" />
        </div>
        <div className={styles.icontext}>{props.text}</div>
      </div>
    </div>
  );
};
