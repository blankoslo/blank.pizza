import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import { useTranslation } from 'react-i18next';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { ApiEvent } from '../../../api/EventService';
import { useInvitations } from '../../../hooks/useInvitations';
import { datetimeToReadableString } from '../../utils/dateToReadableString';
import Stack from '@mui/material/Stack';
import { InvitationRow } from './InvitationRow';
import { Button3D } from '../../Button3D';
import { Box } from '@mui/material';
import { useState } from 'react';
import DialogEditEvent from './DialogEditEvent';

const EventCard: React.FC<ApiEvent> = ({ id, time, finalized, people_per_event, restaurant, group }) => {
    const { t } = useTranslation();

    const { isLoading, data: invitations } = useInvitations(id);

    const [showEditModal, setShowEditModal] = useState(false);

    const toggleEditForm = () => {
        setShowEditModal((val) => !val);
    };

    return (
        <>
            <DialogEditEvent
                open={showEditModal}
                handleClose={toggleEditForm}
                eventId={id}
                eventTime={new Date(time)}
                restaurant={restaurant}
            />
            <Card
                sx={{
                    backgroundColor: 'white',
                    marginBottom: 1,
                    overflow: 'visible',
                }}
            >
                <Accordion>
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="panel1a-content"
                        id="panel1a-header"
                    >
                        <Box
                            sx={{
                                flex: 1,
                                display: 'flex',
                                justifyContent: 'space-between',
                                alignItems: 'center',
                            }}
                        >
                            <CardContent
                                sx={{
                                    display: 'flex',
                                    flexDirection: 'column',
                                    gap: 1,
                                    padding: 1,
                                }}
                            >
                                <Typography variant="h5" component="h3">
                                    {`${t('events.list.eventCard.normal.place')} ${
                                        restaurant
                                            ? `${restaurant.name} - (${people_per_event} ${t(
                                                  'events.list.eventCard.peoplePerEventEnding',
                                              )})`
                                            : t('events.list.deletedRestaurant')
                                    }`}
                                </Typography>
                                <Typography component="p">{datetimeToReadableString(time)}</Typography>
                                {group && (
                                    <Box
                                        sx={{
                                            display: 'flex',
                                            fontSize: '0.85rem',
                                        }}
                                    >
                                        <span>{`${t('events.list.group')}: ${group.name}`}</span>
                                    </Box>
                                )}
                            </CardContent>
                            {new Date(time) >= new Date() && (
                                <Box
                                    sx={{
                                        marginRight: 1,
                                    }}
                                >
                                    <Button3D
                                        text={t('events.edit.buttons.open')}
                                        stopEventPropagation={true}
                                        onClick={toggleEditForm}
                                    />
                                </Box>
                            )}
                        </Box>
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
                                    <InvitationRow
                                        key={invitation.event_id + invitation.slack_id}
                                        {...invitation}
                                        eventTime={new Date(time)}
                                    />
                                ))}
                        </Stack>
                    </AccordionDetails>
                </Accordion>
            </Card>
        </>
    );
};

export { EventCard };
