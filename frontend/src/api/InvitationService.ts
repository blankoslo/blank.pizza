import { ApiEvent } from './EventService';
import { httpClient } from './httpClient';
import { Pagination, Params } from './types';
import { ApiUser } from './UserService';

const endpoint = '/invitations';

export const invitationsDefaultQueryKey = 'getInvitations';

export interface ApiInvitationBase {
    rsvp: string;
}

export interface ApiInvitation extends ApiInvitationBase {
    event_id: string;
    slack_id: string;
    event: ApiEvent;
    slack_user: ApiUser;
    invited_at: string;
    reminded_at: string;
}

export type ApiInvitationPut = ApiInvitationBase;

export const getInvitationsByEvent: (eventId: string, token?: string) => Promise<Array<ApiInvitation>> = (
    eventId,
    token,
) =>
    httpClient(token)
        .get<Array<ApiInvitation>>(`${endpoint}/${eventId}`)
        .then((response) => {
            return response.data;
        });

export const getInvitationByKey = (eventId: string, userId: string, token?: string): Promise<ApiInvitation> =>
    httpClient(token)
        .get<ApiInvitation>(`${endpoint}/${eventId}/${userId}`)
        .then((response) => response.data);

export const putInvitation = (
    eventId: string,
    userId: string,
    updatedInvitation: ApiInvitationPut,
    token?: string,
): Promise<ApiInvitation> =>
    httpClient(token)
        .put<ApiInvitation>(`${endpoint}/${eventId}/${userId}`, updatedInvitation)
        .then((response) => {
            return response.data;
        });
