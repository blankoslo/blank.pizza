import { httpClient } from './httpClient';
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

export const getEvents: (params?: ApiEventsParams, token?: string) => Promise<ApiEvents> = (
    params = { page: 1, page_size: 10 },
    token,
) =>
    httpClient(token)
        .get<Array<ApiEvent>>(endpoint, { params })
        .then((response) => {
            const pagination = JSON.parse(response.headers['x-pagination']);
            return {
                ...pagination,
                events: response.data,
            };
        });

export interface ApiEventsInfinite {
    data: ApiEvent[];
    nextPage: number;
    prevPage: number;
}

export const getRestaurantsInfinite: (params?: ApiEventsParams, token?: string) => Promise<ApiEventsInfinite> = async (
    params,
    token,
) => {
    const res = await getEvents(params, token);
    return {
        data: res.events,
        nextPage: res.next_page,
        prevPage: res.page,
    };
};

export const getEventById = (eventId: number, token?: string): Promise<ApiEvent> =>
    httpClient(token)
        .get<ApiEvent>(`${endpoint}/${eventId}`)
        .then((response) => response.data);

export const postEvent = (newEvent: ApiEventPost, token?: string): Promise<ApiEvent> =>
    httpClient(token)
        .post<ApiEvent>(endpoint, newEvent)
        .then((response) => {
            return response.data;
        });
