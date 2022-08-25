import React from 'react';
import { Box } from '@mui/material';
import { useTranslation } from 'react-i18next';

export const RestaurantEntryField: React.FC<{ label: string; text?: string }> = ({ label, text }) => {
    const { t } = useTranslation();

    return (
        <Box
            sx={{
                marginBottom: 0.5,
            }}
        >
            <b>{`${label}: `}</b>
            <span>{text ?? t('restaurants.list.optionalValue')}</span>
        </Box>
    );
};
