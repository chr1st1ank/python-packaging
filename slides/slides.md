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
  div.twocols ul {
    margin-top: 0 !important;
  }
  div.twocols p.break {
    break-before: column;
    margin-top: 0;
  }
---

# **Python Packaging**

![bg left:40% 80%](Python-logo-notext.svg.png)

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

### How does it work?

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

## Distributing a Python package

Steps to make a Python package importable on a target system:

![](https://kroki.io/mermaid/svg/eNp9UM9rwjAUvuevyCodG7RQ3C6rQ8GJIOwwZLfiISYvNpglJUlbRfq_L-mi22mX8PL9eN97L00vQglX4kvCpe5pTYxLwo8BJ610W1AMDBiPJSCPyTDgIU3RwZCmxu9bhBh01Qo6kLoB87o3c6tbQ8HucJ7vWyFZns_xB6FHcgAPtY3UZMSacyOqh8gE48YnnR53KBBeyYSlugOD7wPJdK9uzmkVbSFkjoXtawB5ERaPxWLAKGKeP4MNovFbjW9wbZR1RErPuOqTmAO4kAKqE0arL1Bu96dFovQCL8Myd8mtF0JUEmtXwHG8FeZCynLCGMusM_oIf-u8F8zVZdGcZr9Gf2zBCb0612_L9fPLfwY_YNQWxVPhtVRLbcoJ5zyq_DBd5rLxiF59RZtpFm-W_Wx1jZ59AxTcr2o=)

- Build (sdist or wheel)
- Upload
- Download
- Build (if sdist)
- Install

---

## Short history of Python packaging

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

### Distributing an executable

--- 

### Docker: the common way

----

### Docker on wheels

---

### Summary


<!--

outline:

- intro: python packaging and deployment. Steps involved normally. Then docker.
- Tooling for the topics 
- status quo: typical workflow with file copying + requirement installation
- the standard Python way of packaging
- a potential workflow with wheel + docker
- advantages / disadvantages

infos: 

  - https://bernat.tech/presentations/
  - https://gaborbernat.github.io/packaging-tutorial-pycon-us-21/#/78

things to show:

  - venv -> build -> install -> test -> distribute -> run
  - poetry for testing or even building the docker image?
  - issues of manual assembly:
     - relative imports (PYTHONPATH)
     - cython
     - binary
     - resources
-->