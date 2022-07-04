import styles from './styles.module.css';
import Carousel from 'react-multi-carousel';
import 'react-multi-carousel/lib/styles.css';
import {dummyClubLogo} from '../../assets';

const data = [
  {
    name: 'TPC',
    category: 'Technical',
    logoUrl: dummyClubLogo,
  },
  {
    name: 'Jazbaat',
    category: 'Cultural',
    logoUrl: dummyClubLogo,
  },
  {
    name: 'Basketball',
    category: 'Sports',
    logoUrl: dummyClubLogo,
  },
  {
    name: 'Saaz',
    category: 'Cultural',
    logoUrl: dummyClubLogo,
  },
  {
    name: 'Badminton',
    category: 'Sports',
    logoUrl: dummyClubLogo,
  },
];

export const ClubsCarousel: React.FC = () => {
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
        {data.map((club, i) => (
          <div key={i} className={styles.card}>
            <img src={club.logoUrl} alt="club" />
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
