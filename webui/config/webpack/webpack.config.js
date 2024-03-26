/* eslint-disable no-undef */
const HtmlWebpackPlugin = require('html-webpack-plugin');
const TsconfigPathsPlugin = require('tsconfig-paths-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CircularDependencyPlugin = require('circular-dependency-plugin');
const {LicenseWebpackPlugin} = require('license-webpack-plugin');

const PATHS = require('../paths.js');

const ACCEPTABLE_LICENSES = ['MIT', 'BSD-2-Clause', 'BSD-3-Clause', 'Apache-2.0', 'Hippocratic-2.1'];

module.exports = function config(env, options) {
    const isDevelopment = options.mode === 'development';
    const localIdentName = isDevelopment ? '[path][name]__[local]' : '[hash:base64]';

    const styleLoader = isDevelopment ? 'style-loader' : MiniCssExtractPlugin.loader;

    const fileLoader = {
        loader: 'file-loader',
        options: {
            outputPath: 'assets',
        },
    };

    const proxy = env.api
        ? {
              '/api': {
                  pathRewrite: {'^/api': ''},
                  changeOrigin: true,
                  target: env.api,
                  secure: false,
              },
          }
        : undefined;
    return {
        entry: './src/index.tsx',
        module: {
            rules: [
                {
                    test: /\.tsx?$/,
                    use: {
                        loader: 'ts-loader',
                        options: {
                            onlyCompileBundledFiles: true,
                        },
                    },
                },
                {
                    test: /\.css$/,
                    use: [styleLoader, 'css-loader'],
                },
                {
                    test: /\.scss$/,
                    use: [
                        styleLoader,
                        {
                            loader: 'css-loader',
                            options: {
                                modules: {
                                    localIdentName,
                                },
                            },
                        },
                        {
                            loader: 'resolve-url-loader',
                            options: {
                                root: PATHS.appSrc,
                            },
                        },
                        {
                            loader: 'sass-loader',
                            options: {
                                sourceMap: true, //needed for resolve-url-loader to operate on paths
                            },
                        },
                    ],
                },
                {
                    test: /\.(png|jpg)$/,
                    use: [fileLoader],
                },
                {
                    test: /\.svg$/,
                    use: {
                        loader: '@svgr/webpack',
                        options: {
                            memo: true,
                            ref: true,
                            svgoConfig: {
                                plugins: [{prefixIds: false}],
                            },
                        },
                    },
                },
                {
                    test: [/\.woff2$/],
                    use: [
                        {
                            loader: 'file-loader',
                            options: {
                                name: 'static/media/[name].[hash:8].[ext]',
                            },
                        },
                    ],
                },
            ],
        },
        resolve: {
            extensions: ['.tsx', '.ts', '.js'],
            plugins: [new TsconfigPathsPlugin({extensions: ['.tsx', '.ts', '.js']})],
        },
        output: {
            filename: 'bundle.js',
            path: PATHS.dist,
            publicPath: '/',
        },
        devServer: {
            historyApiFallback: true,
            proxy,
        },
        devtool: isDevelopment ? 'source-map' : false,
        plugins: [
            new LicenseWebpackPlugin({
                unacceptableLicenseTest: licenseType => !ACCEPTABLE_LICENSES.includes(licenseType),
                excludedPackageTest: packageName => packageName === 'orion-rwc',
                renderLicenses: () => '',
                licenseTextOverrides: {
                    'popper.js': 'MIT',
                    'raf-schd': 'MIT',
                    isarray: 'MIT',
                    gud: 'MIT',
                },
                perChunkOutput: false,
            }),
            new HtmlWebpackPlugin({
                template: './src/index.html',
                favicon: './src/favicon.png',
            }),
            new MiniCssExtractPlugin({
                filename: '[name].[contenthash:8].css',
            }),
            new CircularDependencyPlugin({
                exclude: /node_modules/,
                failOnError: true,
            }),
        ],
    };
};
