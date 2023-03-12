import React, { useState } from 'react';
import { Box } from '@mui/material';
import { NewEventsContainer } from './NewEventsContainer';
import { OldEventsContainer } from './OldEventsContainer';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import { Button3D } from '../../Button3D';
import DialogNewEvent from './DialogNewEvent';
import { useTranslation } from 'react-i18next';
import {TabPanel} from "../../TabPanel";

const EventList: React.FC = () => {
    const [value, setValue] = React.useState(0);

    const handleChange = (event: React.SyntheticEvent, newValue: number) => {
        setValue(newValue);
    };

    const { t } = useTranslation();

    const [showNewModal, setShowNewModal] = useState(false);

    const toggleCreateNewForm = () => {
        setShowNewModal((val) => !val);
    };

    return (
        <Box
            sx={(theme) => ({
                width: '30vw',
                minWidth: '600px',
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'normal',
                [theme.breakpoints.down('md')]: {
                    width: '100%',
                    minWidth: 'unset',
                },
            })}
        >
            <Tabs
                value={value}
                onChange={handleChange}
                textColor="primary"
                indicatorColor="primary"
                aria-label="Event tabs"
                variant="fullWidth"
                sx={(theme) => ({ width: '100%', backgroundColor: theme.palette.secondary.main, marginBottom: 1 })}
            >
                <Tab value={0} label={t('events.list.futureEvents.title')} sx={{ fontWeight: 700 }} />
                <Tab value={1} label={t('events.list.pastEvents.title')} sx={{ fontWeight: 700 }} />
            </Tabs>
            <TabPanel value={value} index={0}>
                <Box sx={{ marginY: 1 }}>
                    <DialogNewEvent open={showNewModal} handleClose={toggleCreateNewForm} />
                    <Button3D text={t('events.list.newEventButton')} onClick={toggleCreateNewForm} />
                </Box>
                <NewEventsContainer />
            </TabPanel>
            <TabPanel value={value} index={1}>
                <OldEventsContainer />
            </TabPanel>
        </Box>
    );
};

export { EventList };
