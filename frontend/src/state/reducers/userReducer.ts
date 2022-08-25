import { User } from '../store';

type UserActions = {
    type: USER_CONSTANTS;
    payload?: User;
};

enum USER_CONSTANTS {
    LOGIN_USER = 'USER_LOGIN_USER',
    LOGOUT_USER = 'USER_LOGOUT_USER',
}

const loginUser: (payload: User) => UserActions = (payload) => ({
    type: USER_CONSTANTS.LOGIN_USER,
    payload,
});

const logoutUser: () => UserActions = () => ({
    type: USER_CONSTANTS.LOGOUT_USER,
    undefined,
});

const userReducer: (state: User, action: UserActions) => User | undefined = (state, action) => {
    switch (action.type) {
        case USER_CONSTANTS.LOGIN_USER: {
            return {
                ...state,
                ...(action.payload ?? {}),
            };
        }
        case USER_CONSTANTS.LOGOUT_USER: {
            return undefined;
        }
    }
};

export { userReducer, UserActions, loginUser, logoutUser };
