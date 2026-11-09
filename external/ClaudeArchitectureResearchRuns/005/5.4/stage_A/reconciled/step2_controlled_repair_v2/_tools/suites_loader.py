"""Loads another regression suite by file name, so a v2 suite can reuse a v1 model without copying it."""
import importlib.util
import os

from rcommon import OUT


def load_suite(name):
    spec = importlib.util.spec_from_file_location('loaded_' + name, os.path.join(OUT, '_tools', 'suites', name + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m
