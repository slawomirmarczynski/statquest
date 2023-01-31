[metadata]
name = statquest
version = 0.4.0.1
description = Statistical software to find dependent observables.
author = Sławomir Marczyński
author_email =

[options]
packages = find:
install_requires =
    gettext~=0.19.8.1
    pandas~=1.4.3
    numpy~=1.23.0
    scipy~=1.8.1
    typing~=3.10.0.0
    setuptools~=62.6.0
include_package_data=True

[options.package_data]
statquest = locale/*

[options.packages.find]
include=
    statquest*
exclude=
    tests*