import * as React from 'react';
import { styled } from '@mui/material/styles';
import TextField from '@mui/material/TextField';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { StaticDatePicker } from '@mui/x-date-pickers/StaticDatePicker';
import { PickersDay, PickersDayProps } from '@mui/x-date-pickers/PickersDay';
import endOfWeek from 'date-fns/endOfWeek';
import isSameDay from 'date-fns/isSameDay';
import isWithinInterval from 'date-fns/isWithinInterval';
import startOfWeek from 'date-fns/startOfWeek';
import add from 'date-fns/add';
import { addDays, Locale } from 'date-fns';
import { useTranslation } from 'react-i18next';
import enLocale from 'date-fns/locale/en-US';
import nbLocale from 'date-fns/locale/nb';

export const PIZZA_EVENT_TIME_IN_HOURS_24_HOURS = 18;

type CustomPickerDayProps = PickersDayProps<Date> & {
    dayIsBetween: boolean;
    isFirstDay: boolean;
    isLastDay: boolean;
    isSelectedDay: boolean;
};

export const getRandomInteger = (min = 2, max = 5) => {
    /** Selects number in range [x,y) */
    // const min = 2; //tuesday
    // const max = 5; //friday
    return Math.random() * (max - min) + min;
};

interface indexable {
    [index: string]: Locale;
}

const localeMap: indexable = {
    en: enLocale,
    nb: nbLocale,
};

const CustomPickersDay = styled(PickersDay, {
    shouldForwardProp: (prop) =>
        prop !== 'dayIsBetween' && prop !== 'isFirstDay' && prop !== 'isLastDay' && prop !== 'isSelectedDay',
})<CustomPickerDayProps>(({ theme, dayIsBetween, isFirstDay, isLastDay, isSelectedDay }) => ({
    ...(dayIsBetween && {
        borderRadius: 0,
        backgroundColor: '#272d2a',
        color: '#fffcb6',
        '&:hover': {
            backgroundColor: theme.palette.primary.dark,
        },
        '&:focus': {
            backgroundColor: '#272d2a',
        },
    }),
    ...(isFirstDay && {
        borderTopLeftRadius: '50%',
        borderBottomLeftRadius: '50%',
    }),
    ...(isLastDay && {
        borderTopRightRadius: '50%',
        borderBottomRightRadius: '50%',
    }),
    ...(isSelectedDay && {
        borderRadius: 0,
        backgroundColor: '#fffcb6',
        color: '#272d2a',
    }),
})) as React.ComponentType<CustomPickerDayProps>;

type CalendarProps = {
    value: Date | null;
    setSelectedDate: React.Dispatch<React.SetStateAction<Date | null>>;
};

const WeekPicker: React.FC<CalendarProps> = ({ value, setSelectedDate }) => {
    const { t, i18n } = useTranslation();

    const renderWeekPickerDay = (
        date: Date,
        selectedDates: Array<Date | null>,
        pickersDayProps: PickersDayProps<Date>,
    ) => {
        if (!value) {
            return <PickersDay {...pickersDayProps} />;
        }

        const start = startOfWeek(value);
        const end = endOfWeek(value);

        const dayIsBetween = isWithinInterval(date, { start, end });
        const isFirstDay = isSameDay(date, start);
        const isLastDay = isSameDay(date, end);
        const isSelectedDay = isSameDay(date, value);

        return (
            <CustomPickersDay
                {...pickersDayProps}
                disableMargin
                dayIsBetween={dayIsBetween}
                isFirstDay={isFirstDay}
                isLastDay={isLastDay}
                isSelectedDay={isSelectedDay}
            />
        );
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

    return (
        <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={localeMap[i18n.language]}>
            <StaticDatePicker
                minDate={getMinDate()}
                displayStaticWrapperAs="desktop"
                label={t('events.new.datePicker.label')}
                value={value}
                onChange={(newValue) => {
                    setSelectedDate(selectRandomPizzaDay(newValue));
                }}
                renderDay={renderWeekPickerDay}
                renderInput={(params) => <TextField {...params} />}
                inputFormat={t('events.new.datePicker.inputFormat')}
            />
        </LocalizationProvider>
    );
};

export default WeekPicker;
