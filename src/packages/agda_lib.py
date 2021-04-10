#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass

import yaml
from yaml import CLoader as Loader


@dataclass
class AgdaLib:
  dependencies: list[str]
  includes: list[str]
  name: str
  location: str

  def __call__(self):
    with open(self.location) as loc:
      y = yaml.load(loc, Loader=Loader)
      if "depend" in y:
        depends = self._remove_comment(y["depend"])
        self.dependencies = " ".join(depends.split())
      if "include" in y:
        includes = self._remove_comment(y["include"])
        self.includes = " ".join(includes.split())
      if "name" in y:
        self.name = self._remove_comment(y["name"])

  @staticmethod
  def _remove_comment(x: str) -> str:
    comment = x.find("--")
    if comment != -1:
      return x[comment:]
    else:
      return x
