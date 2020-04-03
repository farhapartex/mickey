import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mickey", # Replace with your own username
    version="0.0.3",
    author="Md Nazmul Hasan",
    author_email="hasan08sust@gmail.com",
    description="A Django app to build complete blog site.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/farhapartex/mickey",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)