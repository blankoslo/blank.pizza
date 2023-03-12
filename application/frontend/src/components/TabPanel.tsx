import React from 'react';
import { Box } from '@mui/material';

interface Props {
    children?: React.ReactNode;
    index: number;
    value: number;
}

const TabPanel: React.FC<Props> = (props) => {
    const { children, value, index, ...other } = props;

    return (
        <Box
            role="tabpanel"
            hidden={value !== index}
            id={`simple-tabpanel-${index}`}
            aria-labelledby={`simple-tab-${index}`}
            sx={{
                display: 'contents',
            }}
            {...other}
        >
            {value === index && (
                <Box sx={(theme) => ({ display: 'flex', flexDirection: 'column', overflow: 'auto' })}>{children}</Box>
            )}
        </Box>
    );
};

export { TabPanel };
