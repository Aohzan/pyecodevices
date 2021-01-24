import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyecodevices",
    version="1.0.0",
    author="Aohzan",
    author_email="aohzan@gmail.com",
    description="Get information from GCE Eco-Devices.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aohzan/pyecodevices",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
