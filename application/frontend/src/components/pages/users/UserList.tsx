import React from 'react';
import { Paper } from '@mui/material';
import Typography from '@mui/material/Typography';
import { Box } from '@mui/material';
import { useTranslation } from 'react-i18next';
import { UserCard } from './UserCard';
import { InfinityList } from '../../InfinityList';
import { useInfiniteUsers } from '../../../hooks/useUsers';
import Tab from "@mui/material/Tab";
import Tabs from "@mui/material/Tabs";
import {TabPanel} from "../../TabPanel";

const UserList: React.FC = () => {
    const { t } = useTranslation();

    const { isLoading, data: _users, hasNextPage, fetchNextPage } = useInfiniteUsers({ page_size: 10 });
    const hasMore = isLoading ? true : hasNextPage ?? false;
    const users = _users?.pages.flatMap((page) => page.data);

    const INFINITY_LIST_ID = 'userInfinityListContainer';

    return (
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
                <Tab value={0} label={t('users.list.title')} sx={{ fontWeight: 700 }} />
            </Tabs>
            <TabPanel value={0} index={0}>
                <Box
                    id={INFINITY_LIST_ID}
                    sx={{
                        overflow: 'auto',
                        display: 'flex',
                        flexDirection: 'column',
                        flex: 1,
                    }}
                >
                    {users && (
                        <InfinityList
                            parentId={INFINITY_LIST_ID}
                            fetchData={fetchNextPage}
                            hasMore={hasMore}
                            showEndMessage={false}
                            items={users.map((user) => (
                                <UserCard key={user.slack_id} {...user} />
                            ))}
                        />
                    )}
                    {users && users.length == 0 && (
                        <Box sx={{ display: 'flex', justifyContent: 'center' }}>{t('users.list.noResults')}</Box>
                    )}
                </Box>
            </TabPanel>
        </Box>
    );
};

export { UserList };
