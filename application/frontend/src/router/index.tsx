import React, { useEffect, useState } from 'react';
import { Routes, Route, BrowserRouter, Outlet } from 'react-router-dom';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { useStore } from '../state/store';
import Auth from './Auth';

import { Login } from '../components/pages/login';
import { Logout } from '../components/pages/logout';
import NewRestaurantPage from '../components/pages/restaurants/new';
import RestaurantListPage from '../components/pages/restaurants/list';
import EvenListPage from '../components/pages/events/list';
import NewEventPage from '../components/pages/events/new';
import UserListPage from '../components/pages/users/list';

type Props = {
    children?: React.ReactNode;
};

const RouterContainer: React.FC<Props> = ({ children }) => {
    const [isLoading, setIsLoading] = useState(false);
    const [state, dispatch] = useStore();
    //const loggedIn = !!state.user;

    // TODO: Fix loading indicator
    /*useEffect(() => {
        if (loggedIn) {
            setIsLoading(true);
        }
    }, [loggedIn]);*/

    if (isLoading) {
        return <LoadingSpinner />;
    }

    return <>{children}</>;
};

export const Router: React.FC = () => {
    return (
        <BrowserRouter>
            <RouterContainer>
                <Routes>
                    <Route element={<Auth loggedIn={false} />}>
                        <Route path="/login" element={<Login />} />
                        <Route path="/login/callback" element={<Login callback={true} />} />
                    </Route>
                    <Route element={<Auth loggedIn={true} />}>
                        <Route path="/" element={<Outlet />} />
                        <Route path="/restaurants" element={<Outlet />}>
                            <Route path="new" element={<NewRestaurantPage />} />
                            <Route path="list" element={<RestaurantListPage />} />
                        </Route>
                        <Route path="/events" element={<Outlet />}>
                            <Route path="new" element={<NewEventPage />} />
                            <Route path="list" element={<EvenListPage />} />
                        </Route>
                        <Route path="/users" element={<Outlet />}>
                            <Route path="list" element={<UserListPage />} />
                        </Route>
                        <Route path="/logout" element={<Logout />} />
                    </Route>
                </Routes>
            </RouterContainer>
        </BrowserRouter>
    );
};
