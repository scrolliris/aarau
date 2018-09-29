module.exports = (config) => {
  let preprocessors = {};
  preprocessors['test/assets/conftest.js'] = ['webpack'];
  preprocessors['test/assets/**/*_test.js'] = ['webpack'];

  config.set({
    basePath: ''
  , autoWatch: true
  , frameworks: ['qunit']
  , files: [
      'test/assets/js/**/*_test.js'
    ]
  , preprocessors: preprocessors
  , webpack: {
      module: {
        loaders: [{
          test: /\.js$/
        , loader: 'babel-loader'
        }]
      }
    }
  , browserConsoleLogOptions: {
      level: 'error'
    , format: '%b %T: %m'
    , terminal: true
    }
  , logLevel: config.LOG_INFO
  , reporters: [
      'progress'
    ]
  , colors: true
  , port: 9876
  , browsers: ['FirefoxHeadless']
  , singleRun: true
  , concurrency: Infinity
  })
}
