/* eslint-disable node/no-unsupported-features/node-builtins */
import {useEffect} from 'react';
import {convertAccessToken} from '../../api/googleOauth';
import {useNavigate} from 'react-router-dom';

export const LoginRedirect: React.FC = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const errQuery = new URLSearchParams({error: 'Please try again later!'});
    const code = new URLSearchParams(window.location.search).get('code');

    if (!code) {
      return navigate('/');
    } else {
      convertAccessToken(
        code,
        () => navigate('/'),
        () => navigate('/login?' + errQuery.toString())
      );
    }
  }, []);
  return <div>Loading...</div>;
};
