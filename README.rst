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

    [index]
    template = index-template.html
    dev = index-development.html
    prod = index-production.html

    [output]
    # download external files into these directories
    dir_js = lib
    dir_css = lib
    # merge local files into these files
    prod_js = production.js
    prod_css = production.css
    # combine partials into template cache for production
    prod_tmpl = mytmpl.js
    # empty template cache for development
    dev_tmpl = no-tmpl.js

    [javascript]
    test.js
    # include in development index.html only
    ?no-tmpl.js
    # include in production index.html only
    !mytmpl.js
    # detected as remote source. downloaded for development,
    # but included as-is for production
    //ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js

    [css]
    test.css

    [partial]
    test.html


Command line options::

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
      --prod-js=PROD_JS     Output filename minified JavaScript for production
      --prod-css=PROD_CSS   Output filename minified CSS for production
      --prod-tmpl=PROD_TMPL
                            Output filename cached templates for production
      --dev-tmpl=DEVL_TMPL  Output filename empty template cache for development
      -j URL_JS, --javascript=URL_JS
                            JavaScript URL, use once for each file. URLs from the
                            config file are written first. Prefix filename with !
                            to include in production only, ? to include in
                            development only.
      -c URL_CSS, --css=URL_CSS
                            StyleSheet URL, use once for each file
      -p URL_TMPL, --partial=URL_TMPL
                            Partial HTML URL, use once for each file


Angular usage::

    angular.module('MyApp', ['templatecache']);
