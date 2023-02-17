import * as React from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import { useTranslation } from 'react-i18next';

interface Props {
    open: boolean;
    onDelete: () => void;
    handleClose: () => void;
}

const DialogDeleteEvent: React.FC<Props> = ({ open, onDelete, handleClose }) => {
    const { t } = useTranslation();

    return (
        <Dialog open={open} onClose={handleClose}>
            <DialogTitle>{t('events.delete.confirmation.title')}</DialogTitle>
            <DialogContent>
                <DialogContentText>
                    {t('events.delete.confirmation.content.line1')}
                    <br></br>
                    {t('events.delete.confirmation.content.line2')}
                </DialogContentText>
            </DialogContent>
            <DialogActions>
                <Button autoFocus onClick={handleClose}>
                    {t('events.delete.confirmation.action.cancel')}
                </Button>
                <Button onClick={onDelete}>{t('events.delete.confirmation.action.accept')}</Button>
            </DialogActions>
        </Dialog>
    );
};

export default DialogDeleteEvent;
