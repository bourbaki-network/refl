#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import *

from packages.package.package import Package

# import yaml
# from yaml import CLoader as Loader


@dataclass
class ReflProject:
  location: str
  name: Optional[str] = None
  package: Optional[Package] = None
  includes: Optional[list[str]] = None
  dependencies: Optional[list[Package]] = None

  # def __call__(self):
  #   with open(self.location) as loc:
  #     y = yaml.load(loc, Loader=Loader)
  #     self.package = y
