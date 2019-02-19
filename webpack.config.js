const webpack = require('webpack');

const config = {
  entry: {
    application: __dirname + '/app/application.js',
    bootstrap_css: __dirname + '/app/vendor/css/bootstrap.min.css',
    bootstrap_js: __dirname + '/app/vendor/js/bootstrap.min.js',
  },
  output: {
    filename: "[name].js",
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
