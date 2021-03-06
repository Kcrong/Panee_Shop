var gulp = require('gulp');
var $ = require('gulp-load-plugins')();
var bowerFiles = require('main-bower-files');

var path = "app/client/";
var config = {
    ngsrc: [path + "*.js", path + "config/**/*.js", path + "services/**/*.js", path + "components/**/*.js", path + "controllers/**/*.js"],
    ngbundle: path + "min"
};


gulp.task('index-lib', function () {
    gulp.src('./app/templates/sample.html')
        .pipe($.inject(gulp.src(bowerFiles({
            path: {
                bowerDirectory: 'lib',
                bowerrc: './.bowerrc',
                bowerJson: './bower.json'
            }
        }), {read: false, 'ignorePath': 'app/', addRootSlash: false}), {name: 'bower', 'ignorePath': path, addRootSlash: false}))
        .pipe($.inject(gulp.src(config.ngsrc, {read: false }), {name: 'ng', 'ignorePath': path, addRootSlash: false}))
        .pipe($.rename({
            basename: 'index'
        }))
        .pipe(gulp.dest('./app/templates'));
});