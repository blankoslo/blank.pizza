import * as React from 'react';
import { Paper } from '@mui/material';
import Typography from '@mui/material/Typography';
import { Box } from '@mui/material';
import { useTranslation } from 'react-i18next';
import { Button3D } from '../../Button3D';
import DialogNewEvent from './DialogNewEvent';
import { useState } from 'react';

interface Props {
    children: React.ReactNode;
    title: string;
    showNewButton?: boolean;
}

const EventsContainer: React.FC<Props> = ({ children, title, showNewButton = false }) => {
    const { t } = useTranslation();

    const [showNewModal, setShowNewModal] = useState(false);

    const toggleCreateNewForm = () => {
        setShowNewModal((val) => !val);
    };

    return (
        <>
            <DialogNewEvent open={showNewModal} handleClose={toggleCreateNewForm} />
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
                    {showNewButton && <Button3D text={t('events.list.newEventButton')} onClick={toggleCreateNewForm} />}
                </Box>
                {children}
            </Paper>
        </>
    );
};

export { EventsContainer };
