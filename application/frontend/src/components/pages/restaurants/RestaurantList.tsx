import React, { useState } from 'react';
import { Box, Paper, Typography } from '@mui/material';
import { useInfiniteRestaurants } from '../../../hooks/useRestaurants';
import { restaurantsDefaultQueryKey, useRestaurantService } from '../../../api/RestaurantService';
import { toast } from 'react-toastify';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { eventsDefaultQueryKey } from '../../../api/EventService';
import DialogDeleteWarning from './DialogDeleteWarning';
import DialogNew from './DialogNew';
import { RestaurantEntry } from './RestaurantEntry';
import { useTranslation } from 'react-i18next';
import { Button3D } from '../../Button3D';
import { InfinityList } from '../../InfinityList';
import Tab from '@mui/material/Tab';
import Tabs from '@mui/material/Tabs';
import { TabPanel } from '../../TabPanel';

export const RestaurantList: React.FC = () => {
    const { t } = useTranslation();
    const { deleteRestaurant } = useRestaurantService();

    const [showNewModal, setShowNewModal] = useState(false);
    const [deleteId, setDeleteId] = useState<string>();
    const { isLoading, data: _restaurants, hasNextPage, fetchNextPage } = useInfiniteRestaurants({ page_size: 10 });
    const hasMore = isLoading ? true : hasNextPage ?? false;
    const restaurants = _restaurants?.pages.flatMap((page) => page.data);

    const queryClient = useQueryClient();

    const addMutation = useMutation((id: string) => deleteRestaurant(id), {
        onSuccess: () => {
            toast.success(t('restaurants.delete.mutation.onSuccess'));
        },
        onError: () => {
            toast.error(t('restaurants.delete.mutation.onError'));
        },
        onSettled: () => {
            queryClient.invalidateQueries([restaurantsDefaultQueryKey]);
            queryClient.invalidateQueries([eventsDefaultQueryKey]);
        },
    });

    const deleteRestaurantButton = (id: string) => {
        setDeleteId(id);
    };

    const deleteRestaurantCallback = () => {
        if (deleteId) {
            addMutation.mutate(deleteId);
            setDeleteId(undefined);
        }
    };

    const deleteRestaurantCancel = () => {
        setDeleteId(undefined);
    };

    const toggleCreateNewForm = () => {
        setShowNewModal((val) => !val);
    };

    const INFINITY_LIST_ID = 'restaurantInfinityListContainer';

    return (
        <>
            <DialogDeleteWarning
                open={!!deleteId}
                handleClose={deleteRestaurantCancel}
                onDelete={deleteRestaurantCallback}
            />
            <DialogNew open={showNewModal} handleClose={toggleCreateNewForm} />
            <Box
                sx={(theme) => ({
                    height: '100%',
                    width: '30vw',
                    minWidth: '600px',
                    display: 'flex',
                    flexDirection: 'column',
                    [theme.breakpoints.down('md')]: {
                        width: '100%',
                        minWidth: 'unset',
                    },
                })}
            >
                <Tabs
                    value={0}
                    textColor="primary"
                    indicatorColor="primary"
                    aria-label="Event tabs"
                    variant="fullWidth"
                    sx={(theme) => ({ width: '100%', backgroundColor: theme.palette.secondary.main, marginBottom: 1 })}
                >
                    <Tab value={0} label={t('restaurants.list.title')} sx={{ fontWeight: 700 }} />
                </Tabs>
                <TabPanel value={0} index={0}>
                    <Box sx={{ marginY: 1 }}>
                        <Button3D text={t('restaurants.list.newRestaurantButton')} onClick={toggleCreateNewForm} />
                    </Box>
                    <Box
                        sx={{
                            overflow: 'auto',
                            display: 'flex',
                            flexDirection: 'column',
                            flex: 1,
                        }}
                        id={INFINITY_LIST_ID}
                    >
                        {restaurants && (
                            <InfinityList
                                parentId={INFINITY_LIST_ID}
                                fetchData={() => fetchNextPage()}
                                hasMore={hasMore}
                                showEndMessage={false}
                                items={restaurants.map((restaurant) => (
                                    <RestaurantEntry
                                        key={restaurant.id}
                                        restaurant={restaurant}
                                        deleteRestaurantButton={deleteRestaurantButton}
                                    />
                                ))}
                            />
                        )}
                        {restaurants && restaurants.length == 0 && (
                            <Box sx={{ display: 'flex', justifyContent: 'center' }}>
                                {t('restaurants.list.noResults')}
                            </Box>
                        )}
                    </Box>
                </TabPanel>
            </Box>
        </>
    );
};
