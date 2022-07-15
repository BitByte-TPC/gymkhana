import styles from './styles.module.scss';
import Carousel from 'react-multi-carousel';
import 'react-multi-carousel/lib/styles.css';
import {useEffect, useState} from 'react';
import {useNavigate} from 'react-router-dom';
import {SERVER_URL} from '../../globals/constants';

export const ClubsCarousel: React.FC = () => {
  interface ClubsCarouselData {
    name: string;
    logo: string;
    category: string;
  }
  const [data, setData] = useState<ClubsCarouselData[]>([]);
  const token = window.sessionStorage.getItem('token');
  const CLUBS_API_URL = SERVER_URL + '/clubs';
  const navigate = useNavigate();
  const invalidTokenHandler = () => {
    const errQuery = new URLSearchParams({
      error: 'Please try again later!',
    });

    window.sessionStorage.removeItem('token');
    navigate('/login?' + errQuery.toString());
  };
  const getClubs = async () => {
    const response = await fetch(CLUBS_API_URL, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    if (response) {
      if (response.status === 200) {
        const data = await response.json();
        setData(data);
      } else if (response.status === 403) {
        token && invalidTokenHandler();
      }
    }
  };
  useEffect(() => {
    getClubs();
  }, []);

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
        {data.map((club, index) => (
          <div key={index} className={styles.card}>
            <img src={club.logo} alt="club" />
            <div>
              <div className={styles.name}>{club.name}</div>
              <div className={styles.category}>{club.category}</div>
            </div>
          </div>
        ))}
      </Carousel>
    </div>
  );
};
