import React, { useCallback } from 'react';
import { useEffect } from 'react';
import { InputLabel, Paper } from '@mui/material';
import Typography from '@mui/material/Typography';
import { Box } from '@mui/material';
import { useTranslation } from 'react-i18next';
import Image from 'mui-image';
import TextInput from '../../TextInput';
import { FormProvider, useForm, SubmitHandler } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import i18n from 'i18next';
import { ApiUser, ApiUserPut, useUserService, usersDefaultQueryKey } from '../../../api/UserService';
import SwitchInput from '../../SwitchInput';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'react-toastify';
import { dateToString } from '../../utils/dateToString';

const validationSchema = yup.object().shape({
    priority: yup
        .number()
        .min(1, i18n.t('restaurants.new.validation.name.min'))
        .max(10, i18n.t('restaurants.new.validation.name.max'))
        .required(i18n.t('restaurants.new.validation.name.required')),
    active: yup.boolean().required(),
});

const UserCard: React.FC<ApiUser> = ({ slack_id, current_username, first_seen, email, active, priority }) => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const { updateUser } = useUserService();

    const { handleSubmit, watch, ...formMethods } = useForm<ApiUserPut>({
        resolver: yupResolver(validationSchema),
        defaultValues: {
            priority: priority ?? 1,
            active: active,
        },
    });

    const addUserMutation = useMutation((updatedUser: ApiUserPut) => updateUser(slack_id, updatedUser), {
        onSuccess: () => {
            toast.dismiss();
            toast.success(t('users.update.mutation.onSuccess'));
        },
        onError: () => {
            toast.dismiss();
            toast.error(t('users.update.mutation.onError'));
        },
        onSettled: () => {
            queryClient.invalidateQueries([usersDefaultQueryKey]);
        },
    });

    const onSubmit: SubmitHandler<ApiUserPut> = useCallback(
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
            <Paper
                component="form"
                sx={{
                    marginBottom: 1,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    overflow: 'auto',
                }}
            >
                <Box
                    sx={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                    }}
                >
                    <Box>
                        <Image src="" height={50} width={50} wrapperStyle={{ marginRight: 12 }} showLoading />
                    </Box>
                    <Box>
                        <Box sx={{ display: 'flex' }}>
                            <Typography>{t('users.list.card.username')}</Typography>
                            {current_username}
                        </Box>
                        <Box sx={{ display: 'flex' }}>
                            <Typography>{t('users.list.card.email')}</Typography>
                            {email ?? t('users.list.card.noEmail')}
                        </Box>
                        <Box sx={{ display: 'flex' }}>
                            <Typography>{t('users.list.card.joined')}</Typography>
                            {dateToString(first_seen)}
                        </Box>
                    </Box>
                </Box>
                <Box
                    sx={{
                        display: 'flex',
                        flexDirection: 'column',
                        marginRight: 1,
                    }}
                >
                    <Box sx={{ width: '62px' }}>
                        <TextInput
                            alwaysShowNumberArrows={true}
                            marginBottom={false}
                            centerText={true}
                            variant="standard"
                            name="priority"
                            min={1}
                            max={10}
                            type="number"
                        />
                        <InputLabel sx={{ textAlign: 'center' }}>{t('users.list.card.priority')}</InputLabel>
                    </Box>
                    <SwitchInput name="active" labelPlacement="bottom" label={t('users.list.card.active')} />
                </Box>
            </Paper>
        </FormProvider>
    );
};

export { UserCard };
