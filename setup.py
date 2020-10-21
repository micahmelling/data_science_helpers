import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="data_science_helpers",
    version="0.0.1",
    author="Micah Melling",
    author_email="micahmelling@gmail.com",
    description="Common data science helper functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/micahmelling",
    packages=['ds_helpers'],
    install_requires=['boto3>=1.11.2', 'SQLAlchemy>=1.3.20', 'pymysql>=0.9.3'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
