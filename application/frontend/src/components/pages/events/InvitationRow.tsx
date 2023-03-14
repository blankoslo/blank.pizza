import React, { useCallback, useEffect } from 'react';
import Typography from '@mui/material/Typography';
import { useTranslation } from 'react-i18next';
import { Box } from '@mui/material';
import { datetimeToString } from '../../utils/datetimeToString';
import Image from 'mui-image';
import SelectInput from '../../SelectInput';
import { FormProvider, SubmitHandler, useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import i18n from 'i18next';
import {
    ApiInvitation,
    ApiInvitationPut,
    invitationsDefaultQueryKey,
    useInvitationService,
} from '../../../api/InvitationService';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'react-toastify';

const validationSchema = yup.object().shape({
    rsvp: yup.string().required(i18n.t('invitations.update.validation.rsvp.required')),
});

interface Props extends ApiInvitation {
    eventTime: Date;
}

const InvitationRow: React.FC<Props> = ({ eventTime, event_id, slack_id, slack_user, invited_at, reminded_at, rsvp }) => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const { putInvitation } = useInvitationService();

    const { handleSubmit, watch, ...formMethods } = useForm<ApiInvitationPut>({
        resolver: yupResolver(validationSchema),
        defaultValues: {
            rsvp: rsvp,
        },
    });

    const addUserMutation = useMutation(
        (updatedInvitation: ApiInvitationPut) => putInvitation(event_id, slack_id, updatedInvitation),
        {
            onSuccess: () => {
                toast.dismiss();
                toast.success(t('invitations.update.mutation.onSuccess'));
            },
            onError: () => {
                toast.dismiss();
                toast.error(t('invitations.update.mutation.onError'));
            },
            onSettled: () => {
                queryClient.invalidateQueries([invitationsDefaultQueryKey]);
            },
        },
    );

    const onSubmit: SubmitHandler<ApiInvitationPut> = useCallback(
        (data) => {
            addUserMutation.mutate(data);
        },
        [addUserMutation],
    );

    useEffect(() => {
        const handler = handleSubmit(onSubmit);
        const subscription = watch(() => handler());
        return () => subscription.unsubscribe();
    }, [onSubmit, handleSubmit, watch]);

    return (
        <FormProvider handleSubmit={handleSubmit} watch={watch} {...formMethods}>
            <Box
                sx={(theme) => ({
                    borderTop: '1px solid gray',
                    padding: 1,
                    display: 'flex',
                    justifyContent: 'space-between',
                    [theme.breakpoints.down('md')]: {
                        flexDirection: 'column',
                    },
                })}
            >
                <Box
                    sx={{
                        display: 'flex',
                        gap: 2,
                    }}
                >
                    <Box
                        sx={{
                            display: 'flex',
                            alignItems: 'center',
                        }}
                    >
                        <Image src="" height={50} width={50} showLoading />
                    </Box>
                    <Box>
                        <Typography>{slack_user.current_username}</Typography>
                        <Typography sx={{ display: 'flex' }}>
                            <Typography component="span" sx={{ fontWeight: 'bold', whiteSpace: 'nowrap' }}>
                                {t('invitations.list.invitedAt')}
                            </Typography>
                            {datetimeToString(invited_at)}
                        </Typography>
                        <Typography sx={{ display: 'flex' }}>
                            <Typography component="span" sx={{ fontWeight: 'bold', whiteSpace: 'nowrap' }}>
                                {t('invitations.list.remindedAt')}
                            </Typography>
                            {datetimeToString(reminded_at)}
                        </Typography>
                    </Box>
                </Box>
                <Box
                    sx={{
                        display: 'flex',
                        alignItems: 'center',
                    }}
                >
                    <SelectInput
                        disabled={eventTime < new Date()}
                        name="rsvp"
                        width={140}
                        fullWidthMobile={true}
                        marginLeft={false}
                        items={[
                            { value: 'attending', text: 'attending' },
                            { value: 'not attending', text: 'not attending' },
                            { value: 'unanswered', text: 'unanswered' },
                        ]}
                    />
                </Box>
            </Box>
        </FormProvider>
    );
};

export { InvitationRow };
