import {
  API_CLIENT_ID,
  API_CLIENT_SECRET,
  GOOGLE_CLIENT_ID,
  REDIRECT_URL,
  SERVER_URL,
} from '../globals/constants';
import {setToken} from '../utils/token';

export const openGoogleOAuthPage = () => {
  const scopes = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
  ];
  // eslint-disable-next-line node/no-unsupported-features/node-builtins
  const queryParams = new URLSearchParams({
    scope: scopes.toString().replace(',', ' '),
    include_granted_scopes: 'true',
    response_type: 'token',
    state: 'state_parameter_passthrough_value',
    redirect_uri: REDIRECT_URL,
    client_id: GOOGLE_CLIENT_ID,
  });
  window.location.assign(
    'https://accounts.google.com/o/oauth2/v2/auth?' + queryParams.toString()
  );
};

/**
 * Exchange google's access token for our API's access token.
 * @param googleAccessToken - google's access token
 * @param redirectToHome - callback function to redirect to home
 */
export const convertAccessToken = async (
  googleAccessToken: string,
  redirectToHome: () => void,
  failRedirect: () => void
) => {
  try {
    const res = await fetch(SERVER_URL + '/auth/convert-token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        grant_type: 'convert_token',
        client_id: API_CLIENT_ID,
        client_secret: API_CLIENT_SECRET,
        backend: 'google-oauth2',
        token: googleAccessToken,
      }),
    });
    const data = await res.json();
    if (data.access_token) {
      setToken(data.access_token);
      redirectToHome();
    } else {
      throw new Error('API error');
    }
  } catch (err) {
    failRedirect();
  }
};
