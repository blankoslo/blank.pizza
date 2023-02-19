import { useHttpClient } from './httpClient';
import { ApiRestaurant } from './RestaurantService';
import { Pagination, Params } from './types';
import { ApiUser } from './UserService';

const endpoint = '/images';

export const imagesDefaultQueryKey = 'getImages';

export interface ApiImage {
    cloudinary_id: string;
    uploaded_by: ApiUser;
    uploaded_at: string;
    title: string;
}

export interface ApiImages extends Pagination {
    events: ApiImage[];
}

export interface ApiImagesParams extends Params {
    order?: string;
}

export interface ApiImagesInfinite {
    data: ApiImage[];
    nextPage: number;
    prevPage: number;
}

export const useEventService = () => {
    const { httpGetClient } = useHttpClient();

    const getEventById = (eventId: number): Promise<ApiImage> =>
        httpGetClient<ApiImage>(`${endpoint}/${eventId}`).then((response) => response.data);

    const getEvents: (params?: ApiImagesParams) => Promise<ApiImages> = (params = { page: 1, page_size: 10 }) =>
        httpGetClient<ApiImage>(endpoint, { params }).then((response) => {
            const pagination = JSON.parse(response.headers['x-pagination']);
            return {
                ...pagination,
                events: response.data,
            };
        });

    const getImagesInfinite: (params?: ApiImagesParams) => Promise<ApiImagesInfinite> = async (params) => {
        const res = await getEvents(params);
        return {
            data: res.events,
            nextPage: res.next_page,
            prevPage: res.page,
        };
    };

    return {
        getEventById,
        getEvents,
        getImagesInfinite,
    };
};
