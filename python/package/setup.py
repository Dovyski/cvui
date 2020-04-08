import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cvui",
    version="2.7",
    author="Fernando Bevilacqua",
    author_email="dovyski@gmail.com",
    license="MIT",
    description="A (very) simple UI lib built on top of OpenCV drawing primitives",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dovyski/cvui",
    packages=setuptools.find_packages(),
    classifiers=(
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: User Interfaces"
    ),
)
