import {ClubsCarousel} from '../../components/ClubsCarousel';
import {EventsCarousel} from '../../components/EventsCarousel';
import {Layout} from '../../components/Layout/Layout';
import {NewsCarousel} from '../../components/NewsCarousel';

export const Home: React.FC = () => {
  return (
    <Layout>
      <NewsCarousel />
      <ClubsCarousel />
      <EventsCarousel />
    </Layout>
  );
};
