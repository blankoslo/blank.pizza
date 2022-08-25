import axios, { AxiosInstance } from 'axios';

export const httpClient = (token?: string): AxiosInstance => {
    return axios.create({
        baseURL: '/api/',
        /*headers: {
            Authorization: `Bearer ${token}`,
        },
        withCredentials: true,*/
        responseType: 'json',
    });
};
