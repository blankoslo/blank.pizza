import { Box, Paper, Typography } from '@mui/material';
import * as React from 'react';
import { useTranslation } from 'react-i18next';

const HomePage: React.FC = () => {
    const { t } = useTranslation();

    return (
        <Box
            sx={{
                flex: 1,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                width: '100%',
            }}
        >
            <Paper
                sx={{
                    padding: 2,
                    width: { xs: '100%', md: '800px' },
                    overflow: 'auto',
                }}
            >
                <Typography component="h2" variant="h4">
                    {t('home.faq.title')}
                </Typography>
                <ul>
                    <li>
                        <b>{t('home.faq.question1.question')}</b>
                        <ul>
                            <li>{t('home.faq.question1.answer')}</li>
                            <li>{t('home.faq.question1.answer2')}</li>
                        </ul>
                    </li>
                    <li>
                        <b>{t('home.faq.question2.question')}</b>
                        <ul>
                            <li>{t('home.faq.question2.answer')}</li>
                        </ul>
                    </li>
                    <li>
                        <b>{t('home.faq.question3.question')}</b>
                        <ul>
                            <li>
                                {t('home.faq.question3.answer')}{' '}
                                <a href="https://www.blank.no/">https://www.blank.no/</a>.
                            </li>
                        </ul>
                    </li>
                </ul>
            </Paper>
        </Box>
    );
};
export default HomePage;
