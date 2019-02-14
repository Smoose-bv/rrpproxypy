from setuptools import find_packages
from setuptools import setup


with open('README.md', 'r') as readme:
    long_description = readme.read()


version = '0.1.0'


setup(
    name='rrpproxypy',
    version=version,
    author='Smoose BV',
    description='Python interface to the RRPproxy API.',
    url='https://github.com/Smoose-bv/rrpproxypy',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='GPL-3',
    keywords='rrpproxy rrp api library',
    packages=find_packages(),
    install_requires=[
        'requests >= 2.21.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
)
