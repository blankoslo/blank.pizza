import * as React from 'react';
import { Paper } from '@mui/material';
import Typography from '@mui/material/Typography';
import { Box } from '@mui/material';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { Button3D } from '../../../Button3D';

interface Props {
    children: React.ReactNode;
    title: string;
}

const EventsContainer: React.FC<Props> = ({ children, title }) => {
    const navigate = useNavigate();

    const { t } = useTranslation();

    const navigateToNewEvent = () => {
        navigate('/events/new');
    };

    return (
        <Paper
            sx={(theme) => ({
                height: '40%',
                borderRadius: 3,
                backgroundColor: theme.palette.secondary.main,
                display: 'flex',
                flexDirection: 'column',
            })}
        >
            <Box
                sx={{
                    fontSize: '1.2rem',
                    fontWeight: 'bold',
                    margin: '24px 24px 12px 24px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                }}
            >
                <Typography variant="h5" component="h3">
                    {t(title)}
                </Typography>
                <Button3D text={t('events.list.newEventButton')} onClick={navigateToNewEvent} />
            </Box>
            {children}
        </Paper>
    );
};

export { EventsContainer };
