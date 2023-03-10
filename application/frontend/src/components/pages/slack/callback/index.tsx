import { Box, Grid } from '@mui/material';
import React, { useEffect, useRef } from 'react';
import { LoadingSpinner } from '../../../LoadingSpinner';
import { LocalizationButton } from '../../../LocalizationButton';
import { useQuery } from '../../../../hooks/useQuery';
import { useSlackInstall } from '../../../../hooks/useSlackInstall';
import { toast } from 'react-toastify';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

export const Callback: React.FC = () => {
    const { t } = useTranslation();
    const query = useQuery();
    const navigate = useNavigate();
    const { installApp } = useSlackInstall();
    const hasInstalled = useRef(false);

    useEffect(() => {
        const init = async () => {
            const code = query.get('code');
            if (code) {
                const status = await installApp(code);
                if (status == 200) {
                    toast.success(t('install.successAlert'));
                    navigate('/login');
                } else if (status == 501) {
                    toast.error(t('install.enterpriseInstallAlert'));
                    navigate('/login');
                } else {
                    toast.error(t('install.genericErrorAlert'));
                    navigate('/login');
                }
            }
        };

        if (!hasInstalled.current) {
            hasInstalled.current = true;
            init();
        }
    }, []);

    return (
        <Box
            sx={(theme) => ({
                display: 'flex',
                flexDirection: 'column',
                minHeight: '100vh',
                backgroundColor: theme.palette.primary.main,
            })}
        >
            <Box
                sx={{
                    display: 'flex',
                    justifyContent: 'end',
                }}
            >
                <LocalizationButton />
            </Box>
            <Grid
                flex={1}
                sx={{
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    flexDirection: 'column',
                    padding: 2,
                    maxHeight: `100vh`,
                    width: '100%',
                }}
            >
                <LoadingSpinner />
            </Grid>
        </Box>
    );
};
