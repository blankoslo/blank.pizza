import axios, { AxiosError, AxiosInstance, AxiosRequestConfig, AxiosRequestHeaders, AxiosResponse } from 'axios';
import { useTranslation } from 'react-i18next';
import { toast } from 'react-toastify';
import { logoutUser, refreshUser } from '../state/reducers/userReducer';
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
    const { t } = useTranslation();

    const access_token = state.user?.token;
    const refresh_token = state.user?.refresh_token;

    type httpClientType = <T>(
        url: string,
        data?: any,
        config?: AxiosRequestConfig<any>,
    ) => Promise<AxiosResponse<T, any>>;

    const refreshGuard = async <T>(method: (token?: string) => Promise<AxiosResponse<T, any>>) => {
        // TODO: Handle invalid tokens (f.ex. secret key changed)
        try {
            const promise = method(access_token);
            await promise;
            return promise;
        } catch (error) {
            if (
                axios.isAxiosError(error) &&
                (error as AxiosError<ServerError>).response?.data.msg == 'Token has expired'
            ) {
                try {
                    const res = await httpClient(refresh_token).post<RefreshJWT>('/auth/refresh');
                    const new_access_token = res.data.access_token;
                    dispatch(refreshUser({ token: new_access_token }));
                    return method(new_access_token);
                } catch (error2) {
                    if (
                        axios.isAxiosError(error) &&
                        (error as AxiosError<ServerError>).response?.data.msg == 'Token has expired'
                    ) {
                        toast.warn(t('token.refresh.expired'), { autoClose: 10000 });
                        dispatch(logoutUser());
                    }
                    return Promise.reject(error);
                }
            }
            return Promise.reject(error);
        }
    };

    const httpGetClient: httpClientType = async <T>(url: string, config?: AxiosRequestConfig<any>) => {
        const method = (token?: string) => httpClient(token).get<T>(url, config);
        return refreshGuard<T>(method);
    };

    const httpPostClient: httpClientType = async <T>(
        url: string,
        data: any,
        config: AxiosRequestConfig<any> | undefined,
    ) => {
        const method = (token?: string) => httpClient(token).post<T>(url, data, config);
        return refreshGuard<T>(method);
    };

    const httpPutClient: httpClientType = async <T>(url: string, data?: any, config?: AxiosRequestConfig<any>) => {
        const method = (token?: string) => httpClient(token).put<T>(url, data, config);
        return refreshGuard<T>(method);
    };

    const httpPatchClient: httpClientType = async <T>(url: string, data?: any, config?: AxiosRequestConfig<any>) => {
        const method = (token?: string) => httpClient(token).put<T>(url, data, config);
        return refreshGuard<T>(method);
    };

    const httpDeleteClient: httpClientType = async <T>(url: string, config?: AxiosRequestConfig<any>) => {
        const method = (token?: string) => httpClient(token).delete<T>(url, config);
        return refreshGuard<T>(method);
    };

    return {
        httpGetClient,
        httpPostClient,
        httpPutClient,
        httpPatchClient,
        httpDeleteClient,
    };
};
