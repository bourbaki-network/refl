#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from enum import Enum
from typing import *


class Origin(Enum):
  git = 1
  local = 2
  remote = 3


class Kind(Enum):
  user = 1
  everyone = 2
  local = 3


@dataclass
class GitOptions:
  git_url: str
  https_url: Optional[str]
  head: Optional[str]
  commit_hash: Optional[str]
  tag: Optional[str]


@dataclass
class LocalOptions:
  local_url: str
