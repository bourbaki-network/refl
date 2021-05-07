#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shutil
import tempfile
from dataclasses import dataclass
from os import path
from typing import *

from git import Repo

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


@dataclass
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
      return self._local(opts.location)
    elif type(opts) == RemoteOptions:
      return self._remote(opts.url)

  def _git(self, url: str, head: str = None, tag: str = None, commit_hash: str = None):
    # set target directory of install
    if head is not None:
      target_directory = path.join(self.where, f"{self.name}-{head}")
    elif tag is not None:
      target_directory = path.join(self.where, f"{self.name}-{tag}")
    elif commit_hash is not None:
      target_directory = path.join(self.where, f"{self.name}-{commit_hash}")
    else:
      target_directory = path.join(self.where, f"{self.name}")

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
    return self

  # def _local(self, location: str):
  #   target_directory = path.join(self.where, f"{location}")
  #   if self.installed(target_directory):
  #     return self._load_lib_file(target_directory)

  #   # try to uncompress file if needed
  #   file_type = filetype.guess(location)
  #   if file_type in ARCHIVE_TYPES:
  #     tmpdir = tempfile.mkdtemp()
  #     Archive(location).extractall(tmpdir)
  #   else:
  #     tmpdir = location

  #   shutil.move(tmp_dir, target_directory)
  #   return self

  # def _remote(self, url: str):
  #   target_directory = path.join(self.where, f"{identifier}")
  #   if self.installed(target_directory):
  #     return self._load_lib_file(target_directory)

  #   location = tempfile.mkdtemp()
  #   response = requests.get(url, stream=True)
  #   download_file = path.join(location, "downloaded.file")

  #   # download the file
  #   with open(download_file, "wb") as handle:
  #     for data in tqdm(response.iter_content()):
  #       handle.write(data)

  #     # try to uncompress file if needed
  #     file_type = filetype.guess(download_file)
  #     if file_type in ARCHIVE_TYPES:
  #       tmpdir = tempfile.mkdtemp()
  #       Archive(download_file).extractall(tmpdir)
  #     else:
  #       raise Exception("Unknown file type, could not uncompress")

  #     # check if there exists a ".agda-lib" file
  #     lib_file = glob.glob(path.join(tmpdir, "*.agda-lib"))
  #     assert len(lib_file) == 0, ".agda-lib file missing from library root"

  #     # move directory to `where`
  #   shutil.move(tmp_dir, target_directory)
  #   return self
