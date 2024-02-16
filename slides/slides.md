---
theme: gaia
_class: lead
paginate: true
backgroundColor: #ccc
marp: true
#backgroundImage: url('https://marp.app/assets/hero-background.svg')
style: |
  @import 'https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css';
  section {
    font-size: 30px
  }
  div.twocols {
    margin-top: 35px;
    column-count: 2;
  }
  div.twocols p:first-child,
  div.twocols h1:first-child,
  div.twocols h2:first-child,
  div.twocols ul:first-child,
  div.twocols ul li:first-child,
  div.twocols ul li p:first-child {
    margin-top: 0 !important;
  }
  div.twocols p.break+ul {
    margin-top: 0 !important;
  }
  div.twocols p.break+p {
      margin-top: 0px;
  }
  div.twocols p.break {
    break-before: column;
    margin-top: 0;
  }
---

# **Python Packaging**

![bg left:40% 80%](Python-logo-notext.svg.png)

--- 

## Outline

- [**Python Packaging**](#python-packaging)
  - [Outline](#outline)
  - [The Python import system](#the-python-import-system)
  - [Distributing a Python package](#distributing-a-python-package)
  - [Tools for the distribution process](#tools-for-the-distribution-process)
  - [Packaging and testing](#packaging-and-testing)
  - [Python applications in Docker/OCI](#python-applications-in-dockeroci)
  - [Summary](#summary)
  - [Thank you!](#thank-you)


---

## The Python import system

### Different module types

<!--
virtualenv env
./env/bin/python -m pip install pytoml
-->

```pycon
❯ ./env/bin/python
Python 3.10.12 (main, Jun 11 2023, 05:26:28) [GCC 11.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import sys
>>> sys                        # => Binary module linked to the interpreter
<module 'sys' (built-in)>
>>> import os
>>> os                         # => Standard library module
<module 'os' from '/usr/lib/python3.10/os.py'> 
>>> import pytoml
>>> pytoml                     # => Site-package module (installed with pip)
<module 'pytoml' from '/home/christian/code/python-packaging/env/lib/python3.10/site-packages/pytoml/__init__.py'>
```

---

### How does importing work?

There are multiple Importers which are called:

```pycon
>>> import sys
>>> for importer in sys.meta_path:
...     print(importer)
...
<_virtualenv._Finder object at 0x7f792a1d6560>
<class '_frozen_importlib.BuiltinImporter'>
<class '_frozen_importlib.FrozenImporter'>
<class '_frozen_importlib_external.PathFinder'>
```

This is where PathFinder looks for modules:

```pycon
>>> sys.path
['', '/usr/lib/python310.zip', '/usr/lib/python3.10', '/usr/lib/python3.10/lib-dynload', 
'/home/christian/code/python-packaging/env/lib/python3.10/site-packages']
```

---

### The parts of an installed Python package

<div class="twocols">

`bin` or `scripts` contains entry-points:
```console
❯ tree env/bin/
env/bin/
├── activate
├── activate.csh
...
├── pip
...
├── python -> /usr/bin/python3
├── python3 -> python
├── python3.10 -> python
├── wheel
...
```

<p class="break"></p>

`site-packages` holds the modules:

```console
❯ tree env/lib/python3.10/site-packages/pytoml
pytoml
├── __init__.py
├── __pycache__
│   ├── __init__.cpython-310.pyc
│   ...
├── core.py
├── parser.py
├── test.py
├── utils.py
└── writer.py
```

Metadata for each package:

```console
❯ ls env/lib/python3.10/site-packages/pytoml-0.1.21.dist-info/
INSTALLER  LICENSE  METADATA  RECORD  REQUESTED  WHEEL  top_level.txt
```

</div>

---

### Special case: editable install

- `pip install -e <folder>`
- The package is editable, because it is only linked - [PEP 660](https://peps.python.org/pep-0660/)
- Entry-points are installed as normally

<div class="twocols">

```console
❯ lsd --tree venv/lib/python3.11/site-packages/langc*
langc-0.1.0.dist-info
├── direct_url.json
├── entry_points.txt
├── INSTALLER
├── METADATA
├── RECORD
├── REQUESTED
└── WHEEL
langc.pth
```

<p class="break"></p>

```
───────┬─────────────────────────────────────────────────────────────────
       │ File: venv/lib/python3.11/site-packages/langc.pth
───────┼─────────────────────────────────────────────────────────────────
   1   │ /home/christian/code/python-packaging/poetry
```

```
───────┬─────────────────────────────────────────────────────────────────
       │ File: venv/bin/langc
───────┼─────────────────────────────────────────────────────────────────
   1   │ #!/home/christian/code/python-packaging/poetry/venv/bin/python
   2   │ # -*- coding: utf-8 -*-
   3   │ import re
   4   │ import sys
   5   │ from langc.cli import main
   6   │ if __name__ == '__main__':
   7   │     sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
   8   │     sys.exit(main())
```

---


## Distributing a Python package

Steps to make a Python package importable on a target system:

![](https://kroki.io/mermaid/svg/eNp9UM9rwjAUvuevyCodG7RQ3C6rQ8GJIOwwZLfiISYvNpglJUlbRfq_L-mi22mX8PL9eN97L00vQglX4kvCpe5pTYxLwo8BJ610W1AMDBiPJSCPyTDgIU3RwZCmxu9bhBh01Qo6kLoB87o3c6tbQ8HucJ7vWyFZns_xB6FHcgAPtY3UZMSacyOqh8gE48YnnR53KBBeyYSlugOD7wPJdK9uzmkVbSFkjoXtawB5ERaPxWLAKGKeP4MNovFbjW9wbZR1RErPuOqTmAO4kAKqE0arL1Bu96dFovQCL8Myd8mtF0JUEmtXwHG8FeZCynLCGMusM_oIf-u8F8zVZdGcZr9Gf2zBCb0612_L9fPLfwY_YNQWxVPhtVRLbcoJ5zyq_DBd5rLxiF59RZtpFm-W_Wx1jZ59AxTcr2o=)

- Build (sdist or wheel) ➡️ `python -m build`
- Upload ➡️ `python -m twine`
- Download
- Build (if sdist)
- Install ➡️ `python -m pip install <package>`

---

## Tools for the distribution process

<div class="twocols">

- Build
  - `python -m build`
  - `poetry build`
  - `flit build`
- Upload
  - `python -m twine`
  - `poetry publish`
  - `flit publish`
- Download, build, install
  - `python -m pip install <package>`

<p class="break"></p>

Frontend versus backend:

- A frontend:
  - Installs the build tools
  - Runs the build backend
- Some backends have a frontend, too

---

### Short history of Python packaging

<div class="twocols" style="font-size: 85%;">

- **2000** Python 1.6 - *distutils* - setup.py introduced:
    - used as invocation interface
    - configuration as Python code
- **2002** *PyPi* - [PEP 301](https://peps.python.org/pep-0301/)
- **2003** Standardized package *metadata* - [PEP 314](https://peps.python.org/pep-0314/)
- **2004** *Setuptools* became de-facto standard
- **2006** *virtualenv* - Third-party tool for virtual environment
- **2011** *venv* - Python 3.3 - [PEP 405](https://peps.python.org/pep-0405/)

<p class="break"></p>

- **2014** *Wheels* - [PEP 427](https://peps.python.org/pep-0427/)
- **2015** *flit* - declaratively configured builds
- **2016** *pyproject.toml* - [PEP 518](https://peps.python.org/pep-0518/)
- **2017** *build backends* without setup.py - [PEP 517](https://peps.python.org/pep-0517/)
- **2018** *poetry* - single tool to rule them all
- **2020** *pip dependency resolver*
- **2021** *pdm* - another tool to rule them all
- **2023** *rye* - another tool to rule them all

<sub><sup>See also [Packaging History](https://www.pypa.io/en/latest/history/) of the PyPa</sup></sub>

</div>

---

### The tooling landscape

<div style="text-align:center">

![height:480px](venn_diagram.png)
<sub><sup>Source <https://alpopkes.com/posts/python/packaging_tools/></sup></sub>

</div>

---

### What is needed on the target machine?

For a library:

- A Python interpreter environment
- Dependencies - compatible versions or exact version
- The python modules
- (maybe) Binary extensions
- (maybe) Resources (e.g. icons, ML models, man page)

For an application:

`+` Entry points
`-` Importable modules

---

### Build

```console
❯ python -m build
* Creating virtualenv isolated environment...
* Installing packages in isolated environment... (poetry-core>=1.0.0)
* Getting build dependencies for sdist...
* Building sdist...
* Building wheel from sdist
* Creating virtualenv isolated environment...
* Installing packages in isolated environment... (poetry-core>=1.0.0)
* Getting build dependencies for wheel...
* Building wheel...
Successfully built langc-0.1.0.tar.gz and langc-0.1.0-py3-none-any.whl
```

---

### Upload

```console
❯ twine upload --repository-url https://test.pypi.org/legacy/ dist/*
Uploading distributions to https://test.pypi.org/legacy/
Enter your API token: 
Uploading langc-0.1.0-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 447.8/447.8 kB • 00:00 • 3.5 MB/s
Uploading langc-0.1.0.tar.gz
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 436.7/436.7 kB • 00:00 • 3.7 MB/s

View at:
https://test.pypi.org/project/langc/0.1.0/
```

---
### Download & Install

From a package index:

```console
❯ pip install --index-url  https://test.pypi.org/simple langc
Looking in indexes: https://test.pypi.org/simple
Collecting langc
  Downloading https://test-files.pythonhosted.org/packages/e7/4c/
  ...
```

From a wheel:
```console
❯ venv2/bin/pip install /home/christian/code/python-packaging/poetry/dist/langc-0.1.0-py3-none-any.whl
...
```
--- 

## Packaging and testing

<div class="twocols" style="font-size: 85%;">

```shell
pip install poetry
poetry install

poetry run pytest
```

Issues, especially for libraries:

- Running on lock file dependencies
- Build dependencies are also available and tests may succeed only because of this
- Files in the sources may not be packaged

<p class="break"></p>

Wouldn't it be cleaner to test the *package*?

```shell
pip install build
pyproject-build --wheel

# ... move to clean folder and new Python environment

# Install the library from the wheel including test dependencies
pip install source-folder/dist/*.whl[test]

# Get the test code
cp source-folder/test ./

# Test
python -m pytest
```

</div>


---

## Python applications in Docker/OCI

Do we have everything to deploy an application now?

- A Python interpreter environment 🙌
- Dependencies - compatible versions or exact version 🙌
- The python modules ✅
- (maybe) Binary extensions ✅
- (maybe) Resources (e.g. icons, ML models, man page) ✅
- Entry points ✅

➡️ The image should provide the rest

---

### Docker images the usual way

```
FROM python:3.9-slim-bookworm

COPY ./environment/requirements.txt ./
RUN python -m pip install -r ./requirements.txt --no-cache-dir

ENV PYTHONPATH "${PYTHONPATH}:/workspace"    # <== Because imports didn't work

COPY ./pypackage ./pypackage                 #
COPY ./api ./api                             # <== Don't forget anything
COPY ./config ./config                       #
COPY ./entrypoint.py ./entrypoint.py         #

EXPOSE 8080

CMD ["python", "entrypoint.py"]
```

----

### Docker on wheels

![](https://kroki.io/mermaid/svg/eNpNjD0LwjAQQPf8iiOSzYJzBCcXwakOziF3aULPplxSKpT8dz9wcHvvDc-YLU2pWth04Lz66KTqjyEFt3DtaUISknfTxKNuDZoxahA3R7j2St3yIp4KdN0J7pGIv3R5uIGU8uxKOVOA3w1CYrY7RNyXKnmkf-7WhDXaw_w8vgCbcTIg)

```
FROM python:3.9-slim-bookworm

COPY ./environment/requirements.txt ./                          # Still good for caching 🤷‍♂️
RUN python -m pip install -r ./requirements.txt --no-cache-dir  # but not necessary

# no more PYTHONPATH mangling

COPY ./dist/*.whl ./                                            # We copy the wheel
RUN python -m pip install *.whl                                 # and install it

EXPOSE 8080

CMD ["myapi"]                                                   # Entrypoints are easy
```

---

### Comparison

Advantages of only Docker:

- No package build step

Advantages of Python + Docker builds:

- No problems with PYTHONPATH
- Binary extensions (e.g. Cython, PyO3) are covered
- Resources can be already included
- Entrypoints are available out-of-the-box
- No docker needed to test completeness of a package

---

## Summary

- Python's packages and virtual environments are standardized
- Distribution of a Python package:
  - consists of build, upload, download, install steps
  - there are several tools for each step
  - all deliver the same output from the same input (+ config)
- Python environment:
  - Interpreter needs to be set up separately
  - Dependencies are covered, but there is some degree of uncertainty
  - Docker images can help here
- Combining Python + Docker builds yields a fully standardized workflow

---

## Thank you!

Recommended readings:

- Anna-Lena Popkes: [Packaging tools](https://alpopkes.com/posts/python/packaging_tools/)
- Bernát Gábor [Python packaging demystified](https://bernat.tech/presentations/#py-packaging-us-21)
