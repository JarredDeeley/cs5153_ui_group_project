const webpack = require('webpack');

const config = {
  entry: {
    'bundle': [
      __dirname + '/app/application.js',
    ],
  },
  optimization: {
    splitChunks: {
      chunks: "all",
      cacheGroups: {
        default: false,
        vendors: false,
        vendor: {
          name: "bundle",
          chunks: "all",
          test: /node_modules/,
          priority: 20
        }
      }
    }
  },
  output: {
    filename: "[name].js",
    chunkFilename: "[name]-[chunkhash].js",
    path: __dirname + '/public',
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          'style-loader',
          'css-loader'
        ]
      },
      {
        test: /\.(png|svg|jpg|gif)$/,
        use: [
          'file-loader'
        ]
      }
    ]
  }
};

module.exports = config;
