from setuptools import setup, find_packages
import os
import json

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open("package_setup.json", "r") as f:
    package_setup = json.load(f)
    package_name = package_setup["package_name"]
    package_version = package_setup["package_version"]
    package_description = package_setup["package_description"]
    package_tasks = package_setup["tasks"]
    package_url = package_setup["package_url"]


setup(
    name=package_name,
    description="A python package template for build, test and deploy python wheel jobs to environment",
    long_description=package_description,
    long_description_content_type="text/markdown",
    author="harish.nedunuri@outlook.com",
    url=package_url,
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            f"{package_name}.{task}={package_name}.{task}.entry:main"
            for task in package_tasks
        ]
    },
    version=package_version,
    install_requires=requirements,
    python_requires=">=3.12",
)