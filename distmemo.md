# 配布作業メモ
(作業が安定したら.travis.ymlに追加)

1. ./setup.py編集
1. python3 setup.py sdist
1. twine upload dist/*
1. [pypi](https://pypi.python.org/pypi?%3Aaction=pkg_edit&name=jsonica)確認


```
$ python3 setup.py sdist
running sdist
running egg_info
creating jsonica.egg-info
writing jsonica.egg-info/PKG-INFO
writing dependency_links to jsonica.egg-info/dependency_links.txt
writing requirements to jsonica.egg-info/requires.txt
writing top-level names to jsonica.egg-info/top_level.txt
writing manifest file 'jsonica.egg-info/SOURCES.txt'
reading manifest file 'jsonica.egg-info/SOURCES.txt'
reading manifest template 'MANIFEST.in'
warning: no files found matching 'LICENCSE'
warning: no files found matching '*' under directory 'modulename'
warning: no previously-included files matching '*.pyc' found anywhere in distribution
warning: no previously-included files matching '*~' found anywhere in distribution
warning: no previously-included files matching '*.bak' found anywhere in distribution
warning: no previously-included files matching '*.swp' found anywhere in distribution
warning: no previously-included files matching '*.pyo' found anywhere in distribution
writing manifest file 'jsonica.egg-info/SOURCES.txt'
warning: sdist: standard file not found: should have one of README, README.rst, README.txt, README.md

running check
creating jsonica-0.0.9
creating jsonica-0.0.9/docs
creating jsonica-0.0.9/jsonica.egg-info
copying files to jsonica-0.0.9...
copying MANIFEST.in -> jsonica-0.0.9
copying requirements.txt -> jsonica-0.0.9
copying setup.py -> jsonica-0.0.9
copying docs/Appendixies.md -> jsonica-0.0.9/docs
copying docs/README.md -> jsonica-0.0.9/docs
copying docs/README_ja.md -> jsonica-0.0.9/docs
copying docs/Usage_Samples.md -> jsonica-0.0.9/docs
copying docs/_config.yml -> jsonica-0.0.9/docs
copying jsonica.egg-info/PKG-INFO -> jsonica-0.0.9/jsonica.egg-info
copying jsonica.egg-info/SOURCES.txt -> jsonica-0.0.9/jsonica.egg-info
copying jsonica.egg-info/dependency_links.txt -> jsonica-0.0.9/jsonica.egg-info
copying jsonica.egg-info/requires.txt -> jsonica-0.0.9/jsonica.egg-info
copying jsonica.egg-info/top_level.txt -> jsonica-0.0.9/jsonica.egg-info
Writing jsonica-0.0.9/setup.cfg
creating dist
Creating tar archive
removing 'jsonica-0.0.9' (and everything under it)

$ twine upload dist/*
Uploading distributions to https://upload.pypi.org/legacy/
Enter your username: setminami
Enter your password:
Uploading jsonica-0.0.9.tar.gz
```
