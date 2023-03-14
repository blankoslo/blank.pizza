import React from 'react';
import { Box, IconButton, Typography } from '@mui/material';
import { useTranslation } from 'react-i18next';
import LanguageIcon from '@mui/icons-material/Language';

export const LocalizationButton: React.FC = () => {
    const { i18n } = useTranslation();

    const changeLocale = () => {
        i18n.language == 'en' ? i18n.changeLanguage('nb') : i18n.changeLanguage('en');
    };

    return (
        <Box>
            <IconButton
                sx={(theme) => ({
                    height: 'fit-content',
                    color: theme.palette.secondary.main,
                })}
                size="large"
                onClick={changeLocale}
            >
                <LanguageIcon fontSize="large" />
                <Typography sx={{ marginLeft: 0.5, fontSize: { xs: 13, md: '1rem' } }}>
                    {i18n.language == 'en' ? 'English' : 'Norsk'}
                </Typography>
            </IconButton>
        </Box>
    );
};
