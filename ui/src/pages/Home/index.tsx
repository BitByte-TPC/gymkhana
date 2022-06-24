import {NewsCarousel} from '../../components/NewsCarousel';
import {TopBar} from '../../components/TopBar';
import styles from './styles.module.css';

export const Home: React.FC = () => {
  return (
    <div className={styles.container}>
      <div className={styles.dummyNav}>nav</div>
      <div className={styles.mainContent}>
        <TopBar />
        <NewsCarousel />
      </div>
    </div>
  );
};
