#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import *

from packages.common import GitOptions, LocalOptions, Origin


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
