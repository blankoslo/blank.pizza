import { QueryObserverResult, InfiniteQueryObserverResult, useInfiniteQuery, useQuery } from '@tanstack/react-query';
import {
    ApiRestaurantParams,
    ApiRestaurants,
    getRestaurants,
    getRestaurantsInfinite,
    ApiRestaurantsInfinite,
    restaurantsDefaultQueryKey,
} from '../api/RestaurantService';

export const useRestaurants = (params?: ApiRestaurantParams): QueryObserverResult<ApiRestaurants> => {
    return useQuery<ApiRestaurants>({
        queryKey: [restaurantsDefaultQueryKey, params],
        queryFn: () => getRestaurants(params),
    });
};

export const useInfiniteRestaurants = (
    params?: Omit<ApiRestaurantParams, 'page'>,
): InfiniteQueryObserverResult<ApiRestaurantsInfinite> => {
    return useInfiniteQuery<ApiRestaurantsInfinite>({
        queryKey: [restaurantsDefaultQueryKey, params],
        queryFn: ({ pageParam = 1 }) => getRestaurantsInfinite({ ...params, page: pageParam }),
        getNextPageParam: (lastGroup) => lastGroup.nextPage,
        getPreviousPageParam: (firstGroup) => firstGroup.prevPage,
    });
};
