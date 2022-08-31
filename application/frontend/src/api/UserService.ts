import { httpClient, useHttpClient } from './httpClient';
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

export interface ApiUsersInfinite {
    data: ApiUser[];
    nextPage: number;
    prevPage: number;
}

export const useUserService = () => {
    const { httpGetClient, httpPutClient } = useHttpClient();

    const getUsers: (params?: ApiUsersParams) => Promise<ApiUsers> = (params = { page: 1, page_size: 10 }) =>
        httpGetClient<Array<ApiUser>>(endpoint, { params }).then((response) => {
            const pagination = JSON.parse(response.headers['x-pagination']);
            return {
                ...pagination,
                users: response.data,
            };
        });

    const getUsersInfinite: (params?: ApiUsersParams) => Promise<ApiUsersInfinite> = async (params) => {
        const res = await getUsers(params);
        return {
            data: res.users,
            nextPage: res.next_page,
            prevPage: res.page,
        };
    };

    const getUserById = (userId: string): Promise<ApiUser> =>
        httpGetClient<ApiUser>(`${endpoint}/${userId}`).then((response) => response.data);

    const updateUser = (userId: string, updatedUser: ApiUserPut): Promise<ApiUser> =>
        httpPutClient<ApiUser>(`${endpoint}/${userId}`, updatedUser).then((response) => response.data);

    return {
        getUsers,
        getUsersInfinite,
        getUserById,
        updateUser,
    };
};
