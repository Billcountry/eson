import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

with open("RELEASE", "r") as release:
    version = release.read().strip()

setuptools.setup(
    name="eson",
    version=version,
    author="Billcountry",
    author_email="me@billcountry.tech",
    description="Extendable JSON to support different formats of data across languages. By default supports date and datetime objects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Billcountry/eson",
    packages=['eson', 'eson.extensions'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)