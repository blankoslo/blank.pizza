import axios, { AxiosError, AxiosInstance, AxiosRequestConfig, AxiosRequestHeaders, AxiosResponse } from 'axios';
import { refreshUser } from '../state/reducers/userReducer';
import { useStore } from '../state/store';
import { RefreshJWT } from './AuthService';

const baseUrl = process.env.BACKEND_URI ? `${process.env.BACKEND_URI.replace(/\/+$/, '')}/api` : '/api';

export const httpClient = (token?: string): AxiosInstance => {
    const headers: AxiosRequestHeaders = {};

    if (token) {
        headers.Authorization = `Bearer ${token}`;
    }

    return axios.create({
        baseURL: baseUrl,
        headers: headers,
        withCredentials: true,
        responseType: 'json',
    });
};

type ServerError = { msg: string };

export const useHttpClient = () => {
    const [state, dispatch] = useStore();

    const access_token = state.user?.token;
    const refresh_token = state.user?.refresh_token;

    // TODO: Handle invalid tokens (f.ex. secret key changed)
    // TODO: Try to make the http[method]Client functions more DRY
    type httpClientType = <T>(
        url: string,
        data?: any,
        config?: AxiosRequestConfig<any>,
    ) => Promise<AxiosResponse<T, any>>;

    const httpGetClient: httpClientType = async <T>(url: string, config?: AxiosRequestConfig<any>) => {
        try {
            const promise = httpClient(access_token).get<T>(url, config);
            await promise;
            return promise;
        } catch (error) {
            if (
                axios.isAxiosError(error) &&
                (error as AxiosError<ServerError>).response?.data.msg == 'Token has expired'
            ) {
                // TODO: Handle refresh token being expired (maybe log them out with a warning about what happened?)
                const res = await httpClient(refresh_token).post<RefreshJWT>('/auth/refresh');
                const new_access_token = res.data.access_token;
                dispatch(refreshUser({ token: new_access_token }));
                return httpClient(new_access_token).get<T>(url, config);
            }
            return Promise.reject(error);
        }
    };

    const httpPostClient: httpClientType = async <T>(
        url: string,
        data: any,
        config: AxiosRequestConfig<any> | undefined,
    ) => {
        try {
            const promise = httpClient(access_token).post<T>(url, data, config);
            await promise;
            return promise;
        } catch (error) {
            if (
                axios.isAxiosError(error) &&
                (error as AxiosError<ServerError>).response?.data.msg == 'Token has expired'
            ) {
                // TODO: Handle refresh token being expired (maybe log them out with a warning about what happened?)
                const res = await httpClient(refresh_token).post<RefreshJWT>('/auth/refresh');
                const new_access_token = res.data.access_token;
                dispatch(refreshUser({ token: new_access_token }));
                return httpClient(new_access_token).post<T>(url, data, config);
            }
            return Promise.reject(error);
        }
    };

    const httpPutClient: httpClientType = async <T>(url: string, data?: any, config?: AxiosRequestConfig<any>) => {
        try {
            const promise = httpClient(access_token).put<T>(url, data, config);
            await promise;
            return promise;
        } catch (error) {
            if (
                axios.isAxiosError(error) &&
                (error as AxiosError<ServerError>).response?.data.msg == 'Token has expired'
            ) {
                // TODO: Handle refresh token being expired (maybe log them out with a warning about what happened?)
                const res = await httpClient(refresh_token).post<RefreshJWT>('/auth/refresh');
                const new_access_token = res.data.access_token;
                dispatch(refreshUser({ token: new_access_token }));
                return httpClient(new_access_token).put<T>(url, data, config);
            }
            return Promise.reject(error);
        }
    };

    const httpPatchClient: httpClientType = async <T>(url: string, data?: any, config?: AxiosRequestConfig<any>) => {
        try {
            const promise = httpClient(access_token).put<T>(url, data, config);
            await promise;
            return promise;
        } catch (error) {
            if (
                axios.isAxiosError(error) &&
                (error as AxiosError<ServerError>).response?.data.msg == 'Token has expired'
            ) {
                // TODO: Handle refresh token being expired (maybe log them out with a warning about what happened?)
                const res = await httpClient(refresh_token).patch<RefreshJWT>('/auth/refresh');
                const new_access_token = res.data.access_token;
                dispatch(refreshUser({ token: new_access_token }));
                return httpClient(new_access_token).put<T>(url, data, config);
            }
            return Promise.reject(error);
        }
    };

    const httpDeleteClient: httpClientType = async <T>(url: string, config?: AxiosRequestConfig<any>) => {
        try {
            const promise = httpClient(access_token).delete<T>(url, config);
            await promise;
            return promise;
        } catch (error) {
            if (
                axios.isAxiosError(error) &&
                (error as AxiosError<ServerError>).response?.data.msg == 'Token has expired'
            ) {
                // TODO: Handle refresh token being expired (maybe log them out with a warning about what happened?)
                const res = await httpClient(refresh_token).patch<RefreshJWT>('/auth/refresh');
                const new_access_token = res.data.access_token;
                dispatch(refreshUser({ token: new_access_token }));
                return httpClient(new_access_token).delete<T>(url, config);
            }
            return Promise.reject(error);
        }
    };

    return {
        httpGetClient,
        httpPostClient,
        httpPutClient,
        httpPatchClient,
        httpDeleteClient,
    };
};
