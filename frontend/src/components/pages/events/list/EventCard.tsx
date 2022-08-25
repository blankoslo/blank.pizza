import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import { useTranslation } from 'react-i18next';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { ApiEvent } from '../../../../api/EventService';
import { useInvitations } from '../../../../hooks/useInvitations';
import { dateToReadableString } from '../../../utils/dateToReadableString';
import Stack from '@mui/material/Stack';
import { InvitationRow } from './InvitationRow';

const EventCard: React.FC<ApiEvent> = ({ id, time, finalized, restaurant }) => {
    const { t } = useTranslation();

    const { isLoading, data: invitations } = useInvitations(id);

    return (
        <Card
            sx={{
                backgroundColor: 'white',
                marginBottom: 1,
                overflow: 'visible',
            }}
        >
            <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />} aria-controls="panel1a-content" id="panel1a-header">
                    <CardContent>
                        <p>{dateToReadableString(time)}</p>
                        <Typography variant="h5" component="h3">
                            {`${t('events.list.eventCard.normal.place')} ${
                                restaurant ? restaurant.name : t('events.list.deletedRestaurant')
                            }`}
                        </Typography>
                    </CardContent>
                </AccordionSummary>
                <AccordionDetails
                    sx={{
                        paddingX: 0,
                        paddingBottom: 0,
                    }}
                >
                    <Stack>
                        {invitations &&
                            invitations.map((invitation) => (
                                <InvitationRow key={invitation.event_id + invitation.slack_id} {...invitation} />
                            ))}
                    </Stack>
                </AccordionDetails>
            </Accordion>
        </Card>
    );
};

export { EventCard };
