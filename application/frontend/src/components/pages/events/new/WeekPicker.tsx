import * as React from 'react';
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import startOfWeek from 'date-fns/startOfWeek';
import add from 'date-fns/add';
import { addDays, Locale } from 'date-fns';
import { useTranslation } from 'react-i18next';
import enLocale from 'date-fns/locale/en-US';
import nbLocale from 'date-fns/locale/nb';
import DatePicker, { registerLocale } from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import isSameISOWeek from 'date-fns/isSameISOWeek';
import { set } from 'date-fns';

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

    const newDate = set(date, {
        hours: PIZZA_EVENT_TIME_IN_HOURS_24_HOURS,
        minutes: 0,
        seconds: 0,
        milliseconds: 0,
    });
    return newDate;
};

const selectRandomPizzaDay = (selectedDate: Date | null) => {
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

export const selectPizzaDay = (date: Date | null) => {
    return setTime(selectRandomPizzaDay(date));
};

interface indexable {
    [index: string]: Locale;
}

const localeMap: indexable = {
    en: enLocale,
    nb: nbLocale,
};

const StyledDatePicker = styled(Box)`
    .react-datepicker__day--keyboard-selected {
        background-color: #216ba5;
        border-radius: 0.3rem;
        color: #ffffff;
    }
    .react-datepicker__day--selected {
        background-color: #216ba5;
        border-radius: 0.3rem;
        color: #ffffff;
    }
    .react-datepicker__week:hover {
        .react-datepicker__day:not(.react-datepicker__day--selected) {
            background-color: #7cb7e5;
            border-radius: 0.3rem;
            color: #ffffff;
        }
    }
    .react-datepicker__day--today {
        font-weight: normal;
    }
    .react-datepicker__day--highlighted {
        border-radius: 0.3rem;
        background-color: #103552;
        color: #fff;
    }
    .react-datepicker {
        font-size: 1em;
    }
    .react-datepicker__header {
        padding-top: 0.8em;
    }
    .react-datepicker__month {
        margin: 0.4em 1em;
    }
    .react-datepicker__day-name,
    .react-datepicker__day {
        width: 1.9em;
        line-height: 1.9em;
        margin: 0.166em;
    }
    .react-datepicker__current-month {
        font-size: 1em;
    }
    .react-datepicker__navigation {
        top: 0.7em;
        line-height: 1.7em;
        border: 0.45em solid transparent;
    }
    .react-datepicker__navigation--previous {
        border: none;
    }
    .react-datepicker__navigation--next {
        border: none;
    }
    .react-datepicker__navigation-icon::before {
        width: 15px;
        height: 15px;
    }
`;

type Props = {
    selectedDate: Date | null;
    setSelectedDate: React.Dispatch<React.SetStateAction<Date | null>>;
};

const WeekPicker: React.FC<Props> = ({ selectedDate, setSelectedDate }) => {
    const { i18n } = useTranslation();

    registerLocale(i18n.language, localeMap[i18n.language]);

    return (
        <StyledDatePicker>
            <DatePicker
                selected={selectedDate}
                onChange={(newValue) => {
                    setSelectedDate(selectPizzaDay(newValue));
                }}
                showTimeSelect
                disabledKeyboardNavigation
                dateFormat="MMMM d, yyyy h:mm aa"
                calendarStartDay={1}
                dayClassName={(date: Date) => {
                    if (selectedDate && isSameISOWeek(date, selectedDate)) {
                        return 'react-datepicker__day--selected';
                    }

                    return '';
                }}
                locale={i18n.language}
                highlightDates={selectedDate ? [selectedDate] : undefined}
                inline
                showWeekNumbers
            />
        </StyledDatePicker>
    );
};

export default WeekPicker;
