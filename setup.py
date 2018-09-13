from setuptools import find_packages
from setuptools import setup


with open('requirements.txt') as f:
    REQUIREMENTS = [
        line.strip() for line in f.readlines() if line.strip()]


setup(
    name='chorogrid',
    version='0.0.0',
    description='Python choropleths',
    author='Prooffreader',
    author_email='',
    url='https://github.com/jeffschecter/chorogrid',
    packages=["chorogrid"],
    install_requires=REQUIREMENTS
)
