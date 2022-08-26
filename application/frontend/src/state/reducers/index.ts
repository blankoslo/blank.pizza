import { State, User } from '../store';
import { UserActions, userReducer } from './userReducer';
export { loginUser, logoutUser } from './userReducer';

type Actions = UserActions;
type UserType = User;
type States = UserType;

interface Reducer<S, A> {
    [index: string]: (state: S, action: A) => S | undefined;
}

const combineReducers =
    <S extends States, A extends Actions>(reducers: Reducer<S, A>) =>
    (state: State, action: A) =>
        Object.keys(reducers).reduce((newState, reducerName) => {
            const subState = newState[reducerName] as S;
            const reducerFunction = reducers[reducerName];
            return {
                ...newState,
                [reducerName]: reducerFunction(subState, action),
            };
        }, state);

const rootReducer = combineReducers({ user: userReducer });

export default rootReducer;

export { Actions };
