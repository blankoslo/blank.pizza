import React, { useContext } from 'react';
import rootReducer, { Actions } from './reducers';

interface Indexable {
    [key: string]: User | undefined;
}

export interface User {
    uid: string;
    token: unknown;
    roles: Array<string>;
}

export interface State extends Indexable {
    user?: User;
}

export const initialState: State = { user: undefined };

const Store = React.createContext<[State, React.Dispatch<Actions>]>([initialState, () => null]);
Store.displayName = 'Store';

export const useStore: () => [State, React.Dispatch<Actions>] = () => {
    return useContext(Store);
};

type Props = {
    children?: React.ReactNode;
    initState: State;
};

export const StoreProvider: React.FC<Props> = ({ children, initState }) => {
    const [globalState, dispatch] = React.useReducer(rootReducer, initState);

    return <Store.Provider value={[globalState, dispatch]}>{children}</Store.Provider>;
};
