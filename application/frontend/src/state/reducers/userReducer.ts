import { User } from '../store';

type UserActions = {
    type: USER_CONSTANTS;
    payload?: User | Pick<User, 'token'>;
};

enum USER_CONSTANTS {
    LOGIN_USER = 'USER_LOGIN_USER',
    REFRESH_USER = 'USER_REFRESH_USER',
    LOGOUT_USER = 'USER_LOGOUT_USER',
}

const loginUser: (payload: User) => UserActions = (payload) => ({
    type: USER_CONSTANTS.LOGIN_USER,
    payload,
});

const refreshUser: (payload: Pick<User, 'token'>) => UserActions = (payload) => ({
    type: USER_CONSTANTS.REFRESH_USER,
    payload,
});

const logoutUser: () => UserActions = () => ({
    type: USER_CONSTANTS.LOGOUT_USER,
    undefined,
});

const userReducer: (state: User, action: UserActions) => User | undefined = (state, action) => {
    switch (action.type) {
        case USER_CONSTANTS.LOGIN_USER: {
            if (action.payload) {
                return {
                    ...state,
                    ...action.payload,
                };
            }
            return state;
        }
        case USER_CONSTANTS.REFRESH_USER: {
            if (action.payload) {
                return {
                    ...state,
                    ...action.payload,
                };
            }
            return state;
        }
        case USER_CONSTANTS.LOGOUT_USER: {
            return undefined;
        }
    }
};

export { userReducer, UserActions, loginUser, refreshUser, logoutUser };
