from setuptools import setup

setup(name='logger',
    version='0.1',
    description='Colorful and useful logging utility module',
    author='netgoatfr',
    author_email='netgoatfr@gmail.com',
    license='CC BY-SA',
    packages=['logger'],
    install_requires=[
        "datetime",
        "colorama",
        "traceback"
    ]
)
