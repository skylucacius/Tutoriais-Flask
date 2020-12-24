from setuptools import find_packages, setup

setup(
    name='flaskr', # escolher um nome
    version='1.0.0', # escolher uma versão
    packages=find_packages(), # ['flaskr']
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)