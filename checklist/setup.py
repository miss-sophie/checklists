from setuptools import setup, find_packages

setup(
    name='checklist',
    version='1.0.0',
    description='Modular aviation checklist management toolkit (YAML, ForeFlight .fmd, LaTeX)',
    author='miss-sophie',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'PyYAML==6.0.2',
        'pycryptodome',
        'jinja2',
    ],
    entry_points={
        'console_scripts': [
            'checklist=checklist.cli:main'
        ],
    },
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
    ],
)