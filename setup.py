import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lighthouse_block_export",
    version="0.0.1",
    author="Lakshman Sankar",
    author_email="lsankar4033@gmail.com",
    description="Chain db export for lighthouse nodes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lsankar4033/lighthouse_block_export",
    packages=setuptools.find_packages(),
    install_requires=[
        "plyvel==1.2.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
