import os
from os.path import dirname, exists, join, realpath, relpath
from setuptools import setup
import sys
import shutil

#  NOTE: Shebangs:
#      * https://docs.python.org/3/using/windows.html#shebang-lines
#      * https://github.com/pypa/pip/issues/4616

if sys.platform == 'win32':
    sys.executable='python.exe'

ROOT = dirname(realpath(__file__))

def get_package_data():
    print('-- GET PACKAGE DATA')

    def get_file_paths(main_path=None, filters=()):
        ''' @filters = ('.html')
        '''
        main_path = join(ROOT, main_path)
        print('>> OCEAN DATA QC JS PATH: {}'.format(main_path))
        if not exists(main_path) or main_path is None:
            raise RuntimeError("packaging non-existent path: %s" % main_path)

        file_paths = []
        for path, dirs, files in os.walk(main_path):
            path = relpath(path, main_path)
            print('>> OCEAN DATA QC JS rel PATH: {}'.format(path))
            for f in files:
                if not filters or f.endswith(filters):
                    file_paths.append(join(path, f))
        print('>> PACKAGE DATA: {}'.format(file_paths))
        return file_paths

    return {
        'ocean_data_qc': [
            'templates/*.*',
            'files/*.json',
        ] + ['static/' + x for x in get_file_paths('ocean_data_qc/static')] + ['octave/' + x for x in get_file_paths('ocean_data_qc/octave')]
        # 'ocean_data_qc_js': get_file_paths('ocean_data_qc_js')
    }

requires = [
    'bokeh ==2.1.1',
    'pandas >=1.0.3',
    'seawater >=3.3.4',
    'more_itertools >=8.2.0',
    'oct2py >=5.0.4',
    'scipy >=1.4.1',  # oct2py needs it, though it is not a direct dependency
    'tilecloud >=1.1.0',

    # libraries related to export svg, png and pdf files
    # 'svglib >=0.9.2',
    'reportlab >=3.5.42',
    # 'selenium >=3.141.0',
]

dependency_links = [
    'https://github.com/ocean-data-qc/tilecloud/tarball/master#egg=tilecloud'
]

if sys.platform == "win32":
    requires.append('python-magic-win64 >=0.4.13')  # depends on python-magic and adds the DLL libmagic library

setup(
    name='ocean_data_qc',
    version='1.4.0',                                    # TODO: extract the version from package.json
    description='WHP file managing',
    long_description=open("README.md").read(),          # TODO: check if this is readable in this is publish in a future channel repository or
    long_description_content_type="text/markdown",      #       Python Package Index https://pypi.org/
    keywords="ocean data quality control seawater csv whp",
    url='https://www.atlantos-h2020.eu/',
    author='Jesus Cacabelos',
    author_email='jcacabelos@iim.csic.es',
    license='MIT',
    install_requires=requires,
    dependency_links=dependency_links,
    packages=[
        'ocean_data_qc',
        'ocean_data_qc.bokeh_models',
        'ocean_data_qc.data_models',
        'ocean_data_qc.octave'
    ],
    package_data=get_package_data(),
    zip_safe=False,
)
