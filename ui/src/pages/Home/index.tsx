import {useState} from 'react';
import {ClubsCarousel} from '../../components/ClubsCarousel';
import {EventsCarousel} from '../../components/EventsCarousel';
import {NewsCarousel} from '../../components/NewsCarousel';
import {Sidebar} from '../../components/Sidebar/Sidebar';
import {TopBar} from '../../components/TopBar';
import styles from './styles.module.scss';

export const Home: React.FC = () => {
  const [isSidebarOpenOnMobile, setIsSidebarOpenOnMobile] = useState(false);
  return (
    <div className={styles.container}>
      <Sidebar
        isSidebarOpenOnMobile={isSidebarOpenOnMobile}
        setIsSidebarOpenOnMobile={setIsSidebarOpenOnMobile}
      />
      <div
        className={`${styles.mainContent} ${
          isSidebarOpenOnMobile ? styles.mainContentBlur : ''
        }`}
      >
        <TopBar
          isSidebarOpenOnMobile={isSidebarOpenOnMobile}
          setIsSidebarOpenOnMobile={setIsSidebarOpenOnMobile}
        />
        <NewsCarousel />
        <ClubsCarousel />
        <EventsCarousel />
      </div>
    </div>
  );
};
