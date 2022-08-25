const path = require('path');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const { merge } = require('webpack-merge')
const common = require('./webpack.common')

module.exports = merge(common, {
    mode: 'production',
    output: {
        path: path.resolve(__dirname, 'public'),
        filename: '[name].[fullhash].bundle.js',
        publicPath: "",
    },
    module: {
        rules: [
            {
                test: /\.ts(x?)$/,
                loader: 'ts-loader',
                exclude: /node_modules/,
            },
        ]
    },
    plugins: [
        new CleanWebpackPlugin()
    ]
});
