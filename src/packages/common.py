#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from enum import Enum
from typing import *


class Origin(Enum):
  GIT = "git"
  LOCAL = "local"
  REMOTE = "remote"


class Kind(Enum):
  USER = "user"
  EVERYONE = "everyone"
  LOCAL = "local"


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
