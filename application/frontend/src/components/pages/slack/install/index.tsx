import { Box, Typography, Button, Grid } from '@mui/material';
import React, { useEffect } from 'react';
import Logo from '../../../../assets/BlankLogoLight5.svg';
import { useTranslation } from 'react-i18next';
import { LoadingSpinner } from '../../../LoadingSpinner';
import { LocalizationButton } from '../../../LocalizationButton';
import { useSlackInstall } from '../../../../hooks/useSlackInstall';

interface Props {
    callback?: boolean;
}

export const Install: React.FC<Props> = ({ callback = false }) => {
    const { t } = useTranslation();
    const { createInstallURI } = useSlackInstall();

    const onClickInstall = async () => {
        const res = await createInstallURI();
        window.location.replace(res.redirect_url);
    };

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
                {callback ? (
                    <LoadingSpinner />
                ) : (
                    <>
                        <Box
                            sx={{
                                marginBottom: 2,
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
                                {t('login.logo')}
                            </Typography>
                            <Logo />
                        </Box>
                        <Box
                            sx={{
                                width: '300px',
                                height: '200px',
                                display: 'flex',
                                justifyContent: 'center',
                                alignItems: 'center',
                            }}
                        >
                            <Button
                                size="large"
                                variant="contained"
                                color="secondary"
                                sx={{
                                    fontFamily: '"Respira"',
                                    fontStyle: 'normal',
                                    fontWeight: 400,
                                    width: 200,
                                    height: 80,
                                    fontSize: 24,
                                }}
                                onClick={onClickInstall}
                            >
                                {t('install.button')}
                            </Button>
                        </Box>
                    </>
                )}
            </Grid>
        </Box>
    );
};
