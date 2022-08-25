import { InfiniteData } from '@tanstack/react-query';
import { httpClient } from './httpClient';
import { Pagination, Params } from './types';

const endpoint = '/restaurants';

export const restaurantsDefaultQueryKey = 'getRestaurants';

export interface ApiRestaurantBase {
    name: string;
    link?: string;
    tlf?: string;
    address?: string;
}

export interface ApiRestaurant extends ApiRestaurantBase {
    id: string;
}

export interface ApiRestaurants extends Pagination {
    restaurants: ApiRestaurant[];
}

export type ApiRestaurantPost = ApiRestaurantBase;

export interface ApiRestaurantParams extends Params {
    order?: string;
}

export const getRestaurants: (params?: ApiRestaurantParams, token?: string) => Promise<ApiRestaurants> = (
    params = { page: 1, page_size: 10 },
    token,
) =>
    httpClient(token)
        .get<Array<ApiRestaurant>>(endpoint, { params })
        .then((response) => {
            const pagination = JSON.parse(response.headers['x-pagination']);
            return {
                ...pagination,
                restaurants: response.data,
            };
        });

export interface ApiRestaurantsInfinite {
    data: ApiRestaurant[];
    nextPage: number;
    prevPage: number;
}

export const getRestaurantsInfinite: (
    params?: ApiRestaurantParams,
    token?: string,
) => Promise<ApiRestaurantsInfinite> = async (params, token) => {
    const res = await getRestaurants(params, token);
    return {
        data: res.restaurants,
        nextPage: res.next_page,
        prevPage: res.page,
    };
};

export const getRestaurantById = (restaurantId: string, token?: string): Promise<ApiRestaurant> =>
    httpClient(token)
        .get<ApiRestaurant>(`${endpoint}/${restaurantId}`)
        .then((response) => response.data);

export const postRestaurant = (newRestaurant: ApiRestaurantPost, token?: string): Promise<ApiRestaurant> =>
    httpClient(token)
        .post<ApiRestaurant>(endpoint, newRestaurant)
        .then((response) => {
            return response.data;
        });

export const deleteRestaurant = (restaurantId: string, token?: string): Promise<void> =>
    httpClient(token).delete<ApiRestaurant>(`${endpoint}/${restaurantId}`).then();
