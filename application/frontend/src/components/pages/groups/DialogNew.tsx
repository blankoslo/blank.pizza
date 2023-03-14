import * as React from 'react';
import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import { useTranslation } from 'react-i18next';
import { Box, IconButton } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import { GroupForm } from './GroupForm';

interface Props {
    open: boolean;
    handleClose: () => void;
}

const DialogNew: React.FC<Props> = ({ open, handleClose }) => {
    const { t } = useTranslation();

    return (
        <Dialog
            open={open}
            onClose={handleClose}
            fullWidth
            maxWidth="xs"
            PaperProps={{ style: { overflowY: 'visible', width: '100%', maxWidth: '400px' } }}
        >
            <DialogTitle>
                <Box display="flex" alignItems="center">
                    <Box flexGrow={1}>{t('groups.new.title')}</Box>
                    <Box>
                        <IconButton onClick={handleClose}>
                            <CloseIcon />
                        </IconButton>
                    </Box>
                </Box>
            </DialogTitle>
            <DialogContent sx={{ overflowY: 'visible' }}>
                <GroupForm onSubmitFinished={handleClose} />
            </DialogContent>
        </Dialog>
    );
};

export { DialogNew };
