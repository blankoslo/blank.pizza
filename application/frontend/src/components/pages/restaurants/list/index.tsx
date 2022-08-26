import { Box } from '@mui/material';
import * as React from 'react';
import { RestaurantList } from '../list/RestaurantList';

const RestaurantListPage: React.FC = () => (
    <Box
        sx={{
            flex: 1,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
        }}
    >
        <RestaurantList />
    </Box>
);

export default RestaurantListPage;
