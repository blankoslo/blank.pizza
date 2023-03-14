import * as React from 'react';
import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import { useTranslation } from 'react-i18next';
import { Box, IconButton } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import { EventEditor } from './EventEditor';
import { ApiRestaurant } from '../../../api/RestaurantService';

interface Props {
    open: boolean;
    handleClose: () => void;
    eventId: string;
    eventTime: Date;
    restaurant?: ApiRestaurant;
}

const DialogEditEvent: React.FC<Props> = ({ open, handleClose, eventId, eventTime, restaurant }) => {
    const { t } = useTranslation();

    return (
        <Dialog open={open} onClose={handleClose} PaperProps={{ style: { overflowY: 'visible', width: '100%', maxWidth: '500px' } }}>
            <DialogTitle>
                <Box display="flex" alignItems="center">
                    <Box flexGrow={1}>{t('events.edit.title')}</Box>
                    <Box>
                        <IconButton onClick={handleClose}>
                            <CloseIcon />
                        </IconButton>
                    </Box>
                </Box>
            </DialogTitle>
            <DialogContent sx={{ overflowY: 'visible' }}>
                <EventEditor
                    eventId={eventId}
                    eventTime={eventTime}
                    restaurant={restaurant}
                    onSubmitFinished={handleClose}
                />
            </DialogContent>
        </Dialog>
    );
};

export default DialogEditEvent;
