const path = require('path');

module.exports = {
  entry: {
    bootstrap_js: './electron/src/bundle/bootstrap_js.js',
    bootstrap_css: './electron/src/bundle/bootstrap_css.js',
    blog_post_css: './electron/src/bundle/blog_post_css.js',
    fontawesome_css: './electron/src/bundle/fontawesome_css.js'
  },
  output: {
    filename: '[name].bundle.js',
    path: path.resolve(__dirname, 'dist/')
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
      },
      {
        test: /\.(woff(2)?|ttf|eot|svg)(\?v=\d+\.\d+\.\d+)?$/,
        use: [
          {
            loader: 'file-loader',
            options: {
              name: '[name].[ext]',
              outputPath: 'fonts/',
            }
          }
        ]
      }
    ]
  },
  resolve: {
    extensions: ['.js', '.css']
  },
};