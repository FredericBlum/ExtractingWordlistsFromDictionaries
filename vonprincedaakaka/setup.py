from setuptools import setup


setup(
    name='cldfbench_daakaka',
    py_modules=['cldfbench_daakaka'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'cldfbench.dataset': [
            'daakaka=cldfbench_daakaka:Dataset',
        ]
    },
    install_requires=[
        'cldfbench',
        'pyglottolog',
        'pydictionaria>=2.1',
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)
