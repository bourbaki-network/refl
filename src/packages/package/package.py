#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from dataclasses import dataclass
from os import path
from typing import *

import yaml
from dataclasses_json import dataclass_json
from yaml import CLoader as Loader

from packages.common import GitOptions, LocalOptions, Origin
from util.log import Logging

log = Logging()()


@dataclass_json
@dataclass
class Package:
  # Basic info
  name: str
  version: str
  description: str
  # Where to get this package from
  origin: Origin
  options: Union[GitOptions, LocalOptions]
  # Package's source directories to include
  source_dir: Optional[List[str]] = None
  # Dependencies
  agda_version: Optional[str] = None
  dependencies: Optional[List['Package']] = None
  # Docs
  readme: Optional[str] = None
  author: Optional[str] = None
  author_email: Optional[str] = None
  license: Optional[str] = None
  # Tags
  tags: Optional[List[str]] = None
  # Before and after install scripts
  install_script: Optional[str] = None
  uninstall_script: Optional[str] = None

  @staticmethod
  def load(where: str):
    if path.exists(where) and path.isfile(where):
      with open(where) as f:
        y = yaml.load(f, Loader=Loader)
    else:
      log.error(f"Suppied path {where} either does not exist or is not a regular file.")

  def save(self, where: str):
    with open(where, 'w') as f:
      data = json.loads(self.to_json())  # type: ignore
      data = {k: v for k, v in data.items() if v is not None}
      yaml.dump(data, f, allow_unicode=True)
