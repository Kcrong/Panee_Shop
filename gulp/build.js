'use strict';

var gulp = require('gulp');

var $ = require('gulp-load-plugins')();

gulp.task('clean', function () {
  return gulp.src(['./app/templates/index.html'], { read: false }).pipe($.clean());
});

