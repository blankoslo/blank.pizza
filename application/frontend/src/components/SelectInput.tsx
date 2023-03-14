import { Box, Select, MenuItem, InputLabel, FormControl } from '@mui/material';
import React from 'react';
import { Controller, useFormContext } from 'react-hook-form';
import { ErrorMessage } from './ErrorMessage';

interface Props {
    name: string;
    label?: string;
    items: Array<{
        value: string | number;
        text: string | number;
    }>;
    marginBottom?: boolean;
    marginLeft?: boolean;
    disabled?: boolean;
    width?: number;
    fullWidth?: boolean;
    fullWidthMobile?: boolean;
    variant?: 'outlined' | 'filled' | 'standard';
}

const TextInput: React.FC<Props> = ({
    name,
    label,
    items,
    marginBottom = true,
    marginLeft = true,
    disabled = false,
    width,
    fullWidth = false,
    fullWidthMobile = false,
    variant = 'outlined',
}) => {
    const { control } = useFormContext();

    let normalWidth = width ? `${width}px` : null;
    if (fullWidth) {
        normalWidth = '100%';
    }
    let mobileWidth = normalWidth;
    if (fullWidthMobile) {
        mobileWidth = '100%';
    }

    return (
        <Box
            sx={{
                marginBottom: marginBottom ? 2 : 0,
                marginLeft: marginLeft ? 2 : 0,
                display: 'flex',
                flexDirection: 'column',
                width: { xs: mobileWidth, md: normalWidth },
            }}
        >
            <Controller
                render={({ field, formState }) => (
                    <FormControl>
                        <InputLabel>{label}</InputLabel>
                        <Select
                            label={label}
                            variant={variant}
                            {...field}
                            error={!!formState.errors[name]}
                            disabled={disabled}
                            fullWidth
                        >
                            {items.map((item) => (
                                <MenuItem key={item.value} value={item.value}>
                                    {item.text}
                                </MenuItem>
                            ))}
                        </Select>
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
