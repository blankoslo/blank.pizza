import { Box, Card, Typography, Button, Grid } from '@mui/material';
import React, { useEffect } from 'react';
import Logo from '../../../assets/BlankLogoLight5.svg';
import { useTranslation } from 'react-i18next';
import { createLoginURI, getJWT } from '../../../api/AuthService';
import { LoadingSpinner } from '../../LoadingSpinner';
import { useQuery } from '../../../hooks/useQuery';
import { useNavigate } from 'react-router-dom';
import { useStore } from '../../../state/store';
import { loginUser } from '../../../state/reducers';

interface Props {
    callback?: boolean;
}

export const Login: React.FC<Props> = ({ callback = false }) => {
    const { t } = useTranslation();
    const query = useQuery();
    const navigate = useNavigate();
    const [_, dispatch] = useStore();

    useEffect(() => {
        const init = async () => {
            const code = query.get('code');
            const params = Object.fromEntries(query);
            if (callback && code) {
                const user = await getJWT(params);
                dispatch(loginUser(user));
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
        <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
            <Grid
                flex={1}
                sx={(theme) => ({
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    flexDirection: 'column',
                    padding: 2,
                    backgroundColor: theme.palette.primary.main,
                    maxHeight: `100vh`,
                    width: '100%',
                })}
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
                                Login
                            </Button>
                        </Box>
                    </>
                )}
            </Grid>
        </Box>
    );
};
