import {loginArrow, logo} from '../../assets';
import styles from './styles.module.css';

export const Login: React.FC = () => {
  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <img className={styles.logo} src={logo} alt="logo" />
        <div className={styles.heading}>Gymkhana</div>
        <button className={styles.btn}>
          SIGN IN <img src={loginArrow} alt="arrow" />
        </button>
        <div className={styles.footer}>IIITDM Jabalpur</div>
      </div>
    </div>
  );
};
