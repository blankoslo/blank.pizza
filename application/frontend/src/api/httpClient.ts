import axios, { AxiosInstance, AxiosRequestHeaders } from 'axios';

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
