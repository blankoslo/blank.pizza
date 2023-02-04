import React from 'react';
import { Router } from './router';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.min.css';
import { initialState, StoreProvider } from './state/store';
import { CssBaseline, ThemeProvider } from '@mui/material';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import theme from './theme';
import HttpsRedirect from 'react-https-redirect';

const queryClient = new QueryClient();

export const App: React.FC = () => {
    return (
        <HttpsRedirect>
            <LocalizationProvider dateAdapter={AdapterDateFns}>
                <ThemeProvider theme={theme}>
                    <QueryClientProvider client={queryClient}>
                        <StoreProvider initState={initialState}>
                            <Router />
                            <ToastContainer
                                position="top-center"
                                autoClose={5000}
                                hideProgressBar={false}
                                newestOnTop
                                closeOnClick
                                rtl={false}
                                pauseOnFocusLoss
                                draggable
                                pauseOnHover
                            />
                            <CssBaseline />
                        </StoreProvider>
                    </QueryClientProvider>
                </ThemeProvider>
            </LocalizationProvider>
        </HttpsRedirect>
    );
};

export default App;
