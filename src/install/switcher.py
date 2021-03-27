#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import platform
import shutil
from ftplib import FTP
from os import path

import inquirer
from pyunpack import Archive

from util import download_url, unzip
from util.log import LOGLEVEL, Logging

log = Logging(LOGLEVEL)()


class VersionSwitcher:
  def __init__(self, root: str, install_root: str = "/usr/bin"):
    self.root = root
    self.install_root = install_root

  def latest(self) -> str:
    versions = self._get_available_versions()
    versions.reverse()

    for latest in versions:
      ret = self._download(latest)
      if ret:
        destination = f"{self.root}/{latest.replace('.deb', '')}"
        self._switch(destination)
        return latest
    return None

  def install(self):
    questions = [
      inquirer.List(
        'version',
        message="Which version would you like to install?",
        choices=self._get_available_versions(),
      )
    ]
    version = inquirer.prompt(questions)
    version = version['version']
    print(version)
    ret = self._download(version)
    if ret:
      destination = f"{self.root}/{version.replace('.deb', '')}"
      self._switch(destination)

  def _switch(self, to: str):
    log.info(f"Switching Agda version to {to}")
    final_path = path.join(self.install_root, 'agda')
    try:
      os.remove(final_path)
    except Exception as e:
      log.error(f'Path {final_path} does not exist')
    os.symlink(path.abspath(to), final_path)

  def _download(self, filename: str) -> bool:
    try:
      filepath = path.join(self.root, filename)
      destination = f"{self.root}/{filename.replace('.deb', '')}"

      download_url(f'http://ftp.de.debian.org/debian/pool/main/a/agda/{filename}', filepath)
      unzip(filepath)
      os.mkdir(path.join(self.root, '.tmp'))
      Archive(filepath).extractall('.tmp')
      data_tar = path.join('.tmp', 'data.tar')
      Archive(data_tar).extractall('.tmp')
      shutil.move(".tmp/usr/bin/agda", destination)
      shutil.rmtree('.tmp')
      os.remove(filepath)
      return True
    except Exception as e:
      return False

  @staticmethod
  def _get_available_versions(arch: str = "") -> list[str]:
    if arch == "":
      arch = platform.architecture()[1]
    system = platform.system()
    machine = platform.machine()
    if machine == 'x86_64':
      machine = 'amd64'

    if system == 'Linux':
      ftp = FTP('ftp.us.debian.org')
      ftp.login()
      ftp.cwd('debian/pool/main/a/agda/')
      files = ftp.nlst()
      files = [f for f in files if 'agda-bin_' in f]
      files = [f for f in files if machine in f]
      print(files)
      return files
    # TODO: Mac and windows support?
    # elif system = 'Darwin':
    # elif  arch = 'WindowsPE' && system = 'Windows':
    else:
      log.error(f"Not configured for usage on this architecture {platform.architecture()}")
      return []
