module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    less: {
      development: {
        options: {
          paths: ["alias_app/static/less",]
        },
        files: {
          "alias_app/static/css/theme.css": "alias_app/static/less/theme.less"
        }
      },
      production: {
        options: {
          paths: ["alias_app/static/less",],
          compress: true
        },
        files: {
          "alias_app/static/css/theme.min.css": "alias_app/static/less/theme.less"
        }
      }
    },
    autoprefixer: {
      css: {
        expand: true,
        flatten: true,
        src: 'alias_app/static/css/theme.css',
        dest: 'alias_app/static/css/'
      }
    },
    concat: {
      development: {
        options: {
          separator: '\n\n',
        },
        dist: {
          src: [
            "alias_app/static/lib/jquery/dist/jquery.js",
            "alias_app/static/lib/bootstrap/js/collapse.js",
            "alias_app/static/js/app/**/*.js"
          ],
          dest: 'alias_app/static/js/app.min.js'
        }
      },
      production: {
        options: {
          separator: '\n\n',
        },
        dist: {
          src: [
            "alias_app/static/lib/jquery/dist/jquery.js",
            "alias_app/static/lib/bootstrap/js/collapse.js",
            "alias_app/static/js/app/**/*.js"
          ],
          dest: 'alias_app/static/js/app.js'
        }
      }
    },
    uglify: {
      js: {
        options: {
          mangle: false
        },
        files: {
          "alias_app/static/js/app.min.js": [
            "alias_app/static/js/app.js"
          ]
        }
      }
    },
    watch: {
      less: {
          files: 'alias_app/static/less/**/*.less',
          tasks: ['less:development', 'autoprefixer']
      },
      js: {
          files: 'alias_app/static/js/app/**/*.js',
          tasks: ['concat:development',]
      },
      livereload: {
        // Here we watch the files the less task will compile to
        // These files are sent to the live reload server after less compiles to them
        options: { livereload: true },
        files: ['alias_app/static/css/*'],
      },
    }
  });

  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-autoprefixer');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-watch');

  // Default task(s).
  grunt.registerTask('default', ['less:development', 'autoprefixer', 'concat:development', 'watch']);
  grunt.registerTask('production', ['less:production', 'autoprefixer', 'concat:production', 'uglify']);
};