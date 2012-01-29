from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup

setup(
    name='represent-postcodes',
    packages=['postcodes'],
    version='0.0.1',
    install_requires=[
        'django-appconf'
    ],
)