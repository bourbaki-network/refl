#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import *

from packages.project.agda_project import AgdaProject
from packages.project.refl_project import ReflProject
from util.log import LOGLEVEL, Logging

log = Logging(LOGLEVEL)()


class Project:
  project: Optional[Union[AgdaProject, ReflProject]] = None

  def __init__(file):
    error = None
    try:
      self.project = AgdaProject(file)()
    except Exception as e:
      log.warning(f"Failed to parse project as a native Agda project, retrying as a refl project instead {e}")
      self.project = ReflProject(file)()
