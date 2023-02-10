from setuptools import setup

setup(
    name='statquest',
    version='0.4.2.1',
    packages=[''],
    package_dir={'': 'statquest'},
    url='https://github.com/slawomirmarczynski/statquest',
    license='BSD-3-clause',
    author='Sławomir Marczyński',
    author_email='',
    description='Automated statistical data analysis.',
    install_requires=[
        'future',
        'numpy',
        'matplotlib',
        'scipy',
        'networkx',
        'pandas',
        'setuptools',
        'ydata_profile'
    ]
)
