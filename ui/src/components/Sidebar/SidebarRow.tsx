import React from 'react';
import styles from './styles.module.scss';

interface Props {
  icon: string;
  text: string;
  onClick?: () => void;
  //   isActive: boolean;
}

export const SidebarRow: React.FC<Props> = props => {
  return (
    <div
      className={styles.container_row}
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
