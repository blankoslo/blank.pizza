import { Box } from '@mui/material';
import * as React from 'react';
import { EventCreator } from './EventCreator';

const NewEventPage: React.FC = () => (
    <Box
        sx={{
            flex: 1,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
        }}
    >
        <EventCreator />
    </Box>
);

export default NewEventPage;
