const webpack = require('webpack');

const config = {
  // This is 100% not the best way to do this!!!
  entry: {
    app_js:  __dirname + '/app/assets/application.js',
    app_css:  __dirname + '/app/assets/application.css',
    bootstrap_css: __dirname + '/app/vendor/css/bootstrap.min.css',
    bootstrap_js: __dirname + '/app/vendor/js/bootstrap.min.js',
  },
  output: {
    filename: "[name].js",
    path: __dirname + '/public',
  },
  plugins: [
    // so that file hashes don't change unexpectedly
    new webpack.HashedModuleIdsPlugin(),
  ],
  performance: { hints: false },
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
