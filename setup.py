from setuptools import setup

setup(
    name="promg",
    version="0.1",
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
