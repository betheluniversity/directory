const path = require('path')
// const UglifyJsPlugin = require("uglifyjs-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
// const OptimizeCSSAssetsPlugin = require("optimize-css-assets-webpack-plugin");

module.exports = (env, argv) => ({
    entry: './app/static/src/js/index.js',
    output: {
        path: path.resolve(__dirname, 'app/static/dist/'),
        filename: 'main.js'
    },
    // optimization: {
    //     minimizer: [
    //         new UglifyJsPlugin({
    //             cache: true,
    //             parallel: true,
    //             sourceMap: true // set to true if you want JS source maps
    //         }),
    //         new OptimizeCSSAssetsPlugin({})
    //     ]
    // },
    // plugins: [
    //     new MiniCssExtractPlugin({
    //         // Options similar to the same options in webpackOptions.output
    //         // both options are optional
    //         filename: argv.mode === 'development' ? '[name].[hash].css' : 'main.css',
    //         // chunkFilename: argv.mode==='development' ? '[id].css' : '[id].[hash].css',
    //     })
    // ],
    // module: {
    //     rules: [{
    //         test: /\.(sa|sc|c)ss$/,
    //         use: [
    //             MiniCssExtractPlugin.loader,
    //             'css-loader',
    //             {
    //                 loader: 'postcss-loader',
    //                 options: {
    //                     plugins: function () { // postcss plugins, can be exported to postcss.config.js
    //                         return [
    //                             require('autoprefixer'),
    //                             require('cssnano')
    //                         ];
    //                     }
    //                 },
    //             },
    //             'sass-loader'
    //         ]
    //     }]
    // }
})