import * as React from 'react';
import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import { useTranslation } from 'react-i18next';
import { Box, IconButton } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import { EventCreator } from './EventCreator';

interface Props {
    open: boolean;
    handleClose: () => void;
}

const DialogNewEvent: React.FC<Props> = ({ open, handleClose }) => {
    const { t } = useTranslation();

    return (
        <Dialog open={open} onClose={handleClose} PaperProps={{ style: { width: '100%', maxWidth: '400px' } }}>
            <DialogTitle>
                <Box display="flex" alignItems="center">
                    <Box flexGrow={1}>{t('events.new.title')}</Box>
                    <Box>
                        <IconButton onClick={handleClose}>
                            <CloseIcon />
                        </IconButton>
                    </Box>
                </Box>
            </DialogTitle>
            <DialogContent>
                <EventCreator onSubmitFinished={handleClose} />
            </DialogContent>
        </Dialog>
    );
};

export default DialogNewEvent;
