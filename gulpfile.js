'use strict';

var fs = require('fs')
  , path = require('path')
  ;

var gulp = require('gulp')
  , env = require('gulp-env')
  , clean = require('gulp-clean')
  , webpack = require('webpack-stream')
  , named = require('vinyl-named')
  ;

var appName = 'aarau';
var assetsDir = path.resolve(__dirname, appName + '/assets/');


// -- [shared tasks]

// loads environment vars from .env
gulp.task('env', function() {
  var dotenv_file = '.env';
  if (fs.existsSync(dotenv_file)) {
    return gulp.src(dotenv_file)
      .pipe(env({file: dotenv_file, type: '.ini'}));
  }
})


// -- [build tasks]

var builder = function(files) {
  // eslint-disable-next-line global-require
  var webpackConfig = require('./webpack.config.js');
  return gulp.src(files.map(function(file) {
    return path.resolve(assetsDir, file)
  }))
    .pipe(named())
    .pipe(webpack(webpackConfig))
    .pipe(gulp.dest(path.resolve(__dirname, 'tmp/builds/')));
}

gulp.task('build:master', gulp.series('env', function() {
  return builder(['master.js']);
}));

gulp.task('build:vendor', gulp.series('env', function() {
  return builder(['vendor.js']);
}));

gulp.task('build:number', gulp.series('env', function() {
  return builder(['number.js']);
}));

gulp.task('build:author', gulp.series('env', function() {
  return builder(['author.js']);
}));

gulp.task('build:reader', gulp.series('env', function() {
  return builder(['reader.js']);
}));

// copy
gulp.task('copy:img', gulp.series('env', function(done) {
  gulp.src(path.resolve(assetsDir, 'img/*.{png,jpg,gif}'))
    .pipe(gulp.dest('static/img'));
  return done();
}));

gulp.task('copy:ico', gulp.series('env', function(done) {
  gulp.src(path.resolve(assetsDir, 'favicon.ico'))
    .pipe(gulp.dest('static/'));
  return done();
}));

gulp.task('copy:txt', gulp.series('env', function(done) {
  gulp.src(path.resolve(assetsDir, '{robots,humans}.txt'))
    .pipe(gulp.dest('static/'));
  return done();
}));

// builds all .js into %(appName)/tmp/builds
// this run webpack each times.
gulp.task('build', gulp.series(
  'build:master'
, 'build:vendor'
, 'build:number'
, 'build:author'
, 'build:reader'
));

// builds all scripts at once with license plugin for production mode
// this run webpack only once.
gulp.task('build:all', gulp.series('env', function() {
  return builder([
    'master.js'
  , 'vendor.js'
  , 'number.js'
  , 'author.js'
  , 'reader.js'
  ]);
}));


// -- [make tasks]

// places assets files from tmp/builds into static/
gulp.task('distribute', function() {
  return gulp.src([
    'tmp/builds/*.js'
  , 'tmp/builds/*.css'
  , 'tmp/builds/*.txt'
  , 'tmp/builds/**/*.{eot,svg,ttf,woff,woff2}'
  , 'tmp/builds/*.json'
  ])
    .pipe(named())
    .pipe(gulp.dest('static/'));
})

// applies changes of application files to static/app.js
gulp.task('build-install:master', function(done) {
  var run = gulp.series('build:master', 'distribute');
  return run(done);
});

gulp.task('build-install:number', function(done) {
  var run = gulp.series('build:number', 'distribute');
  return run(done);
});

gulp.task('build-install:author', function(done) {
  var run = gulp.series('build:author', 'distribute');
  return run(done);
});

gulp.task('build-install:reader', function(done) {
  var run = gulp.series('build:reader', 'distribute');
  return run(done);
});


// -- [development tasks]

gulp.task('clean', function() {
  return gulp.src([
    'tmp/builds/*'
  , 'static/*.js'
  , 'static/*.json'
  , 'static/*.css'
  , 'static/*.txt'
  , 'static/*.csv'
  , 'static/**/*.{eot,svg,ttf,woff,woff2}'
  , 'static/*.ico'
  , 'static/**/*.png'
  ], {
    read: false
  }).pipe(clean());
});

// copies other static files from assets into %(appName)/tmp/builds
gulp.task('copy', gulp.series(
  'copy:img'
, 'copy:ico'
, 'copy:txt'
));

// distribute and copy
gulp.task('install', gulp.series(
  'distribute'
, 'copy'
));

// watches
var paths = {
  master: [
    path.join(assetsDir, 'master.js')
  , path.join(assetsDir, 'css/**/*.styl')
  , path.join('!' + assetsDir, 'css/{console,carrell,registry}/**/*.styl')
  , path.join(assetsDir, 'js/**/*.js')
  , path.join('!' + assetsDir, 'js/{console,carrell,registry}/**/*.js')
  , path.join(assetsDir, 'component/**/*.{style,js}')
  , path.join('!' + assetsDir,
    'component/{console,carrell,registry}/**/*.{style,js}')
  ]
, number: [ // registry
    path.join(assetsDir, 'number.js')
  , path.join(assetsDir, 'css/{shared,registry}/**/*.styl')
  , path.join(assetsDir, 'js/{shared,registry}/**/*.js')
  , path.join(assetsDir, 'component/registry/**/*.{styl,js}')
  ]
, author: [ // console
    path.join(assetsDir, 'author.js')
  , path.join(assetsDir, 'css/{shared,console}/**/*.styl')
  , path.join(assetsDir, 'js/{shared,console}/**/*.js')
  , path.join(assetsDir, 'component/console/**/*.{styl,js}')
  ]
, reader: [ // carrell
    path.join(assetsDir, 'reader.js')
  , path.join(assetsDir, 'css/{shared,carrell}/**/*.styl')
  , path.join(assetsDir, 'js/{shared,carrell}/**/*.js')
  , path.join(assetsDir, 'component/carrell/**/*.{styl,js}')
  ]
, img: [
    path.join(assetsDir, 'img/*')
  ]
};

gulp.task('watch', gulp.series('env', function() {
  gulp.watch('gulpfile.js', gulp.series('default'));
  gulp.watch(paths.master, gulp.series('build-install:master'));
  gulp.watch(paths.number, gulp.series('build-install:number'));
  gulp.watch(paths.author, gulp.series('build-install:author'));
  gulp.watch(paths.reader, gulp.series('build-install:reader'));
  gulp.watch(paths.img, gulp.series('copy'));
}));


// -- [main tasks]

//gulp.hasTask = function(n) { return true; }

gulp.task('default', gulp.series('env', function(done) {
  var nodeEnv = process.env.NODE_ENV || 'production';
  console.log('» gulp:', nodeEnv);

  var build = (nodeEnv === 'production') ? 'build:all' : 'build';
  var run = gulp.series('clean', build, 'install');
  run(done);
}));
