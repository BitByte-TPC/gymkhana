import {shouldRenderEvent, stringToDate} from '.';

const data = [
  {
    name: 'Past event',
    club: 'TPC',
    image_url: '',
    starts_at: '2020-12-12',
    ends_at: '2020-12-12',
  },
  {
    name: 'Ongoing event',
    club: 'TPC',
    image_url: '',
    starts_at: '2020-12-12',
    ends_at: '2024-12-12',
  },
  {
    name: 'Upcoming event',
    club: 'TPC',
    image_url: '',
    starts_at: '2023-12-12',
    ends_at: '2024-12-12',
  },
];

jest.mock('../../assets', () => jest.fn());
jest.mock('../../globals/constants', () => jest.fn());

describe('<EventsCarousel/>', () => {
  it('should only render upcoming events', () => {
    const curDate = new Date(Date.now());
    data.forEach(event => {
      const res = shouldRenderEvent('upcoming', event);
      const expectedRes = stringToDate(event.starts_at) > curDate;
      expect(res).toEqual(expectedRes);
    });
  });
  it('should only render past events', () => {
    const curDate = new Date(Date.now());
    data.forEach(event => {
      const res = shouldRenderEvent('past', event);
      const expectedRes = stringToDate(event.ends_at) < curDate;
      expect(res).toEqual(expectedRes);
    });
  });
  it('should only render ongoing events', () => {
    const curDate = new Date(Date.now());
    data.forEach(event => {
      const res = shouldRenderEvent('ongoing', event);
      const expectedRes =
        stringToDate(event.starts_at) <= curDate &&
        stringToDate(event.ends_at) >= curDate;
      expect(res).toEqual(expectedRes);
    });
  });
});
