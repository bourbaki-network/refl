#!/usr/bin/env python3

import pytest
import sys
sys.path.insert(0, '.')

from src.commands import *
from src.log import Logging

def test_range():
  r = rangeBuilder('./test/test.agda', 6, 6, 8, 6, 6, 12)
  assert r() == '(intervalsToRange (Just (mkAbsolute "./test/test.agda")) [Interval  (Pn () 6 6 8 ) (Pn () 6 6 12 ) ])'

def test_compile():
  assert Commands('./test/test.agda').compile('GHC', []) == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_compile GHC "./test/test.agda" [])'

def test_load():
  assert Commands('./test/test.agda').load([]) == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_load "./test/test.agda" [])'

def test_constraints():
  assert Commands('./test/test.agda').constraints() == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_constraints)'

def test_metas():
  assert Commands('./test/test.agda').metas() == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_metas)'

def test_show_module_contents_toplevel():
  assert Commands('./test/test.agda').show_module_contents_toplevel('Normalised', 'Agda.Builtin.Nat') == \
    'IOTCM "./test/test.agda" None Indirect (Cmd_show_module_contents_toplevel Normalised "Agda.Builtin.Nat")'

def test_search_about_toplevel():
  assert Commands('./test/test.agda').search_about_toplevel('Normalised', 'Agda.Builtin.Nat') == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_search_about_toplevel Normalised "Agda.Builtin.Nat")'

def test_solveAll():
  assert Commands('./test/test.agda').solveAll('Normalised') == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_solveAll Normalised)'

def test_solveOne():
  r = rangeBuilder('./test/test.agda', 6, 6, 8, 6, 6, 12)

  assert Commands('./test/test.agda').solveOne('Normalised', 0, r, 'Agda.Builtin.Nat') == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_solveOne Normalised 0 (intervalsToRange (Just (mkAbsolute "./test/test.agda")) [Interval  (Pn () 6 6 8 ) (Pn () 6 6 12 ) ]) "Agda.Builtin.Nat")'

def test_autoAll():
  assert Commands('./test/test.agda').autoAll() == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_autoAll)'

def test_autoOne():
  r = rangeBuilder('./test/test.agda', 6, 6, 8, 6, 6, 12)

  assert Commands('./test/test.agda').autoOne(0, r, 'Agda.Builtin.Nat') == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_autoOne 0 (intervalsToRange (Just (mkAbsolute "./test/test.agda")) [Interval  (Pn () 6 6 8 ) (Pn () 6 6 12 ) ]) "Agda.Builtin.Nat")'

def test_auto():
  r = Range()

  assert Commands('./test/test.agda').auto(0, r, '') == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_auto 0 noRange "")'

def test_infer_toplevel():
  assert Commands('./test/test.agda').infer_toplevel('Normalised', 'Agda.Builtin.Nat.Nat') == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_infer_toplevel Normalised "Agda.Builtin.Nat.Nat")'

def test_compute_toplevel():
  assert Commands('./test/test.agda').compute_toplevel('DefaultCompute', 'suc zero') == \
    'IOTCM "./test/test.agda" None Indirect (Cmd_compute_toplevel DefaultCompute "suc zero")'


