'use strict';

var path = require('path')
  , webpack = require('webpack')
  , ExtractTextPlugin = require('extract-text-webpack-plugin')
  , ManifestPlugin = require('webpack-manifest-plugin')
  ;

var nodeEnv = process.env.NODE_ENV || 'production';
console.log('» webpack:', nodeEnv);

var filename = '[name]';
if (nodeEnv === 'production') {
  filename += '.[contenthash]';
}
var stylusBundler = new ExtractTextPlugin(filename + '.css')
  ;

var appName = 'aarau'
  ;

var config = {
  output: {
    path: path.resolve(__dirname, 'tmp/builds/')
  , filename: (nodeEnv === 'production' ?
      '[name].[chunkhash].js' : '[name].js')
  }
, module: {
    loaders: [{
      test: /\.css$/
    , loader: stylusBundler.extract(['css'])
    }, {
      test: /\.styl$/
    , loader: stylusBundler.extract(['css', 'stylus'])
    , include: [
        path.resolve(__dirname, appName + '/assets')
      ]
    }, {
      test: /\.json$/
    , loader: 'json-loader'
    }, {
      test: /\.js$/
    , loader: 'babel-loader'
    , include: [
        path.resolve(__dirname, appName + '/assets')
      , path.resolve(__dirname, 'node_modules/vergil/dst')
      , path.resolve(__dirname, 'node_modules/inferno-tree-select/dst')
      ]
    }]
  }
, resolve: {
    extensions: ['', '.css', '.js']
  , alias: {
      'crossfilter.js': 'crossfilter2/index.js'
    , 'd3.js': 'd3/dist/d3.min.js'
    , 'inferno.js': 'inferno/dist/inferno.min.js'
    , 'inferno-hyperscript.js':
       'inferno-hyperscript/dist/inferno-hyperscript.min.js'
    , 'inferno-tree-select.js': 'inferno-tree-select/dst/index.min.js'
    , 'i18next.js': 'i18next/i18next.min.js'
    , 'i18next-xhr-backend.js': 'i18next-xhr-backend/i18nextXHRBackend.min.js'
    , 'i18next-browser-languagedetector.js':
       'i18next-browser-languagedetector/i18nextBrowserLanguageDetector.min.js'
    , 'vergil.js': 'vergil/dst/index.min.js'
    , 'moment\.js$': 'moment/min/moment.min.js'
    , 'moment-locale-en-gb\.js$': 'moment/locale/en-gb.js'
    , 'styr\.css$': 'styr/dst/styr.min.css'
    }
  }
, plugins: (function() {
    var _plugins = [
      stylusBundler
    ];
    _plugins.push(
      new webpack.EnvironmentPlugin([
       'NODE_ENV'
      ])
    );
    _plugins.push(
      new webpack.DefinePlugin({
        'process.env.NODE_ENV': JSON.stringify(nodeEnv)
      })
    );
    _plugins.push(
      new webpack.ProvidePlugin({
        'window.moment': 'moment\.js'
      })
    );
    if (nodeEnv === 'production') {
      _plugins.push(
        new ManifestPlugin({
          fileName: 'manifest.json'
        })
      );
      _plugins.push(
        new webpack.optimize.UglifyJsPlugin({
          debug: false
        , minimize: true
        , compress: {
            warnings: false
          }
        , output: {
            comments: false
          }
        })
      );
    }
    return _plugins;
  })()
};

module.exports = config;
