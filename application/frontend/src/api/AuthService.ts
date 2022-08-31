import { useHttpClient } from './httpClient';
import { loginUser as dispatchLoginUser } from '../state/reducers';
import { User, useStore } from '../state/store';
import jwt_decode from 'jwt-decode';

const endpoint = '/auth/login';

interface Auth {
    auth_url: string;
}

export interface AuthJWT {
    access_token: string;
    refresh_token: string;
}

export interface RefreshJWT {
    access_token: string;
}

interface Token {
    fresh: string;
    iat: string;
    jti: string;
    type: string;
    sub: string;
    nbf: string;
    exp: string;
    user: {
        email: string;
        picture: string;
        id: string;
        name: string;
        roles: Array<string>;
    };
}

interface AuthParams {
    [index: string]: string;
}

export const useAuthService = () => {
    const { httpGetClient } = useHttpClient();
    const [_, dispatch] = useStore();

    const createLoginURI = (): Promise<Auth> => httpGetClient<Auth>(endpoint).then((response) => response.data);

    const getJWT = (params: AuthParams): Promise<User> =>
        httpGetClient<AuthJWT>(`${endpoint}/callback`, { params }).then((response) => {
            const data = response.data;
            const decodedToken = jwt_decode<Token>(data.access_token);
            const decodedUser = decodedToken.user;
            const user: User = {
                token: data.access_token,
                refresh_token: data.refresh_token,
                ...decodedUser,
            };
            return user;
        });

    const loginUser = async (params: { [k: string]: string }) => {
        const user = await getJWT(params);
        dispatch(dispatchLoginUser(user));
    };

    return {
        createLoginURI,
        getJWT,
        loginUser,
    };
};
