import {ClubsCarousel} from '../../components/ClubsCarousel';
import {EventsCarousel} from '../../components/EventsCarousel';
import {Layout} from '../../components/Layout/Layout';
import {NewsCarousel} from '../../components/NewsCarousel';
import './styles.module.scss';

export const Home: React.FC = () => {
  return (
    <Layout>
      <NewsCarousel />
      <ClubsCarousel />
      <EventsCarousel />
    </Layout>
  );
};
