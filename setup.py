from setuptools import setup, find_packages

setup(
    name='futcli',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'tabulate',
    ],
    entry_points={
        'console_scripts': [
            'futcli = futcli.futcli:futcli',
        ],
    },
)
