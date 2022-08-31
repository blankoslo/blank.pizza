import { QueryObserverResult, InfiniteQueryObserverResult, useInfiniteQuery, useQuery } from '@tanstack/react-query';
import { ApiUsers, ApiUsersInfinite, useUserService, usersDefaultQueryKey, ApiUsersParams } from '../api/UserService';

export const useUsers = (params?: ApiUsersParams): QueryObserverResult<ApiUsers> => {
    const { getUsers } = useUserService();

    return useQuery<ApiUsers>({
        queryKey: [usersDefaultQueryKey],
        queryFn: () => getUsers(params),
    });
};

export const useInfiniteUsers = (
    params?: Omit<ApiUsersParams, 'page'>,
): InfiniteQueryObserverResult<ApiUsersInfinite> => {
    const { getUsersInfinite } = useUserService();

    return useInfiniteQuery<ApiUsersInfinite>({
        queryKey: [usersDefaultQueryKey, params],
        queryFn: ({ pageParam = 1 }) => getUsersInfinite({ ...params, page: pageParam }),
        getNextPageParam: (lastGroup) => lastGroup.nextPage,
        getPreviousPageParam: (firstGroup) => firstGroup.prevPage,
    });
};
