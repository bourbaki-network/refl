#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import *

from packages.package.package import Package

import yaml
from yaml import FullLoader as Loader
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class ReflProject:
  name: Optional[str] = None
  includes: List[str] = []
  dependencies: List[Package] = []

  @staticmethod
  def __call__(location: str) -> Optional[ReflProject]:
    with open(location) as loc:
      y = yaml.load(loc, Loader=Loader)

      name:str = y["name"] if "name" in y else None
      includes:List[str] = y["includes"] if "includes" in y else []
      dependencies:List[Any] = y["dependencies"] if "dependencies" in y else []

      return ReflProject(
        name=name,
        includes=includes,
        dependencies=dependencies
      )
    return None
