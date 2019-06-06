const path = require('path')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')

module.exports = {
    entry: './app/static/src/js/index.js',
    output: {
        path: path.resolve(__dirname, 'app/static/dist/'),
        filename: 'main.js'
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: '[name].css',
            chunkFilename: '[id].css'
        })
    ],
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                loader: 'babel-loader'
            },
            {
                test: /bootstrap\.native/,
                use: {
                    loader: 'bootstrap.native-loader',
                    options: {
                        only: ['collapse']
                    }
                }
            },
            {
                test: /\.(css|scss)$/,
                use: [{
                    loader: MiniCssExtractPlugin.loader
                },
                {
                    loader: 'css-loader'
                }, {
                    loader: 'postcss-loader',
                    options: {
                        plugins: function () {
                            return [
                                require('precss'),
                                require('autoprefixer'),
                                require('cssnano')
                            ]
                        }
                    }
                }, {
                    loader: 'sass-loader'
                }
                ]
            }]
    }
}
