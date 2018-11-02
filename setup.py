import setuptools

with open("README.md", 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="mkmdtl",
    version="0.1",
    author="Nicolas F.",
    description="Generates Markdown tables from track listings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CounterPillow/mkmdtl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: zlib/libpng License"
    ],
    install_requires=[
        'requests',
        'wcwidth'
    ],
    entry_points={
        'console_scripts': ['mb2md=mkmdtl.mb2md:main',
                            'mi2md=mkmdtl.mi2md:main'],
    }
)
