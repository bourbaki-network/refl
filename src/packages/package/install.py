#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import tempfile
from os import path
from typing import *

import filetype
import inquirer
from fuzzywuzzy import fuzz
from git import Repo
from pyunpack import Archive

from packages.common import GitOptions, LocalOptions, Origin, RemoteOptions
from packages.package.package import Package
from util.log import Logging

log = Logging()()

ARCHIVE_TYPES = [
  "application/x-lzip",
  "application/x-unix-archive",
  "application/x-compress",
  "application/zip",
  "application/x-tar",
  "application/x-rar-compressed",
  "application/gzip",
  "application/x-bzip2",
  "application/x-7z-compressed",
  "application/x-xz",
]


class Install(Package):
  def __init__(
    self,
    name: str,
    # Where to get this package from
    origin: Origin,
    options: Union[GitOptions, LocalOptions],
    # Properties
    version: Optional[str] = None,
    description: Optional[str] = None,
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
    self.origin = origin
    self.options = options
    self.version = version
    self.description = description
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

  def __call__(self, target_location: str):
    opts = self.options
    self.where = target_location
    if type(opts) == GitOptions:
      return self._git(opts.git_url, opts.head, opts.tag, opts.commit_hash)
    elif type(opts) == LocalOptions:
      return self._local(opts.local_url)
    elif type(opts) == RemoteOptions:
      return self._remote(opts.url)

  def _git(self, url: str, head: str = None, tag: str = None, commit_hash: str = None):
    # set target directory of install
    if head is not None:
      package_name = f"{self.name}-{head}"
      target_directory = path.join(self.where, package_name)
    elif tag is not None:
      package_name = f"{self.name}-{tag}"
      target_directory = path.join(self.where, package_name)
    elif commit_hash is not None:
      package_name = f"{self.name}-{commit_hash}"
      target_directory = path.join(self.where, package_name)
    else:
      package_name = f"{self.name}"
      target_directory = path.join(self.where, package_name)

    if path.exists(target_directory):
      log.warn(f"{self.name} is already installed at desired location.")
      return self

    tmpdir = tempfile.mkdtemp()
    log.info(f"Cloning {url} into {tmpdir}")
    cloned_repo = Repo.clone_from(url, tmpdir)

    # check out requested head / tag / commit
    if head is not None:
      cloned_repo.git.checkout(head)
      log.info(f"Checked out head {head}")
    if tag is not None:
      tag_ = [x for x in cloned_repo.tags if tag in x.name]
      assert len(tag_) == 1, f"Tag named {tag} not found in the repository"
      commit_hash = tag_[0].commit.hexsha
      log.info(f"Checking out tag {tag}")
    if commit_hash is not None:
      cloned_repo.git.checkout(commit_hash)
      log.info(f"Checked out commit {commit_hash}")

    shutil.move(tmpdir, target_directory)
    self.save(path.join(self.where, f"{package_name}.refl"))
    return self

  def _local(self, location: str):
    target_directory = path.join(self.where, f"{self.name}")
    if path.exists(target_directory):
      log.warn(f"{self.name} is already installed at {target_directory}.")
      return self

    # try to uncompress file if needed
    try:
      file_type = filetype.guess(location).mime
    except IsADirectoryError:
      file_type = ""
    print(file_type)
    if file_type in ARCHIVE_TYPES:
      tmpdir = tempfile.mkdtemp()
      Archive(location).extractall(tmpdir)
    else:
      tmpdir = location

    shutil.copytree(tmpdir, target_directory)
    self.save(path.join(self.where, f"{self.name}.refl"))
    return self


class Uninstall(Package):
  def __init__(self, name: str):
    self.name = name

  def __call__(self, where: str, non_exact: bool = True):
    self.where = where
    target_directory = path.join(self.where, f"{self.name}")
    if not path.exists(target_directory):
      log.error(f"{self.name} is not installed in the specified location: {target_directory}.")
      if non_exact:
        # search for deterministic matches, for packages custom installed from git etc
        log.warn("Trying to find non-exact matches...")
        dirs = os.listdir(self.where)
        deterministic = [x for x in dirs if self.name in x]
        deterministic = [x for x in deterministic if ".refl" not in x]
        if len(deterministic) > 0:
          questions = [inquirer.List(
            'version',
            message="Which version would you like to uninstall?",
            choices=deterministic,
          )]
          version = inquirer.prompt(questions)
          version = version['version']
          target_directory = path.join(self.where, version)
        # string-distance matching
        else:
          non_deterministic = [x for x in dirs if fuzz.ratio(self.name, x) > 70]
          non_deterministic = [x for x in non_deterministic if ".refl" not in x]
          if len(non_deterministic) <= 0:
            log.error(f"Could not find any matches for {self.name}")
          if len(non_deterministic) > 0:
            questions = [inquirer.List(
              'version',
              message="Which version would you like to uninstall?",
              choices=non_deterministic,
            )]
            version = inquirer.prompt(questions)
            version = version['version']
            target_directory = path.join(self.where, version)

    shutil.rmtree(target_directory, ignore_errors=True)
    if path.exists(f"{target_directory}.refl"):
      os.remove(f"{target_directory}.refl")
    return self
