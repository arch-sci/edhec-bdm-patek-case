from setuptools import setup, find_packages

setup(
    name='patek_analysis',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'google-cloud-bigquery',
        'db-dtypes'
    ]
)