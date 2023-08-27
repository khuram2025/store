"use strict";

const gulp = require('gulp');
const {
    src,
    dest,
    parallel,
    series,
    watch
} = require('gulp');
const sass = require('gulp-sass')(require('sass'));
const autoprefixer = require('autoprefixer');
const postcss = require('gulp-postcss');
const pug = require('gulp-pug');

// Move JS files to "dist/js" folder
function js() {
    return src([
            'node_modules/jquery/dist/jquery.min.js',
            'node_modules/bootstrap/dist/js/bootstrap.bundle.min.js',
            'node_modules/owl.carousel/dist/owl.carousel.min.js',
            'node_modules/jquery-waypoints/waypoints.min.js',
            'node_modules/counterup/jquery.counterup.min.js',
            'node_modules/jquery.easing/jquery.easing.min.js',
            'node_modules/jquery-countdown/dist/jquery.countdown.min.js',
            'node_modules/magnific-popup/dist/jquery.magnific-popup.min.js',
            'node_modules/jquery-nice-select/js/jquery.nice-select.min.js'
        ])
        .pipe(dest('dist/js'));
}

// Move CSS files to "dist/css" folder
function css() {
    return src([
            'node_modules/wowjs/css/libs/animate.css',
            'node_modules/bootstrap/dist/css/bootstrap.min.css',
            'node_modules/owl.carousel/dist/assets/owl.carousel.min.css',
            'node_modules/magnific-popup/dist/magnific-popup.css',
            'node_modules/jquery-nice-select/css/nice-select.css'
        ])
        .pipe(dest('dist/css'));
}

// Move static CSS files to "dist/css" folder
function staticCSS() {
    return src(['static/css/*', 'static/css/*/*'])
        .pipe(dest('dist/css'));
}

// Move static Images to "dist/img" folder
function staticImage() {
    return src('static/img/*/*')
        .pipe(dest('dist/img'));
}

// Move static JS files to "dist/js" folder
function staticJS() {
    return src('static/js/*')
        .pipe(dest('dist/js'));
}

// Move static Web Fonts files to "dist/webfonts" folder
function staticWebFonts() {
    return src('static/webfonts/*')
        .pipe(dest('dist/webfonts'));
}

// Move static Common files to "dist/" folder
function staticCommon() {
    return src('static/*')
        .pipe(dest('dist'));
}

// SCSS to CSS Convert
function sassToCss() {
    return src('src/scss/*.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(postcss([autoprefixer(['last 4 version'])]))
        .pipe(dest('dist/'))
}

// Pug to HTML Convert
function pugToHtml() {
    return src('src/pug/*.pug')
        .pipe(pug({
            pretty: true
        }))
        .pipe(dest('dist/'));
}

// Watching
function watching() {
    watch('static/css/*', series(staticCSS));
    watch('static/img/*/*', series(staticImage));
    watch('static/js/*', series(staticJS));
    watch('static/*', series(staticCommon));
    watch('src/scss/*.scss', series(sassToCss));
    watch(['src/pug/*.pug', 'src/pug/inc/*.pug'], series(pugToHtml));
}

const watchingAll = parallel(watching);

exports.watch = watchingAll;
exports.default = series(js, css, staticCSS, staticImage, staticJS, staticWebFonts, staticCommon, sassToCss, pugToHtml, watching);