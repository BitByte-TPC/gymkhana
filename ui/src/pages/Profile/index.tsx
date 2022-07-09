import {ProfileCard} from '../../components/ProfileCard';
import {Sidebar} from '../../components/Sidebar/Sidebar';
import {TopBar} from '../../components/TopBar';
import styles from './styles.module.css';

export const Profile: React.FC = () => {
  return (
    <div className={styles.container}>
      <div className={styles.NavContainer}>
        <Sidebar />
      </div>
      <div className={styles.mainContent}>
        <TopBar />
        <ProfileCard />
      </div>
    </div>
  );
};
