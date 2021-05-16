#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from enum import Enum
from typing import *


class Origin(Enum):
  GIT = "git"
  LOCAL = "local"
  REMOTE = "remote"
  NONE = "none"

  @staticmethod
  def parse(data: str) -> 'Origin':
    d = data.upper()
    try:
      return Origin[d]
    except Exception as e:
      return Origin.NONE


class Kind(Enum):
  USER = "user"
  EVERYONE = "everyone"
  LOCAL = "local"
  NONE = "none"

  @staticmethod
  def parse(data: str) -> 'Kind':
    d = data.upper()
    try:
      return Kind[d]
    except Exception as e:
      return Kind.NONE


@dataclass
class GitOptions:
  git_url: str
  head: Optional[str]
  commit_hash: Optional[str]
  tag: Optional[str]

  @staticmethod
  def parse(data: Any) -> Optional['GitOptions']:
    if type(data) is not dict:
      return None
    try:
      return GitOptions(**data)
    except Exception as e:
      return None


@dataclass
class LocalOptions:
  local_url: str

  @staticmethod
  def parse(data: Any) -> Optional['LocalOptions']:
    if type(data) is not dict:
      return None
    try:
      return LocalOptions(**data)
    except Exception as e:
      return None


@dataclass
class RemoteOptions:
  url: str

  @staticmethod
  def parse(data: Any) -> Optional['RemoteOptions']:
    if type(data) is not dict:
      return None
    try:
      return RemoteOptions(**data)
    except Exception as e:
      return None
