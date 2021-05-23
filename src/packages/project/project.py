#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from dataclasses import dataclass
from os import path
from typing import *

import yaml
from dataclasses_json import dataclass_json
from yaml import SafeDumper

from packages import GitOptions, LocalOptions, Origin, Package
# from packages.common import GitOptions, LocalOptions, Origin
# from packages.package.package import Package
from packages.project.agda_project import AgdaProject
from packages.project.refl_project import ReflProject
from util.log import LOGLEVEL, Logging

log = Logging(LOGLEVEL)()

SafeDumper.add_representer(type(None), lambda dumper, value: dumper.represent_scalar(u'tag:yaml.org,2002:null', ''))


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
      project = ReflProject()(where)
    except Exception as e:
      log.warning(f"Failed to parse project as a native Agda project, retrying as a refl project instead {e}")
      project = AgdaProject()(where)

    return Project(project)

  def exists(self, name: str) -> bool:
    if self.project is None:
      return False  # God damn optional types
    if self.project.dependencies is None:
      return False
    return name in [d.name for d in self.project.dependencies]

  def add_dependency(
    self,
    name: str,
    git: bool,
    local: bool,
    url: str,
    head: str,
    tag: str,
    commit_hash: str,
    location: str,
  ):
    origin: Origin = Origin.GIT if git else Origin.LOCAL
    if git:
      options = GitOptions(git_url=url, head=head, commit_hash=commit_hash, tag=tag)
    else:
      options = LocalOptions(local_url=location)
    dep = Package(name=name, origin=origin, options=options)

    if self.project:
      if self.project.dependencies is None:
        self.project.dependencies = []
      self.project.dependencies.append(dep)
      self.save("project.refl")

  def remove_dependency(self, name: str):
    if self.project and self.project.dependencies:
      self.project.dependencies = [d for d in self.project.dependencies if d.name != name]
    self.save("project.refl")

  def save(self, where: str):
    with open(where, 'w') as f:
      if self.project is None:
        log.error("Project is not initialized")
        return

      if self.project.dependencies is None:
        self.project.dependencies = []
      if self.project.includes is None:
        self.project.includes = []

      data = json.loads(self.project.to_json())  # type: ignore
      yaml.safe_dump(data, f, allow_unicode=True, default_flow_style=False, indent=4)

  @staticmethod
  def init(where: str, name: str, includes: List[str]) -> 'Project':
    p = Project(project=ReflProject(name=name, includes=includes))
    p.save(path.join(where, "project.refl"))
    return p
