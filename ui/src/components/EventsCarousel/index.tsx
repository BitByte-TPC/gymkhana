import styles from './styles.module.scss';
import Carousel from 'react-multi-carousel';
import 'react-multi-carousel/lib/styles.css';
import {dummyNewsImg} from '../../assets';

const data = [
  {
    name: 'Aperta Fons',
    club: 'TPC',
    imgUrl: dummyNewsImg,
  },
  {
    name: 'Aperta Fons',
    club: 'TPC',
    imgUrl: dummyNewsImg,
  },
  {
    name: 'Aperta Fons',
    club: 'TPC',
    imgUrl: dummyNewsImg,
  },
  {
    name: 'Aperta Fons',
    club: 'TPC',
    imgUrl: dummyNewsImg,
  },
  {
    name: 'Aperta Fons',
    club: 'TPC',
    imgUrl: dummyNewsImg,
  },
];

export const EventsCarousel: React.FC = () => {
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
      <div className={styles.heading}>Upcoming</div>
      <Carousel responsive={responsive} className={styles.carousel}>
        {data.map((event, i) => (
          <div key={i} className={styles.card}>
            <img src={event.imgUrl} alt="event" />
            <div>
              <div className={styles.name}>{event.name}</div>
              <div className={styles.club}>{event.club}</div>
            </div>
          </div>
        ))}
      </Carousel>
    </div>
  );
};
