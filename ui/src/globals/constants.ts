export const SERVER_URL = import.meta.env.VITE_SERVER_URL;
export const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID;
export const REDIRECT_URL = import.meta.env.VITE_REDIRECT_URL;

export const RESPONSIVE_BREAKPOINTS_CAROUSEL = {
  desktop: {
    breakpoint: {max: 5000, min: 1024},
    items: 4,
  },
  tablet: {
    breakpoint: {max: 1024, min: 800},
    items: 2,
  },
  mobile: {
    breakpoint: {max: 800, min: 0},
    items: 1,
  },
};

Object.freeze(RESPONSIVE_BREAKPOINTS_CAROUSEL);
