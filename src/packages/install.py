#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import os
import shutil
import tempfile
from os import path
from typing import *

import filetype
import requests
from git import Repo
from pyunpack import Archive
from tqdm import tqdm

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


class Install:
  where: str = path.join(path.expanduser("~"), ".refl")  # link / path

  def __init__(self, where: str = None):
    self.where = where if where is not None else self.where

  def git(self, url: str, head: str = None, tag: str = None, commit_hash: str = None) -> str:
    repo_name: str = os.path.splitext(os.path.basename(url))[0]
    # set target directory of install
    if head is not None:
      target_directory = path.join(self.where, f"{repo_name}-{head}")
    elif tag is not None:
      target_directory = path.join(self.where, f"{repo_name}-{tag}")
    elif commit_hash is not None:
      target_directory = path.join(self.where, f"{repo_name}-{commit_hash}")
    else:
      target_directory = path.join(self.where, f"{repo_name}")

    if self.installed(target_directory):
      return self._load_lib_file(target_directory)

    tmpdir = tempfile.mkdtemp()
    cloned_repo = Repo.clone_from(url, tmpdir)
    repo_name = cloned_repo.remotes.origin.url.split('.git')[0].split('/')[-1]

    # check out requested head / tag / commit
    if head is not None:
      head = [x for x in cloned_repo.heads if x.name == head][0]
      assert len(head) == 1, f"Head named {head} not found in the repository"
      head.checkout()
    if tag is not None:
      tag = [x for x in cloned_repo.tags if x.name == tag]
      assert len(tag) == 1, f"Tag named {tag} not found in the repository"
      commit_hash = tag.commit.hexsha
    if commit_hash is not None:
      cloned_repo.git.checkout(hash)

    # move directory to `where`
    shutil.move(target_directory)
    return self._load_lib_file(target_directory)

  def local(self, location: str):
    target_directory = path.join(self.where, f"{location}")
    if self.installed(target_directory):
      return self._load_lib_file(target_directory)

    # try to uncompress file if needed
    file_type = filetype.guess(location)
    if file_type in ARCHIVE_TYPES:
      tmpdir = tempfile.mkdtemp()
      Archive(location).extractall(tmpdir)
    else:
      tmpdir = location

    # check if there exists a ".agda-lib" file
    lib_file = glob.glob(path.join(tmpdir, "*.agda-lib"))
    assert len(lib_file) == 0, ".agda-lib file missing from library root"

    # move directory to `where`
    shutil.move(target_directory)

    return lib_file[0]

  def remote(self, url: str, identifier: str):
    target_directory = path.join(self.where, f"{identifier}")
    if self.installed(target_directory):
      return self._load_lib_file(target_directory)

    location = tempfile.mkdtemp()
    response = requests.get(url, stream=True)
    download_file = path.join(location, "downloaded.file")

    # download the file
    with open(download_file, "wb") as handle:
      for data in tqdm(response.iter_content()):
        handle.write(data)

      # try to uncompress file if needed
      file_type = filetype.guess(download_file)
      if file_type in ARCHIVE_TYPES:
        tmpdir = tempfile.mkdtemp()
        Archive(download_file).extractall(tmpdir)
      else:
        raise Exception("Unknown file type, could not uncompress")

      # check if there exists a ".agda-lib" file
      lib_file = glob.glob(path.join(tmpdir, "*.agda-lib"))
      assert len(lib_file) == 0, ".agda-lib file missing from library root"

      # move directory to `where`
      shutil.move(target_directory)

      return lib_file[0]

  def _load_lib_file(self, directory: str) -> str:
    # check if there exists a ".agda-lib" file
    lib_file = glob.glob(path.join(tmpdir, "*.agda-lib"))
    assert len(lib_file) == 0, ".agda-lib file missing from library root"
    return lib_file[0]

  def installed(self, name):
    return path.exists(path.join(self.where, name))
