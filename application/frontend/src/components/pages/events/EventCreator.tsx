import Button from '@mui/material/Button';
import WeekPicker, { getRandomInteger, setPizzaDay } from './WeekPicker';
import { useState } from 'react';
import { useRestaurants } from '../../../hooks/useRestaurants';
import { ApiEventPost, eventsDefaultQueryKey, useEventService } from '../../../api/EventService';
import { toast } from 'react-toastify';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { Box, Paper, styled } from '@mui/material';
import React from 'react';
import { useTranslation } from 'react-i18next';

const StyledInput = styled('input')({
    padding: '1rem',
    width: '100%',
    fontSize: '1.25rem',
});

interface Props {
    onSubmitFinished: () => void;
}

export const EventCreator: React.FC<Props> = ({ onSubmitFinished }) => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const { postEvent } = useEventService();

    const [selectedDate, setSelectedDate] = useState<Date | null>(setPizzaDay(new Date()));
    const [peoplePerEvent, setPeoplePerEvent] = useState(5);
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

        if (!Number.isInteger(peoplePerEvent) || peoplePerEvent < 2 || peoplePerEvent > 100) {
            toast.warn(t('events.new.errors.peoplePerEvent'));
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
            people_per_event: peoplePerEvent,
        });

        onSubmitFinished();
    };

    const onPeoplePerEventChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const value = parseInt(event.target.value);
        if (!Number.isInteger(value) || value < 2) {
            setPeoplePerEvent(2);
            return;
        }
        if (value > 100) {
            setPeoplePerEvent(100);
            return;
        }
        setPeoplePerEvent(parseInt(event.target.value));
    };

    return (
        <Box
            sx={(theme) => ({
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
            })}
        >
            <WeekPicker selectedDate={selectedDate} setSelectedDate={setSelectedDate} />
            <Box
                sx={{
                    display: 'flex',
                    flexDirection: 'column',
                    width: '100%',
                }}
            >
                <label htmlFor="peoplePerEventInput">{t('events.new.peoplePerEventInput.label')}</label>
                <StyledInput
                    id="peoplePerEventInput"
                    name="peoplePerEvent"
                    type="number"
                    min={2}
                    max={100}
                    value={peoplePerEvent}
                    onChange={onPeoplePerEventChange}
                />
            </Box>
            <Button sx={{ marginY: 1 }} color="success" variant="contained" fullWidth onClick={() => handleOnClick()}>
                {t('events.new.button')}
            </Button>
        </Box>
    );
};
