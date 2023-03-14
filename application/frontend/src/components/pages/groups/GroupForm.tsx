import React from 'react';
import Button from '@mui/material/Button';
import { Box } from '@mui/material';
import { FormProvider, useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { toast } from 'react-toastify';
import { ApiGroup, ApiGroupPost, groupsDefaultQueryKey, useGroupService } from '../../../api/GroupService';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import i18n from 'i18next';
import TextInput from '../../TextInput';
import { SelectUsers } from '../../SelectUsers';

const validationSchema = yup.object().shape({
    name: yup
        .string()
        .min(1, i18n.t('groups.new.validation.name.min'))
        .required(i18n.t('groups.new.validation.name.required')),
    members: yup
        .array()
        .of(
            yup.object().shape({
                label: yup.string().required(),
                value: yup.string().required(),
            }),
        )
        .required(),
});

interface Schema {
    name: string;
    members: Array<{ label: string; value: string }>;
}

interface Props {
    group?: ApiGroup;
    onSubmitFinished: () => void;
}

export const GroupForm: React.FC<Props> = ({ onSubmitFinished, group }) => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const { postGroup, patchGroup } = useGroupService();

    const formMethods = useForm<Schema>({
        resolver: yupResolver(validationSchema),
        defaultValues: {
            name: group?.name ?? '',
            members: group?.members.map((member) => ({ label: member.current_username, value: member.slack_id })) ?? [],
        },
    });

    const groupMutation = useMutation(
        (_group: ApiGroupPost) => (group ? patchGroup(_group, group.id) : postGroup(_group)),
        {
            onSuccess: () => {
                toast.success(t(group ? 'groups.edit.mutation.onSuccess' : 'groups.new.mutation.onSuccess'));
                formMethods.reset();
            },
            onError: () => {
                toast.error(t(group ? 'groups.edit.mutation.onError' : 'groups.new.mutation.onError'));
            },
            onSettled: () => {
                queryClient.invalidateQueries([groupsDefaultQueryKey]);
            },
        },
    );

    const onSubmit = formMethods.handleSubmit(async (data) => {
        const newGroup: ApiGroupPost = {
            name: data.name,
            members: data.members.map((member) => member.value),
        };

        groupMutation.mutate(newGroup);
        onSubmitFinished();
    });

    return (
        <FormProvider {...formMethods}>
            <Box
                component="form"
                onSubmit={onSubmit}
                sx={{
                    display: 'flex',
                    flexDirection: 'column',
                    color: '#ffffff',
                    marginTop: 1,
                    minWidth: '300px',
                }}
            >
                <TextInput
                    name="name"
                    label={t(group ? 'groups.edit.form.name' : 'groups.new.form.name')}
                    type="text"
                />
                <SelectUsers name="members" />
                <Button variant="contained" color="success" type="submit">
                    {t(group ? 'groups.edit.form.buttons.save' : 'groups.new.form.button')}
                </Button>
            </Box>
        </FormProvider>
    );
};
