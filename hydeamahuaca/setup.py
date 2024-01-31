from setuptools import setup


setup(
    name='lexibank_hydeamahuaca',
    py_modules=['lexibank_hydeamahuaca'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'lexibank.dataset': [
            'hydeamahuaca=lexibank_hydeamahuaca:Dataset',
        ]
    },
    install_requires=[
        'cldfbench',
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)
