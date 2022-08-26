import { Box, FormControlLabel, FormGroup, Switch } from '@mui/material';
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
    labelPlacement?: 'bottom' | 'top' | 'end' | 'start';
}

const SwitchInput: React.FC<Props> = ({
    name,
    label,
    marginBottom = true,
    fullWidth = false,
    disabled = false,
    labelPlacement = 'bottom',
}) => {
    const { control } = useFormContext();

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
                render={({ field: { value, onChange, ...rest } }) => (
                    <FormGroup>
                        <FormControlLabel
                            {...rest}
                            sx={{ margin: 0 }}
                            labelPlacement={labelPlacement}
                            disabled={disabled}
                            control={<Switch />}
                            label={label}
                            checked={value}
                            onChange={(_, checked) => {
                                onChange(checked);
                            }}
                        />
                    </FormGroup>
                )}
                name={name}
                control={control}
            />
            <ErrorMessage name={name} />
        </Box>
    );
};

export default SwitchInput;
