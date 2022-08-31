import { QueryObserverResult, InfiniteQueryObserverResult, useInfiniteQuery, useQuery } from '@tanstack/react-query';
import {
    ApiRestaurantParams,
    ApiRestaurants,
    useRestaurantService,
    ApiRestaurantsInfinite,
    restaurantsDefaultQueryKey,
} from '../api/RestaurantService';

export const useRestaurants = (params?: ApiRestaurantParams): QueryObserverResult<ApiRestaurants> => {
    const { getRestaurants } = useRestaurantService();

    return useQuery<ApiRestaurants>({
        queryKey: [restaurantsDefaultQueryKey, params],
        queryFn: () => getRestaurants(params),
    });
};

export const useInfiniteRestaurants = (
    params?: Omit<ApiRestaurantParams, 'page'>,
): InfiniteQueryObserverResult<ApiRestaurantsInfinite> => {
    const { getRestaurantsInfinite } = useRestaurantService();

    return useInfiniteQuery<ApiRestaurantsInfinite>({
        queryKey: [restaurantsDefaultQueryKey, params],
        queryFn: ({ pageParam = 1 }) => getRestaurantsInfinite({ ...params, page: pageParam }),
        getNextPageParam: (lastGroup) => lastGroup.nextPage,
        getPreviousPageParam: (firstGroup) => firstGroup.prevPage,
    });
};
