var path = require("path");
var webpack = require("webpack");
var BundleTracker = require("webpack-bundle-tracker");

module.exports = {
  context: __dirname,

  entry: "./web/js/index",

  output: {
      path: path.resolve("./assets/"),
      filename: "[name].js",
  },

  plugins: [
    new BundleTracker({filename: "./webpack-stats.json"}),
    new webpack.NoEmitOnErrorsPlugin(),
  ],

  module: {
    loaders: [
      { test: /\.jsx?$/, exclude: /node_modules/, loader: "babel-loader"},
    ],
  },

  resolve: {
    modules: ["node_modules"],
    extensions: [".js", ".jsx"]
  },
};
