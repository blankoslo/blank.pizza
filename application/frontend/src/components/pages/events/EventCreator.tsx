import Button from '@mui/material/Button';
import WeekPicker, { getRandomInteger, setPizzaDay } from './WeekPicker';
import { useState } from 'react';
import { useRestaurants } from '../../../hooks/useRestaurants';
import { ApiEventPost, eventsDefaultQueryKey, useEventService } from '../../../api/EventService';
import { toast } from 'react-toastify';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { Box, Checkbox, styled } from '@mui/material';
import React from 'react';
import { useTranslation } from 'react-i18next';
import { SelectGroup } from '../../SelectGroup';
import { useForm, FormProvider, useWatch } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import i18n from 'i18next';

const StyledInput = styled('input')({
    padding: '1rem',
    width: '100%',
    fontSize: '1.25rem',
});

const validationSchema = yup.object().shape({
    date: yup.date().required(),
    peoplePerEvent: yup.number().min(2).max(100).required(),
    usingGroup: yup.boolean().required(),
    group: yup
        .object()
        .shape({
            label: yup.string().required(),
            value: yup.string().required(),
        })
        .when('usingGroup', {
            is: true,
            then: (schema) => schema.required(),
            otherwise: (schema) => schema,
        })
        .nullable()
        .default(null),
});

interface Schema {
    date: Date;
    peoplePerEvent: number;
    usingGroup: boolean;
    group: {
        label: string;
        value: string;
    };
}

interface Props {
    onSubmitFinished: () => void;
}

export const EventCreator: React.FC<Props> = ({ onSubmitFinished }) => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const { postEvent } = useEventService();

    const formMethods = useForm<Schema>({
        resolver: yupResolver(validationSchema),
        defaultValues: {
            date: setPizzaDay(new Date()) ?? new Date(),
            peoplePerEvent: 5,
            usingGroup: false,
        },
    });

    const usingGroup = useWatch({ control: formMethods.control, name: 'usingGroup' });

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

    const onSubmit = formMethods.handleSubmit(async (data) => {
        if (restaurants === undefined || restaurants.restaurants.length === 0) {
            toast.warn(t('events.new.errors.noRestaurantsExists'));
            return;
        }

        let randomNumber = Math.floor(getRandomInteger(0, restaurants.restaurants.length));
        if (restaurants.restaurants.length === 3) {
            randomNumber = Math.random() > 0.5 ? 1 : 0;
        }

        const restaurant = restaurants.restaurants[randomNumber];

        const event: ApiEventPost = {
            time: data.date.toISOString(),
            restaurant_id: restaurant.id,
            people_per_event: data.peoplePerEvent,
        };

        if (data.usingGroup) {
            event.group_id = data.group.value;
        }

        addEventMutation.mutate(event);

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
                    alignItems: 'center',
                }}
            >
                <WeekPicker name="date" />
                <Box>
                    <label htmlFor="groupSelect">{t('groups.groupSelect.label')}</label>
                    <Box
                        sx={{
                            display: 'flex',
                            gap: 1,
                        }}
                    >
                        <Checkbox
                            {...formMethods.register('usingGroup')}
                            disableRipple
                            sx={{ '& .MuiSvgIcon-root': { fontSize: 28 }, padding: 0 }}
                        />
                        <SelectGroup disabled={!usingGroup} />
                    </Box>
                </Box>
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
                        type="number"
                        min={2}
                        max={100}
                        {...formMethods.register('peoplePerEvent')}
                    />
                </Box>
                <Button sx={{ marginY: 1 }} color="success" variant="contained" fullWidth type="submit">
                    {t('events.new.button')}
                </Button>
            </Box>
        </FormProvider>
    );
};
