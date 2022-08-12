import { useState } from 'react';
import { TextField} from '@mui/material';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import { LocalizationProvider } from '@mui/x-date-pickers';


function CustomDatePicker() {
    const [value, setValue] = useState<Date | null>(
        new Date('2014-08-18T21:11:54'),
      );
    
      const handleChange = (newValue: Date | null) => {
        setValue(newValue);
      };

    return (
        <LocalizationProvider dateAdapter={AdapterDateFns}>
            <DateTimePicker
            label="Date and Time picker"
            value={value}
            onChange={handleChange}
            renderInput={(params) => <TextField {...params} />}
            />
        </LocalizationProvider>

    );
}

export default CustomDatePicker;
