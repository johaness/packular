from setuptools import setup
import importlib

VERSION = '0.0.7'
NAME = 'packular'

setup(
        name = NAME,
        version = VERSION,
        description = "JS/CSS/Partials packing and referencing",
        long_description = importlib.import_module(NAME).__doc__,
        license = 'BSD',
        author = "Johannes Steger",
        author_email = 'jss@coders.de',
        url = 'https://github.com/johaness/%s' % (NAME,),
        zip_safe = True,
        py_modules = [NAME,],
        entry_points = {
            'console_scripts': [
                '%s=%s:main' % (NAME, NAME,),
                ],
            },
        classifiers = [
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'License :: OSI Approved :: BSD License',
            ],
        )

