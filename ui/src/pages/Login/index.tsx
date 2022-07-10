import {Navigate, useSearchParams} from 'react-router-dom';
import {toast, ToastContainer} from 'react-toastify';
import {openGoogleOAuthPage} from '../../api/googleOauth';
import {loginArrow, logo} from '../../assets';
import {isTokenValid} from '../../utils/token';
import styles from './styles.module.scss';
import {useEffect} from 'react';

export const Login: React.FC = () => {
  const [searchParams] = useSearchParams();
  let error = searchParams.get('error');
  useEffect(() => {
    if (error) {
      toast(error);
      error = '';
    }
  }, []);

  if (isTokenValid()) {
    return <Navigate to="/" replace />;
  }
  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <img className={styles.logo} src={logo} alt="logo" />
        <div className={styles.heading}>Gymkhana</div>
        <button
          className={styles.btn}
          data-testid="signin"
          onClick={openGoogleOAuthPage}
        >
          SIGN IN <img src={loginArrow} alt="arrow" />
        </button>
        <div className={styles.footer}>IIITDM Jabalpur</div>
      </div>
      <ToastContainer />
    </div>
  );
};
