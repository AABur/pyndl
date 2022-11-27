"""
Pyndl - Naive Discriminative Learning in Python
===============================================

*pyndl* implements Naïve Discriminative Learning (NDL) in Python. NDL is an
incremental learning algorithm grounded in the principles of discrimination
learning and motivated by animal and human learning research. Lately, NDL
has become a popular tool in language research to examine large corpora and
vocabularies, with 750,000 spoken word tokens and a vocabulary size of 52,402
word types. In contrast to previous implementations, *pyndl* allows for a
broader range of analysis, including non-English languages, adds further
learning rules and provides better maintainability while having the same
fast processing speed. As of today, it supports multiple research groups
in their work and led to several scientific publications.

"""

import platform
import os
import sys
import multiprocessing as mp
try:
    from importlib.metadata import requires
except ModuleNotFoundError:  # python 3.7 and before
    requires = None
try:
    from packaging.requirements import Requirement
except ModuleNotFoundError:  # this should only happend during setup phase
    Requirement = None

try:
    from importlib import metadata
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    import toml
    __version__ = toml.load("pyproject.toml")["tool"]["poetry"]["version"] + "dev"


def sysinfo():
    """
    Prints system the dependency information
    """
    if requires:
        dependencies = [Requirement(req).name for req in requires('pyndl')
                        if not Requirement(req).marker]

    header = ("Pyndl Information\n"
              "=================\n\n")

    general = f"General Information\n-------------------\nPython version: {sys.version.split()[0]}\nPyndl version: {__version__}\n\n"


    uname = platform.uname()
    osinfo = ("Operating System\n"
              "----------------\n"
              "OS: {s.system} {s.machine}\n"
              "Kernel: {s.release}\n"
              "CPU: {cpu_count}\n").format(s=uname, cpu_count=mp.cpu_count())

    if uname.system == "Linux":
        _, *lines = os.popen("free -m").readlines()
        for identifier in ("Mem:", "Swap:"):
            if memory := [line for line in lines if identifier in line]:
                _, total, used, *_ = memory[0].split()
            else:
                total, used = '?', '?'
            osinfo += f"{identifier} {used}MiB/{total}MiB\n"

    osinfo += "\n"

    deps = ("Dependencies\n"
            "------------\n")

    if requires:
        deps += "\n".join("{pkg.__name__}: {pkg.__version__}".format(pkg=__import__(dep))
                          for dep in dependencies)
    else:
        deps = 'You need Python 3.8 or higher to show dependencies.'

    print(header + general + osinfo + deps)
