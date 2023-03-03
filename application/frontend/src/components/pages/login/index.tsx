import { Box, Typography, Button, Grid } from '@mui/material';
import React, {useEffect, useRef} from 'react';
import Logo from '../../../assets/BlankLogoLight5.svg';
import { useTranslation } from 'react-i18next';
import { useAuthService } from '../../../api/AuthService';
import { LoadingSpinner } from '../../LoadingSpinner';
import { useQuery } from '../../../hooks/useQuery';
import { useNavigate } from 'react-router-dom';
import { LocalizationButton } from '../../LocalizationButton';
import { toast } from 'react-toastify';
import {AxiosError} from "axios";

interface Props {
    callback?: boolean;
}

export const Login: React.FC<Props> = ({ callback = false }) => {
    const { t } = useTranslation();
    const query = useQuery();
    const navigate = useNavigate();
    const { loginUser, createLoginURI } = useAuthService();
    const hasInstalled = useRef(false);

    useEffect(() => {
        const init = async () => {
            const code = query.get('code');
            const params = Object.fromEntries(query);
            if (callback && code) {
                try {
                    await loginUser(params);
                } catch (e) {
                    const error = e as AxiosError;
                    if (error.response?.status == 403) {
                        toast.error(t('login.error.403'));
                    } else if (error.response?.status == 401) {
                        toast.error(t('login.error.401'));
                    }
                }
            } else if (callback && !code) {
                navigate('/login');
            }
        };
        if (!hasInstalled.current) {
            hasInstalled.current = true;
            init();
        }
    }, [query]);

    const onClickLogin = async () => {
        const res = await createLoginURI();
        window.location.replace(res.auth_url);
    };

    const onClickInstall = async () => {
        navigate('/slack/install');
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
                                width: '400px',
                                height: '200px',
                                display: 'flex',
                                flexDirection: 'column',
                                gap: 1,
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
                                    fontSize: 24,
                                    padding: 2,
                                }}
                                onClick={onClickLogin}
                            >
                                {t('login.loginButton')}
                            </Button>
                            <Button
                                size="large"
                                variant="contained"
                                color="secondary"
                                sx={{
                                    fontFamily: '"Respira"',
                                    fontStyle: 'normal',
                                    fontWeight: 400,
                                    fontSize: 24,
                                    padding: 2,
                                }}
                                onClick={onClickInstall}
                            >
                                {t('login.installButton')}
                            </Button>
                        </Box>
                    </>
                )}
            </Grid>
        </Box>
    );
};
