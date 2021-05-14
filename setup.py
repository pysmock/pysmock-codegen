import setuptools
from pysmock import __version__,__author__,__author_email__,__description__

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="pysmock",
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    long_description=long_description,
    description=__description__,
    long_description_content_type="text/markdown",
    url="https://github.com/pysmock/pysmock-codegen",
    packages=setuptools.find_packages(include=['pysmock','pysmock.models','pysmock.utils']),
    # namespace_packages=setuptools.find_packages(include=['pysmock','pysmock.models','pysmock.utils']),
    # console_scripts="pysmock.__main__:main",
    # py_modules=['pysmock/models','pysmock/utils'],
    python_requires=">=3.6",
    include_package_data=True,
    install_requires=[
        "typer>=0.3.2",
        "deepdiff>=5.5.0",
        "pyyaml>=5.4.1",
        "jinja2>=2.11.2"
    ],
    entry_points={
        'console_scripts':[
            'pysmock=pysmock:main',
        ]
    }
)