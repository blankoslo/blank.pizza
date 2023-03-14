import { useHttpClient } from './httpClient';
import { ApiRestaurant } from './RestaurantService';
import { Pagination, Params } from './types';
import {ApiGroup} from "./GroupService";

const endpoint = '/events';

export const eventsDefaultQueryKey = 'getEvents';

export interface ApiEventBase {
    time: string;
}

export interface ApiEvent extends ApiEventBase {
    id: string;
    finalized: boolean;
    restaurant?: ApiRestaurant;
    people_per_event: number;
    group?: ApiGroup;
}

export interface ApiEvents extends Pagination {
    events: ApiEvent[];
}

export interface ApiEventPost extends ApiEventBase {
    restaurant_id: string;
    people_per_event: number;
    group_id?: string;
}

export interface ApiEventPatch extends ApiEventBase {
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
    const { httpGetClient, httpPostClient, httpPatchClient, httpDeleteClient } = useHttpClient();

    const postEvent = (newEvent: ApiEventPost): Promise<ApiEvent> =>
        httpPostClient<ApiEvent>(endpoint, newEvent).then((response) => response.data);

    const patchEvent = (newEvent: ApiEventPatch, eventId: string): Promise<ApiEvent> =>
        httpPatchClient<ApiEvent>(`${endpoint}/${eventId}`, newEvent).then((response) => response.data);

    const deleteEvent = (eventId: string): Promise<void> => httpDeleteClient<ApiEvent>(`${endpoint}/${eventId}`).then();

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
        patchEvent,
        deleteEvent,
        getEventById,
        getEvents,
        getRestaurantsInfinite,
    };
};
