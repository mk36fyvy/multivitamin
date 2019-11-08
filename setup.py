from setuptools import setup

setup(
    name='multivitamin', 
    version='1.0', 
    packages=[
        'multivitamin',
        'multivitamin.algorithms',
        'multivitamin.basic',
        'multivitamin.supp',
        'multivitamin.utils'
    ],
    install_requires=[
        'matplotlib',
        'networkx'
    ],
    entry_points={
        'console_scripts': ['multiVitamin=multivitamin.multiVitamin:main']
    }
)