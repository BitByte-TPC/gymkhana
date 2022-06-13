export const setToken = (token: string) => {
  sessionStorage.setItem('token', token);
};

export const isTokenValid = (): boolean => {
  return !!sessionStorage.getItem('token');
};
