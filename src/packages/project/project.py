#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from dataclasses import dataclass
from os import path
from typing import *

import yaml
from dataclasses_json import dataclass_json
from yaml import FullLoader as Loader

from packages.common import GitOptions, LocalOptions, Origin
from packages.package.package import Package
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

    try:
      project = AgdaProject(where)()
    except Exception as e:
      log.warning(f"Failed to parse project as a native Agda project, retrying as a refl project instead {e}")
      project = ReflProject(where)()

    return project

  # @classmethod
  # def init(where:str, name:str, includes:List[str]) -> 'Project':
  #    Project(

  #   )
