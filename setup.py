from setuptools import setup, find_packages

setup(
    name="promg",
    version="0.1",
    packages=find_packages(),
    py_modules=["cli"],
    install_requires=[
        "click",
        "pathspec"
    ],
    entry_points={
        "console_scripts": [
            "promg=cli:cli",
        ],
    },
)