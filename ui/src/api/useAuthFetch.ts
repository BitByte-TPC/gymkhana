import useSWR, {SWRResponse} from 'swr';
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

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}
interface DataResponse<T> extends SWRResponse {
  data?: T;
}

export const useAuthFetch = <T>(resourse: string): DataResponse<T> => {
  return useSWR(resourse, fetcher);
};
