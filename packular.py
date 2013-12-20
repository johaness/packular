#!/usr/bin/env python

"""Packular reads lists of required JavaScript, CSS, and partial HTML files,
and downloads/combines/references them in index.html files for use in
development and production.
"""

from ConfigParser import ConfigParser, NoOptionError
from argparse import ArgumentParser
from pprint import pformat
from itertools import chain
import os.path as osp
from subprocess import check_output, STDOUT
from glob import glob
from urlparse import urlparse


# used only when no command line arguments are provided
# and the file exists
DEFAULT_CONF_FILE = 'packular.conf'
# prefix for section names in config file that describe build targets
PFX = 'target:'
PFX_LEN = len(PFX)

# Templates
SCRIPT = """<script src="%s"></script>"""
LINK = """<link rel="stylesheet" href="%s" />"""
ANGULAR = """angular.module("templatecache", []).run(["$templateCache",
function($templateCache) { %s }]);"""
TMPL = """$templateCache.put("%s", "%s");"""

# Replace this in index_tmpl
AUTOGEN = """<!-- AUTOGENERATED -->"""



class Target(object): # silence pyflakes
    """Configuration for one build target"""

    def __init__(self, **kw):
        self.__dict__.update(**kw)

    def __repr__(self):
        return pformat(self.__dict__)


class _NoDefault:
    """Sentinel for "No Default" for DefaultConfigParser.get()"""
    pass


class DefaultConfigParser(ConfigParser):
    """ConfigParser with default parameter in get()"""

    def get(self, section, option, default=_NoDefault):
        """return ``option`` from ``section``, ``default`` if not found"""
        try:
            return ConfigParser.get(self, section, option)
        except NoOptionError:
            if default == _NoDefault:
                raise
            else:
                return default


def parse_options():
    """Parse command line options"""

    opt = ArgumentParser(description=__doc__)

    opt.add_argument('config_file', metavar="CONFIG_FILE", type=str, nargs='?',
            help = "Packular configuration file (default %s)" %
            (DEFAULT_CONF_FILE,), default = DEFAULT_CONF_FILE)

    opt.add_argument('-S', metavar="KEY=VALUE", type=str, nargs='*',
            help = "Overwrite config file variables, e.g. version=2.0")

    return opt.parse_args()


def read_config(config_file, defaults):
    """read configuration file"""

    cfg = DefaultConfigParser(allow_no_value=True)
    cfg.readfp(config_file)

    # override w/ command line arguments
    for key, value in defaults.items():
        cfg.set('DEFAULT', key, value)

    targets = dict((sect[PFX_LEN:], Target(
                template    = cfg.get(sect, 'template'),
                index       = cfg.get(sect, 'index'),
                download    = (cfg.has_option(sect, 'download') and
                               cfg.getboolean(sect, 'download')) or False,
                outdir_js   = cfg.get(sect, 'dir_js', ''),
                outdir_css  = cfg.get(sect, 'dir_css', ''),
                prefix_js   = cfg.get(sect, 'prefix_js', None),
                prefix_css  = cfg.get(sect, 'prefix_css', None),
                combine_js  = cfg.get(sect, 'combine_js', None),
                combine_css = cfg.get(sect, 'combine_css', None),
                combine_prt = cfg.get(sect, 'combine_partial', None),
                include_js  = cfg.get(sect, 'include_js', None),
                include_css = cfg.get(sect, 'include_css', None),
                url_js   = [],
                url_css  = [],
                url_html = [],
                ))
            for sect in cfg.sections() if sect.startswith('target:'))

    def file_list(file_section, append):
        default_spec = cfg.get('DEFAULT', file_section, None)
        if default_spec is not None:
            default_includes = default_spec.split(',')
        else:
            default_includes = targets.keys()

        for option in cfg.options(file_section):
            if cfg.has_option('DEFAULT', option):
                continue
            option = option.decode('string_escape')
            includes = cfg.get(file_section, option, None)
            for incl in (includes and includes.split(',')) or default_includes:
                for exp in (remote_url(option) and [option]) or \
                        glob(option) or [option]:
                    append(targets[incl.strip()])(exp)

    if cfg.has_section('javascript'):
        file_list('javascript', lambda t: t.url_js.append)

    if cfg.has_section('css'):
        file_list('css', lambda t: t.url_css.append)

    if cfg.has_section('partial'):
        file_list('partial', lambda t: t.url_html.append)

    return targets


def configure():
    """read configuration from command line options and config file values"""
    opts = parse_options()
    defaults = dict(v.split('=') for v in opts.S or [])
    with file(opts.config_file) as config:
        return read_config(config, defaults)



def remote_url(url):
    """return full remote URL or None if local file"""
    if url.startswith('//'):
        return 'https:' + url
    elif url.startswith('http://') or url.startswith('https://'):
        return url


def make_local(urls, out_dir, __nonlocal_cache=[[]]):
    """
    download non-local ``urls`` into ``out_dir``
    return generator of all-local urls
    """
    CURL = 'curl -s -f -o %s %s'

    for url in urls:
        remote = remote_url(url)
        if remote:
            remote = remote.replace('.min.', '.')
            fname = osp.join(out_dir,
                             osp.basename(urlparse(remote).path.rstrip('/')))
            if not (osp.isfile(fname) or fname in __nonlocal_cache[0]):
                print "  Download:", remote
                __nonlocal_cache[0].append(fname)
                curl = CURL % (fname, remote,)
                check_output(curl, stderr=STDOUT, shell=True)
            else:
                print "  Download [cached]:", url
            yield fname
        else:
            yield url


def combine_local(urls, fname, out_name=None):
    """
    merge content of all local ``urls`` into one file `fname`
    return generator of non-local urls
    """
    combine = []

    for url in urls:
        if url.startswith('//'):
            yield url
        else:
            combine.append(file('./' + url).read())

    with file(fname, 'w') as comb:
        comb.write('\n'.join(combine))

    yield out_name or fname


def partials(filename, urls):
    """Read HTML templates and convert into angular $templateCache call"""

    def html2js(url):
        """convert HTML into JavaScript string"""
        data = file('./' + url).read(). \
                replace('"', r'\"').replace('\n', r'\n')
        # angular would not cache the empty string
        return '/' + url, data or "<!-- empty -->"

    tmpls = [TMPL % html2js(url) for url in urls]

    with file(filename, 'w') as tmpl:
        tmpl.write(ANGULAR % ('\n'.join(tmpls),))


def prefix(iterable, pfx):
    """Prepend ``pfx`` to all items in ``iterable``"""
    for elm in iterable:
        if remote_url(elm):
            yield elm
        else:
            yield pfx + elm


def build(target):
    """build one target"""

    if target.combine_prt:
        print "  Partials:", target.combine_prt
        partials(target.combine_prt, target.url_html)

    if target.download:
        target.url_css = make_local(target.url_css, target.outdir_css)
        target.url_js = make_local(target.url_js, target.outdir_js)

    if target.combine_css:
        print "  Combine CSS:", target.combine_css
        target.url_css = combine_local(
                target.url_css, target.combine_css, target.include_css
        )

    if target.combine_js:
        print "  Combine JS:", target.combine_js
        target.url_js = combine_local(
                target.url_js, target.combine_js, target.include_js
        )

    if target.prefix_js:
        print "  Adding JS Prefix:", target.prefix_js
        target.url_js = prefix(target.url_js, target.prefix_js)

    if target.prefix_css:
        print "  Adding CSS Prefix:", target.prefix_css
        target.url_css = prefix(target.url_css, target.prefix_css)

    html_out = "\n".join(chain(
            (LINK % css_file for css_file in target.url_css),
            (SCRIPT % script_file for script_file in target.url_js),
            ))

    print "  Write Index:", target.index
    template = file(target.template).read()
    with file(target.index, 'w') as index:
        index.write(template.replace(AUTOGEN, html_out))



def main():
    """entry point"""
    targets = configure()
    for name, target in targets.items():
        print "Building target", name
        build(target)
        print


if __name__ == '__main__':
    main()
