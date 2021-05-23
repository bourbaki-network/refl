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
from util.log import Logging

log = Logging()()


@dataclass_json
@dataclass
class Package:
  # Basic info
  name: str
  # Where to get this package from
  origin: Origin
  options: Union[GitOptions, LocalOptions]
  # Other attributes
  version: Optional[str] = None
  description: Optional[str] = None
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
  def parse(data: Any) -> Optional['Package']:
    if type(data) is not dict:
      return None
    try:
      return Package(**data)
    except Exception as e:
      log.warn(f"Could not parse package data {str(data)}")
      return None

  @staticmethod
  def load(where: str) -> Optional['Package']:
    if path.exists(where) and path.isfile(where):
      with open(where) as f:
        y = yaml.load(f, Loader=Loader)

        name: str = y["name"] if "name" in y else None
        version: Optional[str] = y["version"] if "version" in y else None
        description: Optional[str] = y["description"] if "description" in y else None
        source_dir: Optional[List[str]] = y["source_dir"] if "source_dir" in y else None
        agda_version: Optional[str] = y["agda_version"] if "agda_version" in y else None
        readme: Optional[str] = y["readme"] if "readme" in y else None
        author: Optional[str] = y["author"] if "author" in y else None
        author_email: Optional[str] = y["author_email"] if "author_email" in y else None
        license: Optional[str] = y["license"] if "license" in y else None
        tags: Optional[List[str]] = y["tags"] if "tags" in y else None
        install_script: Optional[str] = y["install_script"] if "install_script" in y else None
        uninstall_script: Optional[str] = y["uninstall_script"] if "uninstall_script" in y else None

        # entries with special typing needs
        origin: Origin = Origin.parse(y["origin"] if "origin" in y else "local")

        opt: Any = y["options"] if "options" in y else None
        options: Optional[Union[GitOptions, LocalOptions]] = None
        if origin is Origin.GIT:
          options = GitOptions.parse(opt)
        elif origin is Origin.LOCAL:
          options = LocalOptions.parse(opt)
        else:
          log.error(f"Origin {origin} supplied for package {name} is not supported")

        deps: List[Any] = y["dependencies"] if "dependencies" in y else []
        dependencies = [y for y in [Package.parse(x) for x in deps] if y is not None]

        return Package(
          name=name,
          version=version,
          description=description,
          origin=origin,
          options=options,
          source_dir=source_dir,
          agda_version=agda_version,
          dependencies=dependencies,
          readme=readme,
          author=author,
          author_email=author_email,
          license=license,
          tags=tags,
          install_script=install_script,
          uninstall_script=uninstall_script,
        )
    else:
      log.error(f"Suppied path {where} either does not exist or is not a regular file.")
      return None

  def save(self, where: str):
    with open(where, 'w') as f:
      data = json.loads(self.to_json())  # type: ignore
      yaml.safe_dump(data, f, allow_unicode=True, default_flow_style=False, indent=4)
