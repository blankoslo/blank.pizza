import { InfiniteQueryObserverResult, QueryObserverResult, useInfiniteQuery, useQuery } from '@tanstack/react-query';
import {
    ApiImages,
    ApiImagesInfinite,
    ApiImagesParams,
    imagesDefaultQueryKey,
    useEventService,
} from '../api/ImageService';

export const useImages = (params: ApiImagesParams): QueryObserverResult<ApiImages> => {
    const { getEvents } = useEventService();

    return useQuery<ApiImages>({
        queryKey: [imagesDefaultQueryKey, params],
        queryFn: () => getEvents(params),
    });
};

export const useInfiniteImages = (
    params?: Omit<ApiImagesParams, 'page'>,
): InfiniteQueryObserverResult<ApiImagesInfinite> => {
    const { getImagesInfinite } = useEventService();

    return useInfiniteQuery<ApiImagesInfinite>({
        queryKey: [imagesDefaultQueryKey, params],
        queryFn: ({ pageParam = 1 }) => getImagesInfinite({ ...params, page: pageParam }),
        getNextPageParam: (lastGroup) => lastGroup.nextPage,
        getPreviousPageParam: (firstGroup) => firstGroup.prevPage,
    });
};
