const path = require('path')

module.exports = {
    mode: 'development',
    entry: './app/static/src/js/index.js',
    output: {
        path: path.resolve(__dirname, 'app/static/dist/js'),
        filename: 'main.js'
    }
}