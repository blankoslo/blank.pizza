const HtmlWebpackPlugin = require('html-webpack-plugin');
const { WebpackManifestPlugin } = require('webpack-manifest-plugin');
const path = require('path');
const Dotenv = require('dotenv-webpack');

module.exports = {
    entry: path.resolve(__dirname, 'src', 'index.tsx'),
    resolve: {
        extensions: ['.ts', '.tsx', '.js', '.jsx'],
        alias: {
            '@mui/styled-engine': '@mui/styled-engine-sc',
        },
    },
    module: {
        rules: [
            {
                test: /\.css$/i,
                use: ['style-loader', 'css-loader'],
            },
            {
                test: /\.(png|woff2|woff|eot|ttf|otf)$/,
                loader: 'file-loader',
                options: {
                    publicPath: '/',
                }
            },
            {
                test: /\.svg$/i,
                issuer: /\.[jt]sx?$/,
                use: ['@svgr/webpack'],
            },
        ],
    },
    plugins: [
        new HtmlWebpackPlugin({
            publicPath: '/',
            template: path.resolve(__dirname, 'src', 'index.html'),
            favicon: path.resolve(__dirname, 'src', 'assets', 'favicon.ico'),
        }),
        new WebpackManifestPlugin({
            seed: {
                display: "standalone"
            }
        }),
        new Dotenv({
            systemvars: true
        })
    ],
};
