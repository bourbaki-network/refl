#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import path
from typing import *

from .agda_lib import AgdaLib
from .install import Install

PackageMetadata = Union[AgdaLib]


class Package:
  origin: str = ""  # git / local / downloadable archive
  kind: str = ""  # global / user
  where: str = path.join(path.expanduser("~"), ".refl")  # link / path
  meta: PackageMetadata = None

  def __init__(self, origin: str = "git", kind: str = "user", where: str = None):
    assert origin in ["git", "local", "archive"], f"Unknown package origin {origin}"
    assert kind in ["user", "global"], f"Unknown package kind {kind}"

    self.origin = origin
    self.kind = kind
    self.where = where if where is not None else self.where

  def git(self, url: str, head: str = None, tag: str = None, commit_hash: str = None):
    install = Install(self.where)
    lib = install.git(url, head, tag, commit_hash)
    # TODO: add a better alternative config file
    self.meta = AgdaLib(lib)()
    return self

  def local(self, location: str):
    install = Install(self.where)
    lib = install.local(location)
    self.meta = AgdaLib(lib)()
    return self

  def remote(self, url: str):
    install = Install(self.where)
    lib = install.remote(url)
    self.meta = AgdaLib(lib)()
    return self

  def search(self, name: str):
    raise NotImplementedError("Search functionality is TODO")

  def publish(self, name: str, location: str):
    raise NotImplementedError("No central repo to publish to yet")

  def install_dependencies(self, meta: PackageMetadata):
    assert self.meta is not None, "Cannot install dependencies before parsing main package file"
    if isinstance(self.meta, AgdaLib):
      dependencies = self.meta.dependencies

    for dep in dependencies:
      pass
