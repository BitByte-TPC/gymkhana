import {NewsCarousel} from '../../components/NewsCarousel';
import {Sidebar} from '../../components/Sidebar/Sidebar';
import {TopBar} from '../../components/TopBar';
import styles from './styles.module.css';

export const Home: React.FC = () => {
  return (
    <div className={styles.container}>
      <div className={styles.dummyNav}>
        <Sidebar />
      </div>
      <div className={styles.mainContent}>
        <TopBar />
        <NewsCarousel />
      </div>
    </div>
  );
};
