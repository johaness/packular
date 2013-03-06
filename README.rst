packular
========

Packular reads lists of required JavaScript, CSS, and partial HTML files,
and downloads/combines/references them in index.html files for use in
development and production.

packular.conf
=============

When no command line options are given, packular will try to read 
``packular.conf`` in the current directory. Use ``packular -C config_file`` to 
provide another filename. 

Sample config file::

    [DEFAULT]
    # default options apply to all ``target:`` blocks

    # you may define a version ID and interpolate it into values below
    version = 9c2a5d2096dbb
    # (actually you can define any number of such variables)

    # source template for index.html
    template = index-template.html

    # download external files into these directories
    download_remote = true
    dir_js = lib
    dir_css = lib

    # prefix for all URLs inserted into index.html
    prefix_js = ./app/
    prefix_css = ./app/

    [angular]
    # combine list of partials below into template cache file
    template_cache = template-cache.js

    # empty cache for development
    template_empty = no-template-cache.js

    [target:dev]

    # index.html generated for this target
    index = index-development.html

    [target:test]
    index = index-test.html

    [target:prod]
    index = index-production.html

    # combine all JS/CSS sources into one file
    combine_js = production.js
    combine_css = production.css

    # overwrite some of the defaults
    prefix_js = http://cdn.example.org/static/%(version)s/js/
    prefix_css = http://cdn.example.org/static/%(version)s/js/

    [javascript]

    # included in all index.html
    test.js

    # include in development index.html only
    no-template-cache.js = dev

    # include in production and testing index.html only
    template-cache.js = prod,test

    # include in test index.html only
    mocks.js = test

    # detected as remote source. downloaded for development,
    # but included as-is for production
    //ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js

    [css]
    test.css

    [partial]
    test.html


Command line options can only create one target::

    Options:
      -h, --help            show this help message and exit
      -C CONF_FILE, --config=CONF_FILE
                            Packular configuration file
      --index-template=INDEX_TMPL
                            Input template file for index.html
      --index-dev=INDEX_DEV
                            Output index.html for development
      --index-prod=INDEX_PROD
                            Output index.html for production
      --outdir_js=OUTDIR_JS
                            Output directory for downloaded JavaScript files
      --outdir_css=OUTDIR_CSS
                            Output directory for downloaded StyleSheet files
      --combine-js=PROD_JS
                            Output filename minified JavaScript for production
      --combine-css=PROD_CSS
                            Output filename minified CSS for production
      --combine-tmpl=PROD_TMPL
                            Output filename cached templates for production
      --empty-tmpl=DEVL_TMPL
                            Output filename empty template cache for development
      -j URL_JS, --javascript=URL_JS
                            JavaScript URL, use once for each file
      -c URL_CSS, --css=URL_CSS
                            StyleSheet URL, use once for each file
      -p URL_TMPL, --partial=URL_TMPL
                            Partial HTML URL, use once for each file


Angular usage::

    angular.module('MyApp', ['templatecache']);
