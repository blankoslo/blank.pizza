import React from 'react';
import { Box } from '@mui/material';
import { EventCard } from './EventCard';
import { InfinityList } from '../../InfinityList';
import { useInfiniteEvents } from '../../../hooks/useEvents';
import { useTranslation } from 'react-i18next';

const OldEventsContainer: React.FC = () => {
    const { t } = useTranslation();

    const INFINITY_LIST_ID = 'oldEventsInfinityListContainer';

    const {
        isLoading,
        data: _events,
        hasNextPage,
        fetchNextPage,
    } = useInfiniteEvents({
        page_size: 10,
        age: 'Old',
        order: 'Desc',
    });
    const hasMore = isLoading ? true : hasNextPage ?? false;
    const events = _events?.pages.flatMap((page) => page.data);

    return (
        <Box
            id={INFINITY_LIST_ID}
            sx={{
                overflow: 'auto',
                display: 'flex',
                flexDirection: 'column',
                flex: 1,
            }}
        >
            {events && (
                <InfinityList
                    parentId={INFINITY_LIST_ID}
                    fetchData={fetchNextPage}
                    hasMore={hasMore}
                    showEndMessage={false}
                    items={events.map((event) => (
                        <EventCard {...event} key={event.id} />
                    ))}
                />
            )}
            {events && events.length == 0 && (
                <Box sx={{ display: 'flex', justifyContent: 'center' }}>{t('events.list.noResults')}</Box>
            )}
        </Box>
    );
};

export { OldEventsContainer };
