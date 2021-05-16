#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from os import path

from tabulate import tabulate

from packages.common import GitOptions, LocalOptions
from packages.package.package import Package
from util.log import Logging

log = Logging()()


class ListPackage(Package):
  def __init__(self):
    pass

  def __call__(self, location: str):
    try:
      packages = os.listdir(path=location)
    except FileNotFoundError:
      log.info(f"No packages found in {location}")
      return
    packages = [x for x in packages if ".refl" in x]
    # print(packages)

    display = []
    for package in packages:
      p = Package.load(path.join(location, package))
      version = p.version
      if type(p.options) is GitOptions:
        version = p.options.git_url
      display.append([p.name, version, p.description, p.origin])
    log.info(f"Pakcages installed at {location}:")
    print(tabulate(display, headers=["Name", "Version", "Description", "Origin"], tablefmt="fancy_grid"))
