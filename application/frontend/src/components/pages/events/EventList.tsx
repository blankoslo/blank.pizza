import React from 'react';
import { Box } from '@mui/material';
import { NewEventsContainer } from './NewEventsContainer';
import { OldEventsContainer } from './OldEventsContainer';
import { EventsContainer } from './EventsContainer';

const EventList: React.FC = () => (
    <Box
        sx={{
            width: '30vw',
            minWidth: '600px',
            height: '100%',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-around',
        }}
    >
        <EventsContainer title="events.list.futureEvents.title" showNewButton={true}>
            <NewEventsContainer />
        </EventsContainer>
        <EventsContainer title="events.list.pastEvents.title">
            <OldEventsContainer />
        </EventsContainer>
    </Box>
);

export { EventList };
