from setuptools import setup

setup(
    name="represent-postcodes",
    version="0.0.1",
    description="A web API for postal codes associated to electoral districts, packaged as a Django app.",
    url="https://github.com/rhymeswithcycle/represent-postcodes",
    license="MIT",
    packages=[
        'postcodes',
        'postcodes.management',
        'postcodes.management.commands',
        'postcodes.migrations',
    ],
    install_requires=[
        'django-appconf',
        'represent-boundaries',
    ],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'License :: OSI Approved :: MIT License',
        'Framework :: Django',
    ],
)
