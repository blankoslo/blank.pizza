import { Box, Typography } from '@mui/material';
import React, { useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useStore } from '../../../state/store';
import { logoutUser } from '../../../state/reducers';

export const Logout: React.FC = () => {
    const { t } = useTranslation();
    const [_, dispatch] = useStore();

    useEffect(() => {
        dispatch(logoutUser());
    }, []);

    return (
        <Box
            sx={{
                flex: 1,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
            }}
        >
            <Typography
                variant="h4"
                component="span"
                align="center"
                sx={(theme) => ({
                    color: theme.palette.secondary.main,
                    fontFamily: '"Respira"',
                    fontStyle: 'normal',
                    fontWeight: 400,
                })}
            >
                {t('logout')}
            </Typography>
        </Box>
    );
};
