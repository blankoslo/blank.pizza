import React from 'react';
import { Paper } from '@mui/material';
import Typography from '@mui/material/Typography';
import { Box } from '@mui/material';
import { useTranslation } from 'react-i18next';
import { UserCard } from './UserCard';
import { InfinityList } from '../../InfinityList';
import { useInfiniteUsers } from '../../../hooks/useUsers';

const UserList: React.FC = () => {
    const { t } = useTranslation();

    const { isLoading, data: _users, hasNextPage, fetchNextPage } = useInfiniteUsers({ page_size: 10 });
    const hasMore = isLoading ? true : hasNextPage ?? false;
    const users = _users?.pages.flatMap((page) => page.data);

    const INFINITY_LIST_ID = 'userInfinityListContainer';

    return (
        <Paper
            sx={(theme) => ({
                height: '100%',
                width: '30vw',
                minWidth: '500px',
                borderRadius: 3,
                backgroundColor: theme.palette.secondary.main,
                display: 'flex',
                flexDirection: 'column',
                overflow: 'auto',
            })}
        >
            <Box
                sx={{
                    fontSize: '1.2rem',
                    fontWeight: 'bold',
                    margin: '24px 24px 12px 24px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                }}
            >
                <Typography variant="h5" component="h3">
                    {t('users.list.title')}
                </Typography>
            </Box>
            <Box
                id={INFINITY_LIST_ID}
                sx={{
                    overflow: 'auto',
                }}
            >
                {users && (
                    <InfinityList
                        parentId={INFINITY_LIST_ID}
                        fetchData={fetchNextPage}
                        hasMore={hasMore}
                        items={users.map((user) => (
                            <UserCard key={user.slack_id} {...user} />
                        ))}
                    />
                )}
                {users && users.length == 0 && (
                    <Box sx={{ display: 'flex', justifyContent: 'center' }}>{t('users.list.noResults')}</Box>
                )}
            </Box>
        </Paper>
    );
};

export { UserList };
