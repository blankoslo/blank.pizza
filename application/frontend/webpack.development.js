const path = require('path');
const { merge } = require('webpack-merge')
const common = require('./webpack.common')

const createStyledComponentsTransformer = require('typescript-plugin-styled-components').default;
const styledComponentsTransformer = createStyledComponentsTransformer();

const host = process.env.HOST || '0.0.0.0';
const port = process.env.PORT || '3000';
const sockHost = process.env.WDS_SOCKET_HOST || '0.0.0.0';
const sockPath = process.env.WDS_SOCKET_PATH || '/ws';
const sockPort = process.env.WDS_SOCKET_PORT || port;


module.exports = merge(common, {
    mode: 'development',
    devtool: 'inline-source-map',
    output: {
        path: path.resolve(__dirname, 'public'),
        filename: '[name].bundle.js',
        publicPath: "/",
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                enforce: 'pre',
                loader: 'source-map-loader',
            },
            {
                test: /\.ts(x?)$/,
                loader: 'ts-loader',
                exclude: /node_modules/,
                options: {
                    getCustomTransformers: () => ({before: [styledComponentsTransformer]}),
                },
            },
        ]
    },
    devServer: {
        host: host,
        port: port,
        open: false,
        historyApiFallback: true,
        allowedHosts: "all",
        client: {
            webSocketURL: {
              // Enable custom sockjs pathname for websocket connection to hot reloading server.
              // Enable custom sockjs hostname, pathname and port for websocket connection
              // to hot reloading server.
              hostname: sockHost,
              pathname: sockPath,
              port: sockPort,
            },
            overlay: {
              errors: true,
              warnings: false,
            },
        },
    },
    ignoreWarnings: [/Failed to parse source map/],
});
