from setuptools import setup

setup(
    name='multivitamin',
    version='2.2.5',
    packages=[
        'multivitamin',
        'multivitamin.algorithms',
        'multivitamin.basic',
        'multivitamin.supp',
        'multivitamin.utils'
    ],
    install_requires=[
        'matplotlib>=3.1.1',
        'networkx>=2.4',
        'scipy',
        'ete3'
    ],
    entry_points={
        'console_scripts': ['multiVitamin=multivitamin.multiVitamin:main']
    }
)