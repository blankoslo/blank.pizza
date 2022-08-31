import { Box, Card, Typography, Button, Grid } from '@mui/material';
import React, { useEffect } from 'react';
import Logo from '../../../assets/BlankLogoLight5.svg';
import { useTranslation } from 'react-i18next';
import { useAuthService } from '../../../api/AuthService';
import { LoadingSpinner } from '../../LoadingSpinner';
import { useQuery } from '../../../hooks/useQuery';
import { useNavigate } from 'react-router-dom';
import { LocalizationButton } from '../../LocalizationButton';

interface Props {
    callback?: boolean;
}

export const Login: React.FC<Props> = ({ callback = false }) => {
    const { t } = useTranslation();
    const query = useQuery();
    const navigate = useNavigate();
    const { loginUser, createLoginURI } = useAuthService();

    useEffect(() => {
        const init = async () => {
            const code = query.get('code');
            const params = Object.fromEntries(query);
            if (callback && code) {
                await loginUser(params);
            } else if (callback && !code) {
                navigate('/login');
            }
        };
        init();
    }, [query]);

    const onClickLogin = async () => {
        const res = await createLoginURI();
        window.location.replace(res.auth_url);
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
                                onClick={onClickLogin}
                            >
                                {t('login.button')}
                            </Button>
                        </Box>
                    </>
                )}
            </Grid>
        </Box>
    );
};
