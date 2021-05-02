# -*- coding: utf-8 -*-
# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-

# from os import path
# from typing import *
# from urllib.parse import urlparse

# from packages.project.agda_project import AgdaProject
# from packages.common import Kind, Origin
# from packages.package.install import Install as InstallPackage
# from util.log import LOGLEVEL, Logging

# PackageMetadata = Union[AgdaProject]
# log = Logging(LOGLEVEL)()

# class Install:
#   origin: Origin = Origin.local
#   kind: Kind = Kind.user
#   where: str = path.join(path.expanduser("~"), ".refl")  # link / path
#   meta: PackageMetadata = None

#   def __init__(self, origin: str = "git", kind: str = "user", where: str = None):
#     assert isinstance(origin, Origin), f"Unknown package origin {origin}"
#     assert isinstance(kind, Kind), f"Unknown package kind {kind}"

#     self.origin = origin
#     self.kind = kind
#     self.where = where if where is not None else self.where

#   def git(self, url: str, head: str = None, tag: str = None, commit_hash: str = None):
#     install = InstallPackage(self.where)
#     lib = install.git(url, head, tag, commit_hash)
#     # TODO: add a better alternative config file
#     self.meta = AgdaProject(lib)()
#     return self

#   def local(self, location: str):
#     install = InstallPackage(self.where)
#     lib = install.local(location)
#     self.meta = AgdaProject(lib)()
#     return self

#   def remote(self, url: str):
#     install = InstallPackage(self.where)
#     lib = install.remote(url)
#     self.meta = AgdaProject(lib)()
#     return self

#   def search(self, name: str):
#     raise NotImplementedError("Search functionality is TODO")

#   def publish(self, name: str, location: str):
#     raise NotImplementedError("No central repo to publish to yet")

#   def install_dependencies(self, meta: PackageMetadata):
#     assert self.meta is not None, "Cannot install dependencies before parsing main package file"
#     if isinstance(self.meta, AgdaProject):
#       deps = []
#       for dep in self.dependencies:
#         # Try to guess the dependency type, if git, URL or local, try to fetch else give up
#         try:
#           kind_of_url = urlparse(dep)
#           if kind_of_url.scheme == "git":
#             origin = Origin.git
#           elif kind_of_url.scheme == "http" or kind_of_url.scheme == "https":
#             origin = Origin.remote
#           elif path.exists(dep):
#             origin = Origin.local
#           else:
#             raise Exception(f"Could not detect URL type of dependency {kind_of_url}")

#           dependency = {"url": dep, "origin": origin}
#           deps.append(dependency)
#         except Exception as e:
#           log.warning(f"Could not detect URL type of dependency {dependency}")

#       for dep in deps:
#         p = Package(dep["origin"], self.kind, self.where)
#         if self.kind == Kind.git:
#           p.git(dep["url"])
#         elif self.kind == Kind.remote:
#           p.remote(dep["url"])
#         elif self.origin == Kind.local:
#           p.local(dep["url"])
