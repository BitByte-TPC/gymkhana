import styles from './styles.module.scss';
import Carousel from 'react-multi-carousel';
import 'react-multi-carousel/lib/styles.css';
import {HeadingDropdown} from '../HeadingDropdown';
import {useEffect, useState} from 'react';
import {RESPONSIVE_BREAKPOINTS_CAROUSEL} from '../../globals/constants';
import {PaginatedResponse, useAuthFetch} from '../../api/useAuthFetch';
import {useLogout} from '../../hooks/useLogout';

export function stringToDate(dateString: string) {
  const year = +dateString.substring(0, 4);
  const month = +dateString.substring(5, 7);
  const day = +dateString.substring(8, 10);
  return new Date(year, month - 1, day);
}

const EVENT_OPTIONS: {
  value: 'upcoming' | 'past' | 'ongoing';
  label: string;
}[] = [
  {value: 'upcoming', label: 'Upcoming'},
  {value: 'past', label: 'Past'},
  {value: 'ongoing', label: 'Ongoing'},
];
Object.freeze(EVENT_OPTIONS);

interface EventsData {
  name: string;
  club: string;
  image_url: string;
  starts_at: string;
  ends_at: string;
}

export const shouldRenderEvent = (
  eventType: 'upcoming' | 'past' | 'ongoing',
  event: EventsData
) => {
  const curDate = new Date();
  const start = stringToDate(event.starts_at);
  const end = stringToDate(event.ends_at);

  return (
    (eventType === 'upcoming' && start > curDate) ||
    (eventType === 'past' && end < curDate) ||
    (eventType === 'ongoing' && start <= curDate && end >= curDate)
  );
};

export const EventsCarousel: React.FC = () => {
  const [selectedOption, setSelectedOption] = useState(EVENT_OPTIONS[0]);
  const {data, error} = useAuthFetch<PaginatedResponse<EventsData>>('/events');
  const eventsData = data ? data.results : [];
  const logout = useLogout();

  useEffect(() => {
    if (error) {
      logout();
    }
  }, [error]);

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
        {eventsData.map(
          (event, index: number) =>
            shouldRenderEvent(selectedOption.value, event) && (
              <div key={index} className={styles.card}>
                <img src={event.image_url} alt="event" />
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
