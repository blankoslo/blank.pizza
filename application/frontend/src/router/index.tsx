import React, { useEffect, useState } from 'react';
import { Routes, Route, BrowserRouter, Outlet } from 'react-router-dom';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { useStore } from '../state/store';
import Auth from './Auth';

import { Login } from '../components/pages/login';
import { Install } from '../components/pages/slack/install';
import { Logout } from '../components/pages/logout';
import RestaurantPage from '../components/pages/restaurants';
import EventPage from '../components/pages/events';
import UsersPage from '../components/pages/users';
import ImagesPage from '../components/pages/images';
import GroupsPage from '../components/pages/groups';
import { Callback } from '../components/pages/slack/callback';
import HomePage from '../components/pages/home';

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
                        <Route path="/slack/install" element={<Install />} />
                        <Route path="/slack/callback/" element={<Callback />} />
                    </Route>
                    <Route element={<Auth loggedIn={true} />}>
                        <Route path="/" element={<HomePage />} />
                        <Route path="/restaurants" element={<RestaurantPage />} />
                        <Route path="/events" element={<EventPage />} />
                        <Route path="/users" element={<UsersPage />} />
                        <Route path="/images" element={<ImagesPage />} />
                        <Route path="/logout" element={<Logout />} />
                        <Route path="/groups" element={<GroupsPage />} />
                    </Route>
                </Routes>
            </RouterContainer>
        </BrowserRouter>
    );
};
