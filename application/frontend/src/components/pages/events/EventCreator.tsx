import Button from '@mui/material/Button';
import WeekPicker, { getRandomInteger, setPizzaDay } from './WeekPicker';
import { useState } from 'react';
import { useRestaurants } from '../../../hooks/useRestaurants';
import { ApiEventPost, eventsDefaultQueryKey, useEventService } from '../../../api/EventService';
import { toast } from 'react-toastify';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { Box, Paper } from '@mui/material';
import React from 'react';
import { useTranslation } from 'react-i18next';

interface Props {
    onSubmitFinished: () => void;
}

export const EventCreator: React.FC<Props> = ({ onSubmitFinished }) => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const { postEvent } = useEventService();

    const [selectedDate, setSelectedDate] = useState<Date | null>(setPizzaDay(new Date()));
    const { isLoading, data: restaurants } = useRestaurants();

    const addEventMutation = useMutation((newEvent: ApiEventPost) => postEvent(newEvent), {
        onSuccess: () => {
            toast.success(t('events.new.mutation.onSuccess'));
        },
        onError: () => {
            toast.error(t('events.new.mutation.onError'));
        },
        onSettled: () => {
            queryClient.invalidateQueries([eventsDefaultQueryKey]);
        },
    });

    const handleOnClick = async () => {
        if (selectedDate == null) {
            toast.warn(t('events.new.errors.noSelectedDate'));
            return;
        }

        if (restaurants === undefined || restaurants.restaurants.length === 0) {
            toast.warn(t('events.new.errors.noRestaurantsExists'));
            return;
        }

        let randomNumber = Math.floor(getRandomInteger(0, restaurants.restaurants.length));
        if (restaurants.restaurants.length === 3) {
            randomNumber = Math.random() > 0.5 ? 1 : 0;
        }

        const restaurant = restaurants.restaurants[randomNumber];

        addEventMutation.mutate({
            time: selectedDate.toISOString(),
            restaurant_id: restaurant.id,
        });

        onSubmitFinished();
    };

    return (
        <Box
            sx={(theme) => ({
                minWidth: '300px',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
            })}
        >
            <WeekPicker selectedDate={selectedDate} setSelectedDate={setSelectedDate} />
            <Button sx={{ marginY: 1 }} color="success" variant="contained" fullWidth onClick={() => handleOnClick()}>
                {t('events.new.button')}
            </Button>
        </Box>
    );
};
