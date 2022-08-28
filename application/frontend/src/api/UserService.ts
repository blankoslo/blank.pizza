import { httpClient } from './httpClient';
import { Pagination, Params } from './types';

const endpoint = '/users';

export const usersDefaultQueryKey = 'getUsers';

export interface ApiUserBase {
    active: boolean;
    priority: number;
}

export interface ApiUser extends ApiUserBase {
    slack_id: string;
    current_username: string;
    first_seen: string;
    email?: string;
}

export interface ApiUsers extends Pagination {
    users: ApiUser[];
}

export type ApiUserPut = ApiUserBase;

export interface ApiUsersParams extends Params {
    current_username?: string;
    email?: string;
    active?: boolean;
}

export const getUsers: (params?: ApiUsersParams, token?: string) => Promise<ApiUsers> = (
    params = { page: 1, page_size: 10 },
    token,
) =>
    httpClient(token)
        .get<Array<ApiUser>>(endpoint, { params })
        .then((response) => {
            const pagination = JSON.parse(response.headers['x-pagination']);
            return {
                ...pagination,
                users: response.data,
            };
        });

export interface ApiUsersInfinite {
    data: ApiUser[];
    nextPage: number;
    prevPage: number;
}

export const getUsersInfinite: (params?: ApiUsersParams, token?: string) => Promise<ApiUsersInfinite> = async (
    params,
    token,
) => {
    const res = await getUsers(params, token);
    return {
        data: res.users,
        nextPage: res.next_page,
        prevPage: res.page,
    };
};

export const getUserById = (userId: string, token?: string): Promise<ApiUser> =>
    httpClient(token)
        .get<ApiUser>(`${endpoint}/${userId}`)
        .then((response) => response.data);

export const updateUser = (userId: string, updatedUser: ApiUserPut, token?: string): Promise<ApiUser> =>
    httpClient(token)
        .put<ApiUser>(`${endpoint}/${userId}`, updatedUser)
        .then((response) => response.data);
