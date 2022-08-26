import { Box, TextField } from '@mui/material';
import React from 'react';
import { Controller, useFormContext } from 'react-hook-form';
import { ErrorMessage } from './ErrorMessage';

interface Props {
    name: string;
    label?: string;
    triggerNames?: string[];
    marginBottom?: boolean;
    fullWidth?: boolean;
    disabled?: boolean;
    type:
        | 'button'
        | 'checkbox'
        | 'color'
        | 'date'
        | 'datetime-local'
        | 'email'
        | 'file'
        | 'hidden'
        | 'image'
        | 'month'
        | 'number'
        | 'password'
        | 'radio'
        | 'range'
        | 'reset'
        | 'search'
        | 'submit'
        | 'tel'
        | 'text'
        | 'time'
        | 'url'
        | 'week';
    variant?: 'outlined' | 'filled' | 'standard';
    centerText?: boolean;
    min?: number;
    max?: number;
    alwaysShowNumberArrows?: boolean;
}

const TextInput: React.FC<Props> = ({
    name,
    label,
    triggerNames,
    marginBottom = true,
    fullWidth = false,
    disabled = false,
    type,
    variant = 'outlined',
    centerText = false,
    min,
    max,
    alwaysShowNumberArrows = false,
}) => {
    const { control, trigger } = useFormContext();

    return (
        <Box
            sx={{
                marginBottom: marginBottom ? 2 : 0,
                display: 'flex',
                flexDirection: 'column',
                flex: fullWidth ? 1 : null,
            }}
        >
            <Controller
                render={({ field, formState }) => (
                    <TextField
                        fullWidth={fullWidth}
                        label={label}
                        variant={variant}
                        {...field}
                        inputProps={{
                            min: min,
                            max: max,
                            style: centerText
                                ? {
                                      textAlign: 'center',
                                  }
                                : undefined,
                        }}
                        sx={
                            alwaysShowNumberArrows
                                ? {
                                      '& input[type=number]::-webkit-inner-spin-button': {
                                          opacity: 1,
                                      },
                                  }
                                : undefined
                        }
                        onChange={(event) => {
                            const value = event.target.value;
                            field.onChange(value === '' ? undefined : value);
                            // TODO: Temporary fix to handle how yup updates the validation and check of errors
                            if (triggerNames) {
                                trigger([...triggerNames, name]);
                            }
                        }}
                        error={!!formState.errors[name]}
                        disabled={disabled}
                        type={type}
                    />
                )}
                name={name}
                control={control}
            />
            <ErrorMessage name={name} />
        </Box>
    );
};

export default TextInput;
