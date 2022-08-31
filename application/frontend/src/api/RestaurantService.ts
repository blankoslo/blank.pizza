import { useHttpClient } from './httpClient';
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
    rating?: number;
}

export interface ApiRestaurants extends Pagination {
    restaurants: ApiRestaurant[];
}

export type ApiRestaurantPost = ApiRestaurantBase;

export interface ApiRestaurantParams extends Params {
    order?: string;
}

export interface ApiRestaurantsInfinite {
    data: ApiRestaurant[];
    nextPage: number;
    prevPage: number;
}

export const useRestaurantService = () => {
    const { httpGetClient, httpPostClient, httpDeleteClient } = useHttpClient();

    const getRestaurants: (params?: ApiRestaurantParams) => Promise<ApiRestaurants> = (
        params = { page: 1, page_size: 10 },
    ) =>
        httpGetClient<Array<ApiRestaurant>>(endpoint, { params }).then((response) => {
            const pagination = JSON.parse(response.headers['x-pagination']);
            return {
                ...pagination,
                restaurants: response.data,
            };
        });

    const getRestaurantsInfinite: (params?: ApiRestaurantParams) => Promise<ApiRestaurantsInfinite> = async (
        params,
    ) => {
        const res = await getRestaurants(params);
        return {
            data: res.restaurants,
            nextPage: res.next_page,
            prevPage: res.page,
        };
    };

    const getRestaurantById = (restaurantId: string): Promise<ApiRestaurant> =>
        httpGetClient<ApiRestaurant>(`${endpoint}/${restaurantId}`).then((response) => response.data);

    const postRestaurant = (newRestaurant: ApiRestaurantPost): Promise<ApiRestaurant> =>
        httpPostClient<ApiRestaurant>(endpoint, newRestaurant).then((response) => response.data);

    const deleteRestaurant = (restaurantId: string): Promise<void> =>
        httpDeleteClient<ApiRestaurant>(`${endpoint}/${restaurantId}`).then();

    return { getRestaurants, getRestaurantsInfinite, getRestaurantById, postRestaurant, deleteRestaurant };
};
