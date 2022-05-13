""" Setup.py """

from setuptools import find_packages, setup  # type: ignore

install_reqs = [
    "bandit==1.7.4",
    "black==22.3.0",
    "featuretools==1.9.0",
    "mypy==0.950",
    "pylint==2.13.8",
    "typing-inspect==0.7.1",
]

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="tsutility",
    version="0.0.2",
    author="Narayan Nandeda",
    author_email="nandeda.narayan@gmail.com",
    description="A package to create Forecasting Features",
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=install_reqs,
    url="https://github.com/your_package/homepage/",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
