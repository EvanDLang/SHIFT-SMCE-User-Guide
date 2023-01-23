from setuptools import setup, find_packages
from os import path

this_dir = path.abspath(path.dirname(__file__))
with open(path.join(this_dir, "README.md")) as f:
    long_description = f.read()

__version__ = "0.0.1"
for line in open(path.join("SHIFT-SMCE-User-Guide", "__init__.py")):
    if line.startswith("__version__"):
        exec(line.strip())

setup(
    name="SHIFT-SMCE-User-Guide",
    version=__version__,
    description="SHIFT-SMCE-User-Guide",
    url="https://github.com/EvanDLang/SHIFT-SMCE-User-Guide",
    author="Evan Lang",
    author_email="evan.d.lang@nasa.gov",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.4',
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Natural Language :: English",
    ],
    packages=find_packages(),
    install_requires=[],
    entry_points={},
    zip_safe=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
)
