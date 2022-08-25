import { QueryObserverResult, useQuery } from '@tanstack/react-query';
import { ApiInvitation, getInvitationsByEvent, invitationsDefaultQueryKey } from '../api/InvitationService';

export const useInvitations = (eventId: string): QueryObserverResult<Array<ApiInvitation>> => {
    return useQuery<Array<ApiInvitation>>({
        queryKey: [invitationsDefaultQueryKey, eventId],
        queryFn: () => getInvitationsByEvent(eventId),
    });
};
