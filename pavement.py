#!/usr/bin/python3
from paver.easy import *
import paver
import os
import glob
import shutil
import sys
sys.path.append(os.path.dirname(__file__))


@task
def setup():
    sh('python3 -m pip install -U coverage radon yfinance python-dotenv pylint')


@task
def test():
    sh('python3 -m coverage run '
       '--source src/data_fetcher,src/filter_system,src/change_detector '
       '--omit="src/data_fetcher/pipeline.py,src/filter_system/filter_pipeline.py,src/change_detector/detector_pipeline.py" '
       '-m unittest discover -s tests')
    sh('python3 -m coverage html')
    sh('python3 -m coverage report --show-missing')


@task
def clean():
    for pycfile in glob.glob("*/*/*.pyc"):
        try: os.remove(pycfile)
        except: pass
    for pycache in glob.glob("*/__pycache__"):
        try: shutil.rmtree(pycache)
        except: pass
    try:
        shutil.rmtree(os.getcwd() + "/htmlcov")
    except:
        pass


@task
def radon():
    sh('radon cc src -a -nb')
    sh('radon cc src -a -nb > radon.report')
    if os.stat("radon.report").st_size != 0:
        raise Exception('radon found complex code')


@task
@needs(['setup', 'clean', 'test', 'radon'])
def default():
    pass