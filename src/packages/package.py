#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# from typing import *


class Package:
  origin: str = ""  # git / local / downloadable archive
  kind: str = ""  # global / user
  where: str = ""  # link / path

  def __init__(self):
    pass

  def git(self, url: str):
    pass

  def local(self, path: str):
    pass

  def remote(self, url: str):
    pass

  def search(self, name: str):
    pass

  def publish(self, name: str):
    pass

  def _register(self, path: str):
    pass

  def _deregister(self, path: str):
    pass

  def _materialize(self):
    pass

  def resolve_dependencies(self):
    pass
