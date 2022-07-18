import useSWR from 'swr';
import {SERVER_URL} from '../globals/constants';

const fetcher = async (resource: string) => {
  const res = await fetch(SERVER_URL + resource, {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${sessionStorage.getItem('token')!}`,
    },
  });
  if (res.status !== 200) {
    throw new Error(res.status.toString());
  }
  return res.json();
};

export const useAuthFetch = (resourse: string) => {
  return useSWR(resourse, fetcher, {refreshInterval: 10000});
};
