from setuptools import setup, find_packages

setup(
    name="steeltools",
    version="0.0.2",
    description="for steel Project test",
    packages=find_packages(),
    install_requires=[
        'Flask==2.2.3',
        'flasgger'
    ],
    python_requires=">=3.6"
)
