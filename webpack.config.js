const webpack = require('webpack');
const nodeEnv = process.env.NODE_ENV !== 'production' ? 'development' : 'production';

const config = {
  mode: nodeEnv,
  // This is 100% not the best way to do this!!!
  entry: {
    app_js:  __dirname + '/app/assets/js/application.js',
    app_css:  __dirname + '/app/assets/css/application.css',
    bootstrap_css: __dirname + '/app/vendor/css/bootstrap.min.css',
    bootstrap_js: __dirname + '/app/vendor/js/bootstrap.min.js',
    watch_js: __dirname + '/app/assets/js/watch.js',
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
        test: /\.html$/,
        use: [
          "raw-loader"
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
