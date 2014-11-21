packular
========

Packular reads lists of required JavaScript, CSS, and partial HTML files,
and downloads/combines/references them in index.html files for use in
development and production. It supports pre-loading AngularJS templates
via ``$templateCache``.

Packular is a Python solution without any dependencies.
If you are looking for a JavaScript based implementation with similar
features, `grunt`_ is a good match.

.. _grunt: http://gruntjs.com/

packular.conf
=============

When no command line options are given, packular will try to read 
``packular.conf`` in the current directory. Use ``packular config_file`` to 
provide another filename. 

Sample config file::

    [DEFAULT]
    # default options apply to all ``target:`` blocks and can be
    # overriden on the command line

    # you may define a version ID and interpolate it into values below
    version = 9c2a5d2096dbb

    # source template for index.html
    template = index-template.html

    # download remote files into these directories
    download = true
    dir_js = lib
    dir_css = lib

    # prefix for all URLs inserted into index.html
    prefix_js = ./app/
    prefix_css = ./app/

    # specify default targets for file lists below, default is all targets
    javascript = dev,test,prod
    css = dev,test,prod
    partial = test,prod

    # any non reserved options will be passed as context variables when
    # rendering the template. they can be used in the template using the
    # python `format` dictionory interpolation style e.g. {custom_favicon}
    custom_favicon = favicon.ico

    [target:prod]
    index = index-production.html
    download = false

    # combine list of partials below into template cache file
    combine_partial = template-cache.js

    # combine all JS/CSS sources into one file
    combine_js = production.js
    # but include under a different name in the generated HTML
    # (allows for running eg. minification on the output of combine_js)
    include_js = production-min.js
    combine_css = production.css

    # overwrite some of the defaults -- the version is set above in [DEFAULT]
    prefix_js = http://cdn.example.org/static/%(version)s/js/
    prefix_css = http://cdn.example.org/static/%(version)s/css/

    # override variable value
    custom_favicon = favicon.png

    [target:dev]

    # index.html generated for this target
    index = index-development.html

    # empty cache for development
    combine_partial = no-template-cache.js

    [target:test]
    index = index-test.html
    combine_partial = template-cache.js

    [javascript]

    # included in all index.html
    test.js

    # include in development index.html only
    no-template-cache.js = dev

    # include in production and testing index.html only
    template-cache.js = prod,test

    # include in test index.html only
    mocks.js = test

    # remote resources start with //
    //ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js

    [css]
    test.css

    [partial]
    test.html


Command line options::

    usage: packular [-h] [-S [KEY=VALUE [KEY=VALUE ...]]] [CONFIG_FILE]

    positional arguments:
      CONFIG_FILE           Packular configuration file (default packular.conf)

    optional arguments:
          -S [KEY=VALUE [KEY=VALUE ...]]
                            Overwrite config file variables


Example::

    packular -S version=`git rev-parse HEAD`



Angular usage::

    angular.module('MyApp', ['templatecache']);
