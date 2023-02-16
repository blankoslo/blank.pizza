import React from 'react';
import { Box, IconButton } from '@mui/material';
import { RestaurantEntryField } from './RestaurantEntryField';
import { ApiRestaurant } from '../../../api/RestaurantService';
import DeleteIcon from '@mui/icons-material/Delete';
import { useTranslation } from 'react-i18next';
import { Card } from '@mui/material';
import PizzaRating from './PizzaRating';

interface Props {
    restaurant: ApiRestaurant;
    deleteRestaurantButton: (id: string) => void;
}

export const RestaurantEntry: React.FC<Props> = ({
    restaurant: { id, name, link, tlf, address, rating },
    deleteRestaurantButton,
}) => {
    const { t } = useTranslation();

    return (
        <Card
            sx={{
                display: 'flex',
                flexDirection: 'row',
                position: 'relative',
                marginBottom: '20px',
                padding: 3,
                /*'&::before': {
                    content: '""',
                    position: 'absolute',
                    left: 0,
                    bottom: 0,
                    height: '20px',
                    width: '50px',
                    marginBottom: '-10px',
                    borderBottom: '10px solid black',
                },*/
            }}
        >
            <Box
                sx={{
                    flex: 1,
                    display: 'flex',
                    flexDirection: 'column',
                }}
            >
                <RestaurantEntryField label={t('restaurants.list.entry.name')} text={name} />
                <RestaurantEntryField label={t('restaurants.list.entry.link')} text={link} />
                <RestaurantEntryField label={t('restaurants.list.entry.tlf')} text={tlf} />
                <RestaurantEntryField label={t('restaurants.list.entry.address')} text={address} />
            </Box>
            <Box
                sx={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                }}
            >
                <PizzaRating rating={rating} />
            </Box>
            <Box
                sx={{
                    display: 'flex',
                    alignItems: 'center',
                }}
            >
                <IconButton
                    sx={{
                        height: 'fit-content',
                    }}
                    size="large"
                    onClick={() => deleteRestaurantButton(id)}
                >
                    <DeleteIcon fontSize="large" />
                </IconButton>
            </Box>
        </Card>
    );
};
