import styles from './styles.module.scss';
import Carousel from 'react-multi-carousel';
import 'react-multi-carousel/lib/styles.css';
import {dummyNewsImg} from '../../assets';
import {HeadingDropdown} from '../HeadingDropdown';
import {useState} from 'react';
import {
  EVENT_OPTIONS,
  RESPONSIVE_BREAKPOINTS_CAROUSEL,
} from '../../globals/constants';

const data = [
  {
    name: 'Aperta Fons',
    club: 'TPC',
    imgUrl: dummyNewsImg,
    startTime: new Date(2020, 0),
    endTime: new Date(2020, 0),
  },
  {
    name: 'Aperta Fons',
    club: 'TPC',
    imgUrl: dummyNewsImg,
    startTime: new Date(2020, 0),
    endTime: new Date(2024, 0),
  },
  {
    name: 'Aperta Fons',
    club: 'TPC',
    imgUrl: dummyNewsImg,
    startTime: new Date(2023, 0),
    endTime: new Date(2024, 0),
  },
];

export const EventsCarousel: React.FC = () => {
  const [selectedOption, setSelectedOption] = useState(EVENT_OPTIONS[0]);
  const curDate = new Date(Date.now());
  return (
    <div className={styles.container}>
      <HeadingDropdown
        options={EVENT_OPTIONS}
        selectedOption={selectedOption}
        setSelectedOption={setSelectedOption}
      />
      <Carousel
        responsive={RESPONSIVE_BREAKPOINTS_CAROUSEL}
        className={styles.carousel}
      >
        {data.map(
          (event, i) =>
            ((selectedOption.value === 'upcoming' &&
              event.startTime > curDate) ||
              (selectedOption.value === 'past' && event.endTime < curDate) ||
              (selectedOption.value === 'ongoing' &&
                event.startTime <= curDate &&
                event.endTime >= curDate)) && (
              <div key={i} className={styles.card}>
                <img src={event.imgUrl} alt="event" />
                <div>
                  <div className={styles.name}>{event.name}</div>
                  <div className={styles.club}>{event.club}</div>
                </div>
              </div>
            )
        )}
      </Carousel>
    </div>
  );
};
