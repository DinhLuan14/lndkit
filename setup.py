from setuptools import setup, find_packages

setup(
    name="lndkit",
    version="0.0.1",
    author="luannd",
    author_email="dinhluanwork@gmail.com",
    description="A simple utility package for JSON operations",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/DinhLuan14/lndkit",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)