module.exports = {
    entry: '**ENTER ENTRY FILENAME**',
    module: {
        rules: [
        {
            test: /\.ts$/,
            use: 'ts-loader'
        },
        ],
    },
    resolve: {
        extensions: ['.ts', '.js'],
    },
    output: {
        filename: 'test.js'
    },
    mode: "development",
};