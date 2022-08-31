import { useHttpClient } from './httpClient';
import { ApiRestaurant } from './RestaurantService';
import { Pagination, Params } from './types';

const endpoint = '/events';

export const eventsDefaultQueryKey = 'getEvents';

export interface ApiEventBase {
    time: string;
}

export interface ApiEvent extends ApiEventBase {
    id: string;
    finalized: boolean;
    restaurant?: ApiRestaurant;
}

export interface ApiEvents extends Pagination {
    events: ApiEvent[];
}

export interface ApiEventPost extends ApiEventBase {
    time: string;
    restaurant_id: string;
}

export interface ApiEventsParams extends Params {
    age?: string;
    order?: string;
}

export interface ApiEventsInfinite {
    data: ApiEvent[];
    nextPage: number;
    prevPage: number;
}

export const useEventService = () => {
    const { httpGetClient, httpPostClient } = useHttpClient();

    const postEvent = (newEvent: ApiEventPost): Promise<ApiEvent> =>
        httpPostClient<ApiEvent>(endpoint, newEvent).then((response) => response.data);

    const getEventById = (eventId: number): Promise<ApiEvent> =>
        httpGetClient<ApiEvent>(`${endpoint}/${eventId}`).then((response) => response.data);

    const getEvents: (params?: ApiEventsParams) => Promise<ApiEvents> = (params = { page: 1, page_size: 10 }) =>
        httpGetClient<ApiEvent>(endpoint, { params }).then((response) => {
            const pagination = JSON.parse(response.headers['x-pagination']);
            return {
                ...pagination,
                events: response.data,
            };
        });

    const getRestaurantsInfinite: (params?: ApiEventsParams) => Promise<ApiEventsInfinite> = async (params) => {
        const res = await getEvents(params);
        return {
            data: res.events,
            nextPage: res.next_page,
            prevPage: res.page,
        };
    };

    return {
        postEvent,
        getEventById,
        getEvents,
        getRestaurantsInfinite,
    };
};
