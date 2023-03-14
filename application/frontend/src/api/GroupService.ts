import { useHttpClient } from './httpClient';
import { Pagination, Params } from './types';
import { ApiUser } from './UserService';

const endpoint = '/groups';

export const groupsDefaultQueryKey = 'getGroups';

export interface ApiGroupBase {
    name: string;
}

export interface ApiGroup extends ApiGroupBase {
    id: string;
    members: Array<ApiUser>;
}

export interface ApiGroups extends Pagination {
    groups: ApiGroup[];
}

export interface ApiGroupPost extends ApiGroupBase {
    members: string[];
}

export interface ApiGroupPatch extends ApiGroupBase {
    members: string[];
}

export interface ApiGroupsInfinite {
    data: ApiGroup[];
    nextPage: number;
    prevPage: number;
}

export const useGroupService = () => {
    const { httpGetClient, httpPostClient, httpPatchClient, httpDeleteClient } = useHttpClient();

    const getGroups: (params?: Params) => Promise<ApiGroups> = (params = { page: 1, page_size: 10 }) =>
        httpGetClient<Array<ApiGroup>>(endpoint, { params }).then((response) => {
            const pagination = JSON.parse(response.headers['x-pagination']);
            return {
                ...pagination,
                groups: response.data,
            };
        });

    const getGroupsInfinite: (params?: Params) => Promise<ApiGroupsInfinite> = async (params) => {
        const res = await getGroups(params);
        return {
            data: res.groups,
            nextPage: res.next_page,
            prevPage: res.page,
        };
    };

    const getGroupById = (groupId: string): Promise<ApiGroup> =>
        httpGetClient<ApiGroup>(`${endpoint}/${groupId}`).then((response) => response.data);

    const postGroup = (newGroup: ApiGroupPost): Promise<ApiGroup> =>
        httpPostClient<ApiGroup>(endpoint, newGroup).then((response) => response.data);

    const patchGroup = (group: ApiGroupPatch, groupId: string): Promise<ApiGroup> =>
        httpPatchClient<ApiGroup>(`${endpoint}/${groupId}`, group).then((response) => response.data);

    const deleteGroup = (groupId: string): Promise<void> => httpDeleteClient<ApiGroup>(`${endpoint}/${groupId}`).then();

    return { getGroups, getGroupsInfinite, getGroupById, postGroup, patchGroup, deleteGroup };
};
