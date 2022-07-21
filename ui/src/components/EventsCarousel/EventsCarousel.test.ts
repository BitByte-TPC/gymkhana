import {shouldRenderEvent} from '.';

const data = [
  {
    name: 'Past event',
    club: 'TPC',
    imgUrl: '',
    startTime: new Date(2020, 0),
    endTime: new Date(2020, 0),
  },
  {
    name: 'Ongoing event',
    club: 'TPC',
    imgUrl: '',
    startTime: new Date(2020, 0),
    endTime: new Date(2024, 0),
  },
  {
    name: 'Upcoming event',
    club: 'TPC',
    imgUrl: '',
    startTime: new Date(2023, 0),
    endTime: new Date(2024, 0),
  },
];

jest.mock('../../assets', () => jest.fn());
jest.mock('../../globals/constants', () => jest.fn());

describe('<EventsCarousel/>', () => {
  it('should only render upcoming events', () => {
    const curDate = new Date(Date.now());
    data.forEach(event => {
      const res = shouldRenderEvent('upcoming', event);
      const expectedRes = event.startTime > curDate;
      expect(res).toEqual(expectedRes);
    });
  });
  it('should only render past events', () => {
    const curDate = new Date(Date.now());
    data.forEach(event => {
      const res = shouldRenderEvent('past', event);
      const expectedRes = event.endTime < curDate;
      expect(res).toEqual(expectedRes);
    });
  });
  it('should only render ongoing events', () => {
    const curDate = new Date(Date.now());
    data.forEach(event => {
      const res = shouldRenderEvent('ongoing', event);
      const expectedRes =
        event.startTime <= curDate && event.endTime >= curDate;
      expect(res).toEqual(expectedRes);
    });
  });
});
