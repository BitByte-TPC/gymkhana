import {createMemoryHistory} from 'history';
import {createRoot, Root} from 'react-dom/client';
import {act} from 'react-dom/test-utils';
import {Router} from 'react-router-dom';
import {useLogout} from '../../hooks/useLogout';

global.fetch = jest.fn();

let container: Element | null = null;
let root: Root | null = null;

const TestComponent = () => {
  const logout = useLogout();
  return (
    <button onClick={logout} data-testid="logout">
      Logout
    </button>
  );
};

describe('useLogout', () => {
  const {location} = window;

  beforeAll(() => {
    container = document.createElement('div');
    document.body.appendChild(container);
    /* eslint-disable-next-line @typescript-eslint/no-explicit-any */
    delete (window as any).location;
    /* eslint-disable-next-line @typescript-eslint/no-explicit-any */
    window.location = {assign: jest.fn()} as any;
  });

  beforeEach(() => {
    act(() => {
      root = createRoot(container!);
    });
    window.sessionStorage.clear();
  });

  it('should redirect to Login when used', () => {
    window.sessionStorage.setItem('token', 'some-token');
    const history = createMemoryHistory();
    act(() => {
      root!.render(
        <Router location={history.location} navigator={history}>
          <TestComponent />
        </Router>
      );
    });

    const logoutBtn = document.querySelector('[data-testid=logout]');
    act(() => {
      logoutBtn!.dispatchEvent(new MouseEvent('click', {bubbles: true}));
    });

    expect(history.location.pathname).toBe('/login');
    expect(sessionStorage.getItem('token')).toBeNull();
  });

  afterEach(() => {
    act(() => {
      root!.unmount();
    });
    window.sessionStorage.clear();
  });

  afterAll(() => {
    document.body.removeChild(container!);
    window.location = location;
  });
});
