import {Carousel} from 'react-responsive-carousel';
import 'react-responsive-carousel/lib/styles/carousel.min.css';
import {dummyNewsImg, loginArrow} from '../../assets';
import styles from './styles.module.scss';

const data = [
  {
    title: 'Registrations Open',
    clubName: 'The Programming Club',
    description:
      'Bayerische Motoren Werke AG, commonly referred to as BMW is a German multinational corporate manufactu',
    imgUrl: dummyNewsImg,
  },
  {
    title: 'Registrations Open',
    clubName: 'The Programming Club',
    description:
      'Bayerische Motoren Werke AG, commonly referred to as BMW is a German multinational corporate manufactu',
    imgUrl: dummyNewsImg,
  },
  {
    title: 'Registrations Open',
    clubName: 'The Programming Club',
    description:
      'Bayerische Motoren Werke AG, commonly referred to as BMW is a German multinational corporate manufactu',
    imgUrl: dummyNewsImg,
  },
];

export const NewsCarousel: React.FC = () => {
  return (
    <Carousel
      autoPlay
      emulateTouch
      showArrows={false}
      showStatus={false}
      showThumbs={false}
    >
      {data.map((news, i) => (
        <div key={i} className={styles.cardContainer}>
          <div className={styles.leftContainer}>
            <div className={styles.info}>
              <div className={styles.heading}>{news.title}</div>
              <div className={styles.subHeading}>{news.clubName}</div>
              <p className={styles.description}>{news.description}</p>
              <button className={styles.showMore}>
                Show more <img src={loginArrow} alt="arrow" />
              </button>
            </div>
          </div>
          <img className={styles.rightImg} src={news.imgUrl} alt="news" />
        </div>
      ))}
    </Carousel>
  );
};
