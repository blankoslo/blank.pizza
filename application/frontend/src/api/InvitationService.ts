import { ApiEvent } from './EventService';
import { useHttpClient } from './httpClient';
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

export const useInvitationService = () => {
    const { httpGetClient, httpPutClient } = useHttpClient();

    const getInvitationsByEvent: (eventId: string) => Promise<Array<ApiInvitation>> = (eventId) =>
        httpGetClient<Array<ApiInvitation>>(`${endpoint}/${eventId}`).then((response) => {
            return response.data;
        });

    const getInvitationByKey = (eventId: string, userId: string): Promise<ApiInvitation> =>
        httpGetClient<ApiInvitation>(`${endpoint}/${eventId}/${userId}`).then((response) => response.data);

    const putInvitation = (
        eventId: string,
        userId: string,
        updatedInvitation: ApiInvitationPut,
    ): Promise<ApiInvitation> =>
        httpPutClient<ApiInvitation>(`${endpoint}/${eventId}/${userId}`, updatedInvitation).then((response) => {
            return response.data;
        });

    return {
        getInvitationsByEvent,
        getInvitationByKey,
        putInvitation,
    };
};
