from setuptools import setup, find_packages

setup(
    name="common-models",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.85.0",
        "pydantic==1.10.17",
        "sqlalchemy==1.4.41",
        "sqlmodel==0.0.8",
    ],
    description="Shared models for locker-api and bulk-upload-service",
    author="Koloni",
    author_email="info@koloni.me",
    url="https://github.com/Koloni-Share/common-models",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
