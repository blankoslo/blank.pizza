import * as React from 'react';
import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import { useTranslation } from 'react-i18next';
import { RestaurantCreator } from './RestaurantCreator';
import { Box, IconButton } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';

interface Props {
    open: boolean;
    handleClose: () => void;
}

const DialogNew: React.FC<Props> = ({ open, handleClose }) => {
    const { t } = useTranslation();

    return (
        <Dialog open={open} onClose={handleClose} PaperProps={{ style: { width: '100%', maxWidth: '400px' } }}>
            <DialogTitle>
                <Box display="flex" alignItems="center">
                    <Box flexGrow={1}>{t('restaurants.new.title')}</Box>
                    <Box>
                        <IconButton onClick={handleClose}>
                            <CloseIcon />
                        </IconButton>
                    </Box>
                </Box>
            </DialogTitle>
            <DialogContent>
                <RestaurantCreator onSubmitFinished={handleClose} />
            </DialogContent>
        </Dialog>
    );
};

export default DialogNew;
