import * as React from 'react';
import startOfWeek from 'date-fns/startOfWeek';
import add from 'date-fns/add';
import { addDays, isSameDay, set } from 'date-fns';
import 'react-datepicker/dist/react-datepicker.css';
import isSameISOWeek from 'date-fns/isSameISOWeek';
import { _DateTimePicker } from '../../DateTimePicker';
import {Controller, useFormContext} from "react-hook-form";
import {useEffect} from "react";

export const PIZZA_EVENT_TIME_IN_HOURS_24_HOURS = 18;

export const getRandomInteger = (min = 2, max = 5) => {
    /** Selects number in range [x,y) */
    // const min = 2; //tuesday
    // const max = 5; //friday
    return Math.random() * (max - min) + min;
};

const setTime = (date: Date | null) => {
    if (!date) {
        return null;
    }

    return set(date, {
        hours: PIZZA_EVENT_TIME_IN_HOURS_24_HOURS,
        minutes: 0,
        seconds: 0,
        milliseconds: 0,
    });
};

export const selectRandomPizzaDay = (selectedDate: Date | null) => {
    if (!selectedDate) {
        return null;
    }
    const start = startOfWeek(selectedDate);
    const randomInteger = getRandomInteger();
    const randomDate = add(start, { days: randomInteger });

    const today = getMinDate();
    const thursday = 4;
    const wednesday = 3;

    // Don't randomly select a date in the past
    if (randomDate < today) {
        if (today.getDay() > thursday || today.getDay() === 0) {
            // is today after thursday? i.e: are there any available pizzadays this week?
            const startOfNextWeek = startOfWeek(add(selectedDate, { days: 7 }));
            const randomDateNextWeek = add(startOfNextWeek, {
                days: randomInteger,
            });
            return randomDateNextWeek;
        } else if (today.getDay() === thursday) {
            return today;
        } else if (today.getDay() === wednesday) {
            return add(start, { days: getRandomInteger(3, 5) });
        }
    }
    return randomDate;
};

const getMinDate = () => {
    let date = new Date();
    if (date.getHours() > PIZZA_EVENT_TIME_IN_HOURS_24_HOURS) {
        date = addDays(date, 1);
    }
    return date;
};

export const setPizzaDay = (date: Date | null) => {
    return setTime(selectRandomPizzaDay(date));
};

type _Props = {
    selectedDate: Date | null;
    setSelectedDate: React.Dispatch<React.SetStateAction<Date | null>>;
    name?: string;
};

const _WeekPicker: React.FC<_Props> = ({ selectedDate, setSelectedDate, name }) => {
    useEffect(() => {
        console.log("test", selectedDate)
        onChange(selectedDate);
    }, []);
    const onChange = (newValue: Date | null) => {
        if (newValue === null || selectedDate === null || isSameDay(newValue, selectedDate)) {
            setSelectedDate(newValue);
        } else {
            // `selectRandomPizzaDay` can never return null if the input isnt null
            // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
            const randomDate = selectRandomPizzaDay(newValue)!;
            const time = {
                hours: selectedDate.getHours(),
                minutes: selectedDate.getMinutes(),
                seconds: selectedDate.getSeconds(),
                milliseconds: selectedDate.getMilliseconds(),
            };
            const _newDate = set(randomDate, time);
            setSelectedDate(_newDate);
        }
    };

    const dayClassNameSetter: (date: Date) => string = (date: Date) => {
        if (selectedDate && isSameISOWeek(date, selectedDate)) {
            return 'react-datepicker__day--selected';
        }

        return '' as string;
    };

    return (
        <_DateTimePicker
            selectedDate={selectedDate}
            setSelectedDate={setSelectedDate}
            dayClassNameSetter={dayClassNameSetter}
            onChange={onChange}
            highlightWeek={true}
            name={name}
        />
    );
};

interface Props {
    name: string;
}

const WeekPicker: React.FC<Props> = ({ name }) => {
    const { control } = useFormContext();

    return (
        <Controller
            render={({ field: { ref, onChange, onBlur, value, name }, formState }) => (
                <_WeekPicker selectedDate={value} setSelectedDate={onChange} name={name} />
            )}
            name={name}
            control={control}
        />
    );
};

export default WeekPicker;
