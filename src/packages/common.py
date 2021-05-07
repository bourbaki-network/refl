#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from enum import Enum
from typing import *


class Origin(Enum):
  GIT = 1
  LOCAL = 2
  REMOTE = 3


class Kind(Enum):
  USER = 1
  EVERYONE = 2
  LOCAL = 3


@dataclass
class GitOptions:
  git_url: str
  head: Optional[str]
  commit_hash: Optional[str]
  tag: Optional[str]


@dataclass
class LocalOptions:
  local_url: str


@dataclass
class RemoteOptions:
  url: str
