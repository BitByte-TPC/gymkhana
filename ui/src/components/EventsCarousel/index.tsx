import styles from './styles.module.scss';
import Carousel from 'react-multi-carousel';
import 'react-multi-carousel/lib/styles.css';
import {dummyNewsImg} from '../../assets';
import {HeadingDropdown} from '../HeadingDropdown';
import {useState} from 'react';
import {RESPONSIVE_BREAKPOINTS_CAROUSEL} from '../../globals/constants';

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

const EVENT_OPTIONS: {
  value: 'upcoming' | 'past' | 'ongoing';
  label: string;
}[] = [
  {value: 'upcoming', label: 'Upcoming'},
  {value: 'past', label: 'Past'},
  {value: 'ongoing', label: 'Ongoing'},
];
Object.freeze(EVENT_OPTIONS);

interface EventsCarouselData {
  name: string;
  club: string;
  imgUrl: string;
  startTime: Date;
  endTime: Date;
}

export const shouldRenderEvent = (
  eventType: 'upcoming' | 'past' | 'ongoing',
  event: EventsCarouselData
) => {
  const curDate = new Date(Date.now());
  return (
    (eventType === 'upcoming' && event.startTime > curDate) ||
    (eventType === 'past' && event.endTime < curDate) ||
    (eventType === 'ongoing' &&
      event.startTime <= curDate &&
      event.endTime >= curDate)
  );
};

export const EventsCarousel: React.FC = () => {
  const [selectedOption, setSelectedOption] = useState(EVENT_OPTIONS[0]);
  return (
    <div className={styles.container}>
      <HeadingDropdown
        options={EVENT_OPTIONS}
        selectedOption={selectedOption}
        // eslint-disable-next-line @typescript-eslint/ban-ts-comment
        // @ts-ignore
        setSelectedOption={setSelectedOption}
      />
      <Carousel
        responsive={RESPONSIVE_BREAKPOINTS_CAROUSEL}
        className={styles.carousel}
      >
        {data.map(
          (event, i) =>
            shouldRenderEvent(selectedOption.value, event) && (
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
