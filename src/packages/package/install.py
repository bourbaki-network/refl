#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import *

from packages.common import GitOptions, LocalOptions, Origin
from packages.package.package import Package
from util.log import Logging

log = Logging()()


class Install(Package):
  def __init__(
    self,
    name: str,
    version: str,
    description: str,
    # Where to get this package from
    origin: Origin,
    options: Union[GitOptions, LocalOptions],
    # Package's source directories to include
    source_dir: Optional[List[str]] = None,
    # Dependencies
    agda_version: Optional[str] = None,
    dependencies: Optional[List['Package']] = None,
    # Docs
    readme: Optional[str] = None,
    author: Optional[str] = None,
    author_email: Optional[str] = None,
    license: Optional[str] = None,
    # Tags
    tags: Optional[List[str]] = None,
    # Before and after install scripts
    install_script: Optional[str] = None,
    uninstall_script: Optional[str] = None,
  ):
    self.name = name
    self.version = version
    self.description = description

    self.origin = origin
    self.options = options

    self.source_dir = source_dir

    self.agda_version = agda_version
    self.dependencies = dependencies

    self.readme = readme
    self.author = author
    self.author_email = author_email
    self.license = license

    self.tags = tags

    self.install_script = install_script
    self.uninstall_script = uninstall_script

  def __call__(self):
    opts = self.options
    if type(opts) == GitOptions:
      self._git(opts.git_url, opts.head, opts.tag, opts.commit_hash)
    elif type(opts) == LocalOptions:
      self._local(opts.location)
    elif type(opts) == RemoteOptions:
      self._remote(opts.url)

  def _git(self, url: str, head: str = None, tag: str = None, commit_hash: str = None):

    return self

  def _local(self, location: str):

    return self

  def _remote(self, url: str):

    return self
