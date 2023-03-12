import Button from '@mui/material/Button';
import DateTimePicker from '../../DateTimePicker';
import { useState } from 'react';
import { useRestaurants } from '../../../hooks/useRestaurants';
import {ApiEventPatch, ApiEventPost, eventsDefaultQueryKey, useEventService} from '../../../api/EventService';
import { toast } from 'react-toastify';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { Box, Paper } from '@mui/material';
import React from 'react';
import { useTranslation } from 'react-i18next';
import { ApiRestaurant, ApiRestaurantPost, restaurantsDefaultQueryKey } from '../../../api/RestaurantService';
import { SelectRestaurant } from '../../SelectRestaurant';
import { FormProvider, useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { Option } from '../../SelectPaginate';
import DialogDeleteEvent from './DialogDeleteEvent';

interface formType {
    restaurant: Option;
    date: Date;
}

const validationSchema = yup.object().shape({
    restaurant: yup
        .object()
        .shape({
            label: yup.string().required(),
            value: yup.string().required(),
        })
        .required(),
    date: yup.date().required(),
});

interface Props {
    onSubmitFinished: () => void;
    eventId: string;
    eventTime: Date;
    restaurant?: ApiRestaurant;
}

export const EventEditor: React.FC<Props> = ({ onSubmitFinished, eventId, eventTime, restaurant }) => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const { patchEvent, deleteEvent } = useEventService();

    const [showDeleteDialog, setShowDeleteDialog] = useState(false);

    const formMethods = useForm<formType>({
        resolver: yupResolver(validationSchema),
        defaultValues: {
            restaurant: {
                label: restaurant?.name,
                value: restaurant?.id,
            },
            date: eventTime,
        },
    });

    const [selectedDate, setSelectedDate] = useState<Date | null>(eventTime);

    const addEventMutation = useMutation((newEvent: ApiEventPatch) => patchEvent(newEvent, eventId), {
        onSuccess: () => {
            toast.success(t('events.edit.mutation.onSuccess'));
        },
        onError: () => {
            toast.error(t('events.edit.mutation.onError'));
        },
        onSettled: () => {
            queryClient.invalidateQueries([eventsDefaultQueryKey]);
        },
    });

    const onSubmit = formMethods.handleSubmit(async (data) => {
        await addEventMutation.mutate({
            time: data.date.toISOString(),
            restaurant_id: data.restaurant.value.toString(),
        });

        onSubmitFinished();
    });

    const addEventDeleteMutation = useMutation((id: string) => deleteEvent(id), {
        onSuccess: () => {
            toast.success(t('events.delete.mutation.onSuccess'));
        },
        onError: () => {
            toast.error(t('events.delete.mutation.onError'));
        },
        onSettled: () => {
            queryClient.invalidateQueries([restaurantsDefaultQueryKey]);
            queryClient.invalidateQueries([eventsDefaultQueryKey]);
        },
    });

    const onDelete = () => {
        addEventDeleteMutation.mutate(eventId);
        onSubmitFinished();
    };

    const toggleShowDeleteDialog = () => {
        setShowDeleteDialog((prevState) => !prevState);
    };

    return (
        <>
            <DialogDeleteEvent open={showDeleteDialog} handleClose={toggleShowDeleteDialog} onDelete={onDelete} />
            <FormProvider {...formMethods}>
                <Box
                    component="form"
                    onSubmit={onSubmit}
                    sx={() => ({
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                    })}
                >
                    <SelectRestaurant />
                    <DateTimePicker name="date" />
                    <Box
                        sx={{
                            display: 'flex',
                            gap: 1,
                            width: '100%',
                        }}
                    >
                        <Button
                            sx={{ marginY: 1 }}
                            color="error"
                            variant="contained"
                            fullWidth
                            onClick={toggleShowDeleteDialog}
                        >
                            {t('events.delete.button')}
                        </Button>
                        <Button sx={{ marginY: 1 }} color="success" variant="contained" fullWidth type="submit">
                            {t('events.edit.buttons.save')}
                        </Button>
                    </Box>
                </Box>
            </FormProvider>
        </>
    );
};
