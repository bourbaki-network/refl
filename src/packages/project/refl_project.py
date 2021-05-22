#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import *

import yaml
from dataclasses_json import dataclass_json
from yaml import FullLoader as Loader

from packages.package.package import Package


@dataclass_json
@dataclass
class ReflProject:
  name: Optional[str] = None
  includes: Optional[List[str]] = None
  dependencies: Optional[List[Package]] = None

  @staticmethod
  def parse(data: Any) -> Optional['ReflProject']:
    if type(data) is not dict:
      return None
    try:
      return ReflProject(**data)
    except Exception as e:
      return None

  def __call__(self, location: str) -> Optional['ReflProject']:
    if self.dependencies is None:
      self.dependencies = []
    if self.includes is None:
      self.includes = []

    with open(location) as loc:
      y = yaml.load(loc, Loader=Loader)

      name: str = y["name"] if "name" in y else None
      includes: List[str] = y["includes"] if "includes" in y else []
      deps: List[Any] = y["dependencies"] if "dependencies" in y else []
      dependencies: List[Package] = [Package.parse(x) for x in deps]

      return ReflProject(name=name, includes=includes, dependencies=dependencies)
    return None
