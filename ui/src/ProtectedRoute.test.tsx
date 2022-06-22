// eslint-disable-next-line node/no-unpublished-import
import {render} from '@testing-library/react';
import {BrowserRouter} from 'react-router-dom';
import {Router} from './Routes';

const localStorageMock = (() => {
  let store: {[key: string]: string} = {};
  return {
    getItem(key: string) {
      return store[key] || null;
    },
    setItem(key: string, value: string) {
      store[key] = value.toString();
    },
    removeItem(key: string) {
      delete store[key];
    },
    clear() {
      store = {};
    },
  };
})();

Object.defineProperty(window, 'sessionStorage', {
  value: localStorageMock,
});

jest.mock('./assets/index.ts', () => jest.fn());
jest.mock('./globals/constants.ts', () => jest.fn());

describe('Home', () => {
  beforeEach(() => {
    window.sessionStorage.clear();
    jest.restoreAllMocks();
  });

  it('should redirect to login', () => {
    const {getByTestId} = render(
      <BrowserRouter>
        <Router />
      </BrowserRouter>
    );
    const component = getByTestId('signin');
    expect(component).toBeDefined();
  });

  it('should not redirect to login', () => {
    window.sessionStorage.setItem('token', 'val');
    const {getByTestId} = render(
      <BrowserRouter>
        <Router />
      </BrowserRouter>
    );
    let component;
    try {
      component = getByTestId('signin');
      // eslint-disable-next-line no-empty
    } catch (err) {}
    expect(component).toBeUndefined();
  });
});
