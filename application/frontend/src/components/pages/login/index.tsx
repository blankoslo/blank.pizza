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
                        navigate('/login');
                    } else if (error.response?.status == 401) {
                        toast.error(t('login.error.401'));
                        navigate('/login');
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
                            <div
                                onClick={onClickLogin}
                                style={{
                                    cursor: 'pointer',
                                    alignItems: 'center',
                                    color: '#000',
                                    backgroundColor: '#fff',
                                    border: '1px solid #ddd',
                                    borderRadius: '4px',
                                    display: 'inline-flex',
                                    fontFamily: 'Lato, sans-serif',
                                    fontSize: '16px',
                                    fontWeight: 600,
                                    height: '48px',
                                    justifyContent: 'center',
                                    textDecoration: 'none',
                                    width: '256px',
                                }}
                            >
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    style={{ height: '20px', width: '20px', marginRight: '12px' }}
                                    viewBox="0 0 122.8 122.8"
                                >
                                    <path
                                        d="M25.8 77.6c0 7.1-5.8 12.9-12.9 12.9S0 84.7 0 77.6s5.8-12.9 12.9-12.9h12.9v12.9zm6.5 0c0-7.1 5.8-12.9 12.9-12.9s12.9 5.8 12.9 12.9v32.3c0 7.1-5.8 12.9-12.9 12.9s-12.9-5.8-12.9-12.9V77.6z"
                                        fill="#e01e5a"
                                    ></path>
                                    <path
                                        d="M45.2 25.8c-7.1 0-12.9-5.8-12.9-12.9S38.1 0 45.2 0s12.9 5.8 12.9 12.9v12.9H45.2zm0 6.5c7.1 0 12.9 5.8 12.9 12.9s-5.8 12.9-12.9 12.9H12.9C5.8 58.1 0 52.3 0 45.2s5.8-12.9 12.9-12.9h32.3z"
                                        fill="#36c5f0"
                                    ></path>
                                    <path
                                        d="M97 45.2c0-7.1 5.8-12.9 12.9-12.9s12.9 5.8 12.9 12.9-5.8 12.9-12.9 12.9H97V45.2zm-6.5 0c0 7.1-5.8 12.9-12.9 12.9s-12.9-5.8-12.9-12.9V12.9C64.7 5.8 70.5 0 77.6 0s12.9 5.8 12.9 12.9v32.3z"
                                        fill="#2eb67d"
                                    ></path>
                                    <path
                                        d="M77.6 97c7.1 0 12.9 5.8 12.9 12.9s-5.8 12.9-12.9 12.9-12.9-5.8-12.9-12.9V97h12.9zm0-6.5c-7.1 0-12.9-5.8-12.9-12.9s5.8-12.9 12.9-12.9h32.3c7.1 0 12.9 5.8 12.9 12.9s-5.8 12.9-12.9 12.9H77.6z"
                                        fill="#ecb22e"
                                    ></path>
                                </svg>
                                {t('login.loginButton')}
                            </div>
                            <Button
                                size="large"
                                variant="contained"
                                color="secondary"
                                sx={{
                                    fontStyle: 'normal',
                                    fontWeight: 600,
                                    fontSize: '16px',
                                    padding: 1.5,
                                    width: '256px',
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
