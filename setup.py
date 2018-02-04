"""
A setuptools for drf-nested-views
"""
from setuptools import setup, find_packages
from codecs import open
from os import path


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()


setup(
    name='drf-nested-views', 
    version='1.0.0', 
    description='A set of views to work with drf-nested-routers',
    long_description=README,
    url='https://github.com/weynelucas/drf-nested-views/', 
    download_url="https://github.com/weynelucas/drf-nested-views/archive/1.0.0.tar.gz",
    author='Lucas Weyne',
    author_email='weynelucas@gmail.com',
    classifiers=[ 
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='django rest framework drf nested routers views drf-nested-routers drf-nested-views',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
)