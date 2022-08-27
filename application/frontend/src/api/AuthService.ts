import { httpClient } from './httpClient';
import { Pagination, Params } from './types';
import { User } from '../state/store';
import jwt_decode from 'jwt-decode';

const endpoint = '/auth/login';

interface Auth {
    auth_url: string;
}

interface AuthJWT {
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

export const createLoginURI = (): Promise<Auth> =>
    httpClient()
        .get<Auth>(endpoint)
        .then((response) => response.data);

export const getJWT = (params: AuthParams): Promise<User> =>
    httpClient()
        .get<AuthJWT>(`${endpoint}/callback`, { params })
        .then((response) => {
            const data = response.data;
            const decodedToken = jwt_decode<Token>(data.access_token);
            const decodedUser = decodedToken.user;
            const user: User = {
                token: data.access_token,
                ...decodedUser,
            };
            return user;
        });
