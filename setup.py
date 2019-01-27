import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RPi-Manage",
    version="0.0.6",
    author="Joao Marcos L Gomes",
    author_email="joaomarcos1999jm@mgial.com",
    description="A small package for Raspberry Pi manage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Joaomlg/RPi-Manage.git",
    packages=['RPi'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)