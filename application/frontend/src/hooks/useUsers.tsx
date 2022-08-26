import { QueryObserverResult, InfiniteQueryObserverResult, useInfiniteQuery, useQuery } from '@tanstack/react-query';
import {
    ApiUsers,
    ApiUsersInfinite,
    getUsers,
    getRestaurantsInfinite,
    usersDefaultQueryKey,
    ApiUsersParams,
} from '../api/UserService';

export const useUsers = (params?: ApiUsersParams): QueryObserverResult<ApiUsers> => {
    return useQuery<ApiUsers>({
        queryKey: [usersDefaultQueryKey],
        queryFn: () => getUsers(params),
    });
};

export const useInfiniteUsers = (
    params?: Omit<ApiUsersParams, 'page'>,
): InfiniteQueryObserverResult<ApiUsersInfinite> => {
    return useInfiniteQuery<ApiUsersInfinite>({
        queryKey: [usersDefaultQueryKey, params],
        queryFn: ({ pageParam = 1 }) => getRestaurantsInfinite({ ...params, page: pageParam }),
        getNextPageParam: (lastGroup) => lastGroup.nextPage,
        getPreviousPageParam: (firstGroup) => firstGroup.prevPage,
    });
};
