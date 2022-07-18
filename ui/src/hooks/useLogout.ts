import {useNavigate} from 'react-router-dom';
import {removeToken} from '../utils/token';

export const useLogout = () => {
  const navigate = useNavigate();
  return () => {
    removeToken();
    navigate('/login');
  };
};
