#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from dataclasses import dataclass
from os import path
from typing import *

import yaml
from dataclasses_json import dataclass_json

# from packages.common import GitOptions, LocalOptions, Origin
# from packages.package.package import Package
from packages.project.agda_project import AgdaProject
from packages.project.refl_project import ReflProject
from util.log import LOGLEVEL, Logging

log = Logging(LOGLEVEL)()


@dataclass_json
@dataclass
class Project:
  project: Optional[Union[AgdaProject, ReflProject]] = None

  @staticmethod
  def load(where: str) -> Optional['Project']:
    error = None
    project = None

    # TODO: Find a better way to figure out which type of project is it
    try:
      project = AgdaProject(where)()
    except Exception as e:
      log.warning(f"Failed to parse project as a native Agda project, retrying as a refl project instead {e}")
      project = ReflProject(where)()

    return project

  def save(self, where: str):
    with open(where, 'w') as f:
      if self.project is None:
        log.error("Project is not initialized")
        return

      if self.project.dependencies is None:
        self.project.dependencies = []
      if self.project.includes is None:
        self.project.includes = []

      data = json.loads(self.to_json())  # type: ignore
      data = {k: v for k, v in data.items() if v is not None}
      yaml.dump(data, f, allow_unicode=True)

  @staticmethod
  def init(where: str, name: str, includes: List[str]) -> 'Project':
    p = Project(project=ReflProject(name=name, includes=includes))
    p.save(path.join(where, f"{name}.refl"))
    return p
