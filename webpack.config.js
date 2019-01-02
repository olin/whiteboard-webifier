const path = require('path');

const APP_DIR = path.resolve(__dirname, 'src')

module.exports = {
  devtool: 'source-map',
  entry: `${APP_DIR}/index.jsx`,
  output: {
    path: __dirname + '/dist',
    publicPath: '/',
    filename: 'bundle.js'
  },
  devServer: {
    contentBase: './dist'
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: 'babel-loader',
      },
      {
        test: /\.css$/,
        include: APP_DIR,
        loaders: ['style-loader', 'css-loader'],
      },
    ]
  },
  resolve: {
    extensions: ['*', '.js', '.jsx']
  },

};
