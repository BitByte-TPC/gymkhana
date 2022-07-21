import {createMemoryHistory} from 'history';
import {createRoot, Root} from 'react-dom/client';
import {act} from 'react-dom/test-utils';
import {Router} from 'react-router-dom';
import {ProtectedRoute} from './ProtectedRoute';

global.fetch = jest.fn();

let container: Element | null = null;
let root: Root | null = null;

jest.mock('./globals/constants', () => jest.fn());

jest.mock('./assets', () => jest.fn());

describe('<ProtectedRoute />', () => {
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
  it('should not redirect to /login if token is valid', () => {
    window.sessionStorage.setItem('token', 'some-token');
    const history = createMemoryHistory();
    act(() => {
      root!.render(
        <Router location={history.location} navigator={history}>
          <ProtectedRoute>
            <div>homepage</div>
          </ProtectedRoute>
        </Router>
      );
    });

    expect(history.location.pathname).not.toBe('/login');
  });
  it('should redirect to /login if token is not valid', () => {
    const history = createMemoryHistory();
    act(() => {
      root!.render(
        <Router location={history.location} navigator={history}>
          <ProtectedRoute>
            <div>homepage</div>
          </ProtectedRoute>
        </Router>
      );
    });

    expect(history.location.pathname).toBe('/login');
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
