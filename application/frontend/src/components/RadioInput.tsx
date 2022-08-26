import { Box, FormControlLabel, Radio, RadioGroup, FormControl, FormLabel } from '@mui/material';
import React from 'react';
import { Controller, useFormContext } from 'react-hook-form';
import { ErrorMessage } from './ErrorMessage';

interface Props {
    name: string;
    label: string;
    items: Array<{
        value: string | number;
        text: string | number;
    }>;
    marginBottom?: boolean;
    marginLeft?: boolean;
    width?: number;
}

const TextInput: React.FC<Props> = ({ name, label, items, marginBottom = true, marginLeft = true, width }) => {
    const { control } = useFormContext();

    return (
        <Box
            sx={{
                marginBottom: marginBottom ? 2 : 0,
                marginLeft: marginLeft ? 2 : 0,
                display: 'flex',
                flexDirection: 'column',
                width: width ? `${width}px` : null,
            }}
        >
            <Controller
                render={({ field }) => (
                    <FormControl>
                        <FormLabel>{label}</FormLabel>
                        <RadioGroup
                            row
                            {...field}
                            onChange={(event: React.ChangeEvent<HTMLInputElement>, value: string) => {
                                field.onChange(value);
                            }}
                        >
                            {items.map((item) => (
                                <FormControlLabel
                                    key={item.value}
                                    value={item.value}
                                    control={<Radio />}
                                    label={item.text}
                                />
                            ))}
                        </RadioGroup>
                    </FormControl>
                )}
                name={name}
                control={control}
            />
            <ErrorMessage name={name} />
        </Box>
    );
};

export default TextInput;
