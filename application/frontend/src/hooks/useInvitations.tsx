import { QueryObserverResult, useQuery } from '@tanstack/react-query';
import { ApiInvitation, useInvitationService, invitationsDefaultQueryKey } from '../api/InvitationService';

export const useInvitations = (eventId: string): QueryObserverResult<Array<ApiInvitation>> => {
    const { getInvitationsByEvent } = useInvitationService();

    return useQuery<Array<ApiInvitation>>({
        queryKey: [invitationsDefaultQueryKey, eventId],
        queryFn: () => getInvitationsByEvent(eventId),
    });
};
