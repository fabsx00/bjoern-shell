from distutils.core import setup

setup(
    name='bjoern-shell',
    version='0.1',
    packages=['bjoernshell', 'bjoernshell.completer'],
    package_dir={'bjoernshell': 'bjoernshell'},
    package_data={'bjoernshell': ['data/banner.txt']},
    scripts=['scripts/bjosh'],
    url='',
    license='GPLv3',
    author='Alwin Maier',
    author_email='amaier@gwdg.de',
    description='Interactive shell for bjoern'
)