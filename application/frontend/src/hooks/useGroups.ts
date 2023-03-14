import { QueryObserverResult, InfiniteQueryObserverResult, useInfiniteQuery, useQuery } from '@tanstack/react-query';
import { ApiGroups, useGroupService, ApiGroupsInfinite, groupsDefaultQueryKey } from '../api/GroupService';
import { Params } from '../api/types';

export const useGroups = (params?: Params): QueryObserverResult<ApiGroups> => {
    const { getGroups } = useGroupService();

    return useQuery<ApiGroups>({
        queryKey: [groupsDefaultQueryKey, params],
        queryFn: () => getGroups(params),
    });
};

export const useInfiniteGroups = (params?: Omit<Params, 'page'>): InfiniteQueryObserverResult<ApiGroupsInfinite> => {
    const { getGroupsInfinite } = useGroupService();

    return useInfiniteQuery<ApiGroupsInfinite>({
        queryKey: [groupsDefaultQueryKey, params],
        queryFn: ({ pageParam = 1 }) => getGroupsInfinite({ ...params, page: pageParam }),
        getNextPageParam: (lastGroup) => lastGroup.nextPage,
        getPreviousPageParam: (firstGroup) => firstGroup.prevPage,
    });
};
