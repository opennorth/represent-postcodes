from setuptools import setup

setup(
    name="represent-postcodes",
    version="0.0.1",
    license="MIT",
    packages=[
        'postcodes',
        'postcodes.management',
        'postcodes.management.commands',
    ],
    install_requires=[
        'django-appconf',
    ],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'License :: OSI Approved :: MIT License',
        'Framework :: Django',
        'Topic :: Scientific/Engineering :: GIS',
    ],
)
