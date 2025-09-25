from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="testcato",
    version="1.2.4",
    packages=find_packages(),
    description="A package for categorizing test results.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Anurag",
    author_email="anuragsinha003@gmail.com",
    license="MIT",
    install_requires=[],
    entry_points={
        "pytest11": [
            "testcato = testcato.pytest_testcato",
        ],
    },
)
