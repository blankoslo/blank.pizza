import { Box, Grid } from '@mui/material';
import React from 'react';
import Header from './Header';
import Footer from './Footer';

type Props = {
    children?: React.ReactNode;
};

export const Template: React.FC<Props> = ({ children }) => {
    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
            <Header />
            <Grid
                flex={1}
                sx={(theme) => ({
                    display: 'flex',
                    padding: 2,
                    backgroundColor: theme.palette.primary.main,
                    maxHeight: `Calc(100vh - ${theme.mixins.toolbar.minHeight}px - ${theme.mixins.footer.minHeight}px)`,
                    [theme.breakpoints.down('md')]: {
                        maxHeight: `Calc(100vh - ${theme.mixins.toolbar.minHeight}px)`,
                    },
                    [theme.breakpoints.up('sm')]: {
                        // eslint-disable-next-line
                        // @ts-expect-error
                        maxHeight: `Calc(100vh - ${theme.mixins.toolbar['@media (min-width:600px)']['minHeight']}px - ${theme.mixins.footer.minHeight}px)`,
                    },
                })}
            >
                {children}
            </Grid>
            <Footer />
        </Box>
    );
};
