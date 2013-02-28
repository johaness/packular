from setuptools import setup

VERSION = '0.0.1'
NAME = 'packular'

setup(
        name = NAME,
        version = VERSION,
        description = "JS/CSS/Partials packing and referencing",
        long_description = "",
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
        )

