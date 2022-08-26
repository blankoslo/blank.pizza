import React from 'react';
import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { Template } from '../components/Template';
import { useStore } from '../state/store';

type Props = {
    loggedIn: boolean;
    authenticatedRoles?: Array<string>;
};

const Auth: React.FC<Props> = ({ authenticatedRoles, loggedIn }) => {
    const location = useLocation();

    const [state] = useStore();
    const user = state.user;
    const roles = user?.roles || [];

    // If no roles are given then return true as they thus sould have access in that regard else
    // check if they have one of the required roles
    const roleAccess = authenticatedRoles
        ? authenticatedRoles?.reduce((acc, cur) => roles.findIndex((val) => val === cur) > -1 || acc, false)
        : true;

    if (!(user && roleAccess) && loggedIn) {
        // Redirect them to the /login page, but save the current location they were
        // trying to go to when they were redirected. This allows us to send them
        // along to that page after they login, which is a nicer user experience
        // than dropping them off on the home page.
        return <Navigate to="/login" state={{ from: location }} replace />;
    } else if (!(user && roleAccess) && !loggedIn) {
        return <Outlet />;
    } else if (user && roleAccess && !loggedIn) {
        return <Navigate to="/" state={{ from: location }} replace />;
    } else {
        return (
            <Template>
                <Outlet />
            </Template>
        );
    }
};

export default Auth;
