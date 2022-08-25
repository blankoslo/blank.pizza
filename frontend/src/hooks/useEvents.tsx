import { InfiniteQueryObserverResult, QueryObserverResult, useInfiniteQuery, useQuery } from '@tanstack/react-query';
import {
    ApiEvents,
    ApiEventsInfinite,
    ApiEventsParams,
    eventsDefaultQueryKey,
    getEvents,
    getRestaurantsInfinite,
} from '../api/EventService';

export const useEvents = (params: ApiEventsParams): QueryObserverResult<ApiEvents> => {
    return useQuery<ApiEvents>({
        queryKey: [eventsDefaultQueryKey, params],
        queryFn: () => getEvents(params),
    });
};

export const useInfiniteEvents = (
    params?: Omit<ApiEventsParams, 'page'>,
): InfiniteQueryObserverResult<ApiEventsInfinite> => {
    return useInfiniteQuery<ApiEventsInfinite>({
        queryKey: [eventsDefaultQueryKey, params],
        queryFn: ({ pageParam = 1 }) => getRestaurantsInfinite({ ...params, page: pageParam }),
        getNextPageParam: (lastGroup) => lastGroup.nextPage,
        getPreviousPageParam: (firstGroup) => firstGroup.prevPage,
    });
};
