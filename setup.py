# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='django-simple-spam-blocker',
    version='0.1.0',
    description='Simple spam blocker for Django',
    long_description=open('README.rst').read(),
    author='Masahiko Okada',
    author_email='moqada@gmail.com',
    url='http://github.com/moqada/django-simple-spam-blocker/',
    keywords=['django', 'spam'],
    license='BSD License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
