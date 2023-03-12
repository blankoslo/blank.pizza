import * as React from 'react';
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import { Locale } from 'date-fns';
import { useTranslation } from 'react-i18next';
import enLocale from 'date-fns/locale/en-US';
import nbLocale from 'date-fns/locale/nb';
import DatePicker, { registerLocale } from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import isSameISOWeek from 'date-fns/isSameISOWeek';
import { Controller, useFormContext } from 'react-hook-form';

interface indexable {
    [index: string]: Locale;
}

const localeMap: indexable = {
    en: enLocale,
    nb: nbLocale,
};

interface StyledProps {
    highlightWeek?: boolean;
}

const StyledDatePicker = styled(Box, {
    shouldForwardProp: (prop) => prop !== 'highlightWeek',
    name: 'MyStyledDatePicker',
    slot: 'Root',
})<StyledProps>(
    ({ theme, highlightWeek }) => `
    width: max-content;
    
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
    ${
        highlightWeek &&
        `
        .react-datepicker__week:hover {
            .react-datepicker__day:not(.react-datepicker__day--selected) {
                background-color: #7cb7e5;
                border-radius: 0.3rem;
                color: #ffffff;
            }
        }
        `
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
`,
);

type _Props = {
    name?: string;
    selectedDate: Date | null;
    setSelectedDate: React.Dispatch<React.SetStateAction<Date | null>>;
    dayClassNameSetter?: (date: Date) => string;
    onChange: (date: Date) => void;
    onBlur?: (event: React.FocusEvent<HTMLInputElement, Element>) => void;
    highlightWeek?: boolean;
};

const _DateTimePicker: React.FC<_Props> = ({
    name,
    selectedDate,
    dayClassNameSetter,
    onChange,
    onBlur,
    highlightWeek,
}) => {
    const { i18n } = useTranslation();

    registerLocale(i18n.language, localeMap[i18n.language]);

    return (
        <StyledDatePicker highlightWeek={highlightWeek}>
            <DatePicker
                name={name}
                selected={selectedDate}
                onChange={onChange}
                onBlur={onBlur}
                showTimeSelect
                disabledKeyboardNavigation
                dateFormat="MMMM d, yyyy h:mm aa"
                calendarStartDay={1}
                dayClassName={dayClassNameSetter}
                locale={i18n.language}
                highlightDates={selectedDate ? [selectedDate] : undefined}
                inline
                showWeekNumbers
            />
        </StyledDatePicker>
    );
};

export { _DateTimePicker };

type Props = {
    name: string;
};

const DateTimePicker: React.FC<Props> = ({ name }) => {
    const { control, trigger } = useFormContext();

    return (
        <Controller
            render={({ field: { ref, onChange, onBlur, value, name }, formState }) => (
                <_DateTimePicker
                    selectedDate={value}
                    setSelectedDate={onChange}
                    onChange={onChange}
                    onBlur={onBlur}
                    name={name}
                />
            )}
            name={name}
            control={control}
        />
    );
};

export default DateTimePicker;
