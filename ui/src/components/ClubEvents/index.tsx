import styles from './styles.module.scss';
interface IClubEvents {
  type: 'active' | 'past';
}
const ClubEvents: React.FC<IClubEvents> = ({type}) => {
  const demoData = [
    {
      name: 'HackByte Hackathon',
      logo: 'https://www.iiitdmj.ac.in/webix.iiitdmj.ac.in/tpclogo.png',
      description:
        'Lorem ipsum, dolor sit amet consectetur adipisicing elit. Laudantium consequatur quo modi.',
      startDate: '08-08-2022',
      endDate: '08-10-2022',
    },
    {
      name: 'Newbie 2.0',
      logo: 'https://www.iiitdmj.ac.in/webix.iiitdmj.ac.in/tpclogo.png',
      description:
        'Lorem ipsum, dolor sit amet consectetur adipisicing elit. Laudantium consequatur quo modi.',
      startDate: '08-27-2022',
      endDate: '08-29-2022',
    },
  ];
  const getDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date;
  };
  let events;
  if (type === 'active') {
    events = demoData.filter(event => {
      const endDate = getDate(event.endDate);
      const today = new Date();
      if (endDate > today) {
        return event;
      }
    });
  } else {
    events = demoData.filter(event => {
      const endDate = getDate(event.endDate);
      const today = new Date();
      if (endDate < today) {
        return event;
      }
    });
  }
  return (
    <div className={styles.container}>
      {events.map((event, index) => (
        <div key={index} className={styles.itemContainer}>
          <div className={styles.main}>
            <img src={event.logo} className={styles.logo} />
            <div className={styles.content}>
              <div className={styles.eventInfo}>
                <h3 className={styles.h3}>{event.name}</h3>
                <p className={styles.description}>{event.description}</p>
              </div>
              <div className={styles.buttonContainer}>
                <button className={styles.btn}>View</button>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};
export default ClubEvents;
