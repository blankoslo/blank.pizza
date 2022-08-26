import Button from '@mui/material/Button';
import WeekPicker, { getRandomInteger, PIZZA_EVENT_TIME_IN_HOURS_24_HOURS } from './WeekPicker';
import { useState } from 'react';
import { useRestaurants } from '../../../../hooks/useRestaurants';
import { postEvent, ApiEventPost, eventsDefaultQueryKey } from '../../../../api/EventService';
import { toast } from 'react-toastify';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { set } from 'date-fns';
import { Box, Paper } from '@mui/material';
import React from 'react';
import { useTranslation } from 'react-i18next';

export const EventCreator: React.FC = () => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();

    const [selectedDate, setSelectedDate] = useState<Date | null>(new Date());
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
        console.log(selectedDate);

        if (selectedDate == null) {
            toast.warn(t('events.new.errors.noSelectedDate'));
            return;
        }
        console.log(restaurants);
        if (restaurants === undefined || restaurants.restaurants.length === 0) {
            toast.warn(t('events.new.errors.noRestaurantsExists'));
            return;
        }

        let randomNumber = Math.floor(getRandomInteger(0, restaurants.restaurants.length));
        if (restaurants.restaurants.length < 3) {
            randomNumber = Math.random() > 0.5 ? 1 : 0;
        }

        const restaurant = restaurants.restaurants[randomNumber];

        const date = set(selectedDate, {
            hours: PIZZA_EVENT_TIME_IN_HOURS_24_HOURS,
            minutes: 0,
            seconds: 0,
            milliseconds: 0,
        });

        addEventMutation.mutate({
            time: date.toISOString(),
            restaurant_id: restaurant.id,
        });
    };

    return (
        <Paper
            sx={(theme) => ({
                width: '30vw',
                minWidth: '500px',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                backgroundColor: theme.palette.secondary.main,
                borderRadius: '12px',
            })}
        >
            <Box
                sx={{
                    fontSize: '25px',
                    margin: '8px',
                }}
            >
                {t('events.new.title')}
            </Box>
            <Box>
                <WeekPicker value={selectedDate} setSelectedDate={setSelectedDate} />
                <Button
                    sx={{ marginY: 1 }}
                    color="success"
                    variant="contained"
                    fullWidth
                    onClick={() => handleOnClick()}
                >
                    {t('events.new.button')}
                </Button>
            </Box>
        </Paper>
    );
};
