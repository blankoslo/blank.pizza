import { Box } from '@mui/material';
import * as React from 'react';
import { RestaurantList } from './RestaurantList';

const RestaurantPage: React.FC = () => (
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

export default RestaurantPage;
