import styles from './styles.module.scss';
import Carousel from 'react-multi-carousel';
import 'react-multi-carousel/lib/styles.css';
import {useAuthFetch} from '../../api/useAuthFetch';
import {useEffect} from 'react';
import {useLogout} from '../../hooks/useLogout';

interface ClubsCarouselData {
  name: string;
  logo: string;
  category: string;
}

export const ClubsCarousel: React.FC = () => {
  const {data, error} = useAuthFetch('/clubs');
  const logout = useLogout();
  useEffect(() => {
    if (error) {
      logout();
    }
  }, [error]);

  const responsive = {
    desktop: {
      breakpoint: {max: 5000, min: 1024},
      items: 4,
    },
    tablet: {
      breakpoint: {max: 1024, min: 800},
      items: 2,
    },
    mobile: {
      breakpoint: {max: 800, min: 0},
      items: 1,
    },
  };
  return (
    <div className={styles.container}>
      <div className={styles.heading}>Clubs</div>
      <Carousel responsive={responsive} className={styles.carousel}>
        {data ? (
          data.map((club: ClubsCarouselData, index: number) => (
            <div key={index} className={styles.card}>
              <img src={club.logo} alt="club" />
              <div>
                <div className={styles.name}>{club.name}</div>
                <div className={styles.category}>{club.category}</div>
              </div>
            </div>
          ))
        ) : (
          <div>Loading...</div>
        )}
      </Carousel>
    </div>
  );
};
