import axios, { AxiosInstance } from 'axios';

const baseUrl = process.env.BACKEND_URI ? `${process.env.BACKEND_URI}/api/` : '/api/';

export const httpClient = (token?: string): AxiosInstance => {
    return axios.create({
        baseURL: baseUrl,
        /*headers: {
            Authorization: `Bearer ${token}`,
        },
        withCredentials: true,*/
        responseType: 'json',
    });
};
