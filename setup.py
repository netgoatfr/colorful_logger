from setuptools import setup

setup(name='logger',
    version='1.0',
    description='Colorful and useful logging utility module for python',
    author='netgoatfr',
    author_email='netgoatfr@gmail.com',
    license='CC BY-SA',
    packages=['logger'],
    install_requires=[
        "datetime",
        "colorama",
    ]
)
