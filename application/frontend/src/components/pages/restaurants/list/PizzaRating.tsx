import { Box, Rating, styled, Typography } from '@mui/material';
import * as React from 'react';
import LocalPizzaIcon from '@mui/icons-material/LocalPizza';
import LocalPizzaOutlinedIcon from '@mui/icons-material/LocalPizzaOutlined';
import { useTranslation } from 'react-i18next';

const StyledRating = styled(Rating)`
  '& .MuiRating-iconFilled': {
    color: '#ff6d75',
  },
  '& .MuiRating-iconHover': {
    color: '#ff3d47',
  },
`;

interface Props {
    rating?: number;
}

const PizzaRating: React.FC<Props> = ({ rating }) => {
    const { t } = useTranslation();

    return (
        <Box
            sx={{
                flex: 1,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
            }}
        >
            {rating ? (
                <StyledRating
                    defaultValue={rating}
                    precision={0.1}
                    icon={<LocalPizzaIcon fontSize="inherit" />}
                    emptyIcon={<LocalPizzaOutlinedIcon fontSize="inherit" />}
                    readOnly
                />
            ) : (
                <Typography>{t('restaurants.list.rating')}</Typography>
            )}
        </Box>
    );
};

export default PizzaRating;
