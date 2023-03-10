import { useHttpClient } from '../api/httpClient';

const installEndpoint = '/slack/install';
const callbackEndpoint = '/slack/callback';

interface SlackResponse {
    redirect_url: string;
}

const useSlackInstall = () => {
    const { httpGetClient, httpPostClient } = useHttpClient();

    const createInstallURI = (): Promise<SlackResponse> =>
        httpGetClient<SlackResponse>(installEndpoint).then((response) => response.data);

    const installApp = (token: string) =>
        httpPostClient<number>(callbackEndpoint, { code: token })
            .then((response) => response.status)
            .catch((reason) => reason.response.status);

    return {
        createInstallURI,
        installApp,
    };
};

export { useSlackInstall };
