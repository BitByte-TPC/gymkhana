import styles from './styles.module.scss';
import Carousel from 'react-multi-carousel';
import 'react-multi-carousel/lib/styles.css';
import {useAuthFetch} from '../../api/useAuthFetch';
import {useEffect, useState} from 'react';
import {useLogout} from '../../hooks/useLogout';
import {HeadingDropdown} from '../HeadingDropdown';
import {RESPONSIVE_BREAKPOINTS_CAROUSEL} from '../../globals/constants';

export const CLUB_OPTIONS = [
  {value: 'all', label: 'Clubs'},
  {value: 'S&T', label: 'Technical Clubs'},
  {value: 'Cultural', label: 'Cultural Clubs'},
  {value: 'Sports', label: 'Sports Clubs'},
];

Object.freeze(CLUB_OPTIONS);

interface ClubsCarouselData {
  name: string;
  logo: string;
  category: string;
}

export const ClubsCarousel: React.FC = () => {
  const [selectedOption, setSelectedOption] = useState(CLUB_OPTIONS[0]);
  const {data, error} = useAuthFetch('/clubs');
  const logout = useLogout();
  useEffect(() => {
    if (error) {
      logout();
    }
  }, [error]);

  return (
    <div className={styles.container}>
      <HeadingDropdown
        options={CLUB_OPTIONS}
        selectedOption={selectedOption}
        setSelectedOption={setSelectedOption}
      />
      <Carousel
        responsive={RESPONSIVE_BREAKPOINTS_CAROUSEL}
        className={styles.carousel}
      >
        {data ? (
          data.map(
            (club: ClubsCarouselData, index: number) =>
              (selectedOption.value === 'all' ||
                selectedOption.value === club.category) && (
                <div key={index} className={styles.card}>
                  <img src={club.logo} alt="club" />
                  <div>
                    <div className={styles.name}>{club.name}</div>
                    <div className={styles.category}>{club.category}</div>
                  </div>
                </div>
              )
          )
        ) : (
          <div>Loading...</div>
        )}
      </Carousel>
    </div>
  );
};
