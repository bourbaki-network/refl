#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from os import path
from typing import *

import yaml
from yaml import CLoader as Loader

from packages.common import LocalOptions, Origin
from packages.package.package import Package


@dataclass
class AgdaProject:
  location: str
  name: Optional[str] = None
  dependencies: Optional[list[Package]] = None
  includes: Optional[list[str]] = None

  def __call__(self):
    with open(self.location) as loc:
      y = yaml.load(loc, Loader=Loader)

      # Parse all (local) dependencies
      if "depend" in y:
        depends = self._remove_comment(y["depend"]).split()
        basepath = path.dirname(self.location)
        if len(depends) > 0:
          self.dependencies = []

        for dep in depends:
          dep_path = path.join(basepath, f"{dep}.agda-lib")
          self.dependencies += self._parse_dependencies(dep_path)

      # Parse all include directories
      if "include" in y:
        includes = self._remove_comment(y["include"])
        self.includes = " ".join(includes.split())

      # Parse project name
      if "name" in y:
        self.name = self._remove_comment(y["name"])

  def _parse_dependencies(self, file) -> List[Package]:
    with open(file) as dloc:
      p = yaml.load(dloc, Loader=Loader)

      # Recursively parse for all dependencies
      dependencies = []
      if "depend" in p:
        depends = self._remove_comment(p["depend"]).split()
        basepath = path.dirname(file)
        for dep in depends:
          dep_path = path.join(basepath, f"{dep}.agda-lib")
          pkgs = self._parse_dependencies(dep_path)
          dependencies += pkgs

      pkg = Package(
        name=self._remove_comment(p["name"]),
        version=None,
        description=None,
        origin=Origin.LOCAL,
        options=LocalOptions(basepath),
        source_dir=self._remove_comment(p["include"]).split(),
      )

      dependencies.append(pkg)
      return dependencies

  @staticmethod
  def _remove_comment(x: str) -> str:
    comment = x.find("--")
    if comment != -1:
      return x[:comment]
    else:
      return x
