from setuptools import setup, find_packages

setup(
    name="cars_app",
    version="0.1",
    packages=find_packages(),
    python_requires=">=3.6",
    author="Dimitriy Dashinov",
    author_email="ddashinov@abv.bg",
    long_description=open("carsREADME.txt").read(),
    long_description_content_type="text",
    url="https://github.com/DimitriyDashinov/cars-dataset-app",
)