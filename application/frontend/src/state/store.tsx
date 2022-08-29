import React, { useContext, useReducer, useEffect } from 'react';
import rootReducer, { Actions } from './reducers';
import store from 'store';

interface Indexable {
    [key: string]: User | undefined;
}

export interface User {
    id: string;
    email: string;
    picture: string;
    name: string;
    token: string;
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

const initializer: (initialState: State) => State = (initialValue = initialState) => {
    return (store.get('state') as State | null) || initialValue;
};

export const StoreProvider: React.FC<Props> = ({ children, initState }) => {
    const [globalState, dispatch] = useReducer(rootReducer, initState, initializer);

    useEffect(() => {
        store.set('state', globalState);
    }, [globalState]);

    return <Store.Provider value={[globalState, dispatch]}>{children}</Store.Provider>;
};
