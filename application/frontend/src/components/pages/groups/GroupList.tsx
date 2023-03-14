import React, { useState } from 'react';
import { Box, Paper, Typography } from '@mui/material';
import { useInfiniteGroups } from '../../../hooks/useGroups';
import { groupsDefaultQueryKey, useGroupService } from '../../../api/GroupService';
import { toast } from 'react-toastify';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { DialogDeleteWarning } from './DialogDeleteWarning';
import { DialogNew } from './DialogNew';
import { GroupEntry } from './GroupEntry';
import { useTranslation } from 'react-i18next';
import { Button3D } from '../../Button3D';
import { InfinityList } from '../../InfinityList';
import Tab from "@mui/material/Tab";
import Tabs from "@mui/material/Tabs";
import { TabPanel } from '../../TabPanel';

export const GroupList: React.FC = () => {
    const { t } = useTranslation();
    const { deleteGroup } = useGroupService();

    const [showNewModal, setShowNewModal] = useState(false);
    const [deleteId, setDeleteId] = useState<string>();
    const { isLoading, data: _groups, hasNextPage, fetchNextPage } = useInfiniteGroups({ page_size: 10 });
    const hasMore = isLoading ? true : hasNextPage ?? false;
    const groups = _groups?.pages.flatMap((page) => page.data);

    const queryClient = useQueryClient();

    const addMutation = useMutation((id: string) => deleteGroup(id), {
        onSuccess: () => {
            toast.success(t('groups.delete.mutation.onSuccess'));
        },
        onError: () => {
            toast.error(t('groups.delete.mutation.onError'));
        },
        onSettled: () => {
            queryClient.invalidateQueries([groupsDefaultQueryKey]);
        },
    });

    const deleteGroupButton = (id: string) => {
        setDeleteId(id);
    };

    const deleteGroupCallback = () => {
        if (deleteId) {
            addMutation.mutate(deleteId);
            setDeleteId(undefined);
        }
    };

    const deleteGroupCancel = () => {
        setDeleteId(undefined);
    };

    const toggleCreateNewForm = () => {
        setShowNewModal((val) => !val);
    };

    const INFINITY_LIST_ID = 'groupInfinityListContainer';

    return (
        <>
            <DialogDeleteWarning open={!!deleteId} handleClose={deleteGroupCancel} onDelete={deleteGroupCallback} />
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
                    <Tab value={0} label={t('groups.list.title')} sx={{ fontWeight: 700 }} />
                </Tabs>
                <TabPanel value={0} index={0}>
                    <Box sx={{ marginY: 1 }}>
                        <Button3D text={t('groups.list.newGroupButton')} onClick={toggleCreateNewForm} />
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
                        {groups && (
                            <InfinityList
                                parentId={INFINITY_LIST_ID}
                                fetchData={() => fetchNextPage()}
                                hasMore={hasMore}
                                showEndMessage={false}
                                items={groups.map((group) => (
                                    <GroupEntry key={group.id} group={group} deleteGroupButton={deleteGroupButton} />
                                ))}
                            />
                        )}
                        {groups && groups.length == 0 && (
                            <Box sx={{ display: 'flex', justifyContent: 'center' }}>{t('groups.list.noResults')}</Box>
                        )}
                    </Box>
                </TabPanel>
            </Box>
        </>
    );
};
