import {GOOGLE_CLIENT_ID, REDIRECT_URL, SERVER_URL} from '../globals/constants';
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
    response_type: 'code',
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
 * @param authorizationCode - Authorization code returned by google
 * @param redirectToHome - callback function to redirect to home
 */
export const convertAccessToken = async (
  authorizationCode: string,
  redirectToHome: () => void,
  failRedirect: () => void
) => {
  try {
    const res = await fetch(SERVER_URL + '/auth/token/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        authorization_code: authorizationCode,
      }),
    });
    const data = await res.json();
    if (data.token) {
      setToken(data.token);
      redirectToHome();
    } else {
      throw new Error('API error');
    }
  } catch (err) {
    failRedirect();
  }
};
