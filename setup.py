from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="project-prompt-generator",
    version="0.1.4",
    author="Ching Yi, Chan",
    author_email="chingyichan.tw@gmail.com",
    description="A tool to convert project files into structured markdown for LLM prompts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/qrtt1/project-prompt-generator",
    packages=find_packages(),
    py_modules=["cli"],
    install_requires=[
        "pathspec"
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: Markdown",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "promg=cli:cli",
            "ppg=cli:cli",
        ],
    },
)
