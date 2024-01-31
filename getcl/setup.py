from setuptools import setup, find_packages
import codecs

setup(
    name='getcl',
    version='0.1.dev0',
    license='MIT',
    description='Python Package for the Mapping of Conceptlists',
    long_description=codecs.open('README.md', "r", "utf-8").read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords='word prediction',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    py_modules=["getcl"],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    python_requires='>=3.6',
    install_requires=["pysem>=0.5.0", "pyconcepticon", "cldfbench", "tabulate",
        "clldutils", "pycldf"],
    entry_points={"console_scripts": ["conceptlist=getcl:main"]},
    extras_require={
        'dev': ['wheel', 'twine'],
        'test': [
            'pytest>=4.3',
            'pytest-cov',
            'coverage>=4.2',
        ],
    },
)
