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
    selectedDate: Date | null;
    setSelectedDate: React.Dispatch<React.SetStateAction<Date | null>>;
    dayClassNameSetter?: (date: Date) => string;
    onChange: (date: Date) => void;
    highlightWeek?: boolean;
};

const _DateTimePicker: React.FC<_Props> = ({ selectedDate, dayClassNameSetter, onChange, highlightWeek }) => {
    const { i18n } = useTranslation();

    registerLocale(i18n.language, localeMap[i18n.language]);

    return (
        <StyledDatePicker highlightWeek={highlightWeek}>
            <DatePicker
                selected={selectedDate}
                onChange={onChange}
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
    selectedDate: Date | null;
    setSelectedDate: React.Dispatch<React.SetStateAction<Date | null>>;
};

const DateTimePicker: React.FC<Props> = ({ selectedDate, setSelectedDate }) => {
    const onChange = (newValue: Date | null) => {
        setSelectedDate(newValue);
    };

    return <_DateTimePicker selectedDate={selectedDate} setSelectedDate={setSelectedDate} onChange={onChange} />;
};

export default DateTimePicker;
