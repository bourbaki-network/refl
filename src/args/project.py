#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import *

import click
from click_help_colors import HelpColorsGroup
from giturlparse import parse as git_parse
from prompt_toolkit import prompt

from packages import GitOptions, InstallPackage, LocalOptions, Origin, Package, Project, UninstallPackage
from util.log import LOGLEVEL, Logging

log = Logging(LOGLEVEL)()

CONTEXT_SETTINGS = {
  'max_content_width': 200,
  # 'short_help_width':  400,
  'color': True
}


@click.group(cls=HelpColorsGroup,
             help_headers_color='magenta',
             help_options_color='cyan',
             chain=True,
             invoke_without_command=True,
             context_settings=CONTEXT_SETTINGS)
def project():
  """Manage Agda packages
  """
  pass


@project.command('install')
@click.option('-n', '--name', 'name', type=str, help='Name of the package')
@click.option('-g', '--git', 'git', type=bool, is_flag=True, help='Install this package from git')
@click.option('-l', '--local', 'local', type=bool, is_flag=True, help='Install this package from a local directory')
@click.option('-u', '--url', 'url', type=str, help='Git: url of the git repository')
@click.option('-h', '--head', 'head', type=str, help='Git: head of the git repository')
@click.option('-t', '--tag', 'tag', type=str, help='Git: tag of the git repository')
@click.option('-c', '--commit_hash', 'commit_hash', type=str, help='Git: commit_hash of the git repository')
@click.option('-g', '--location', 'location', type=str, help='Local: Location of the local package')
def install(
  name: str,
  git: bool = False,
  local: bool = False,
  url: str = "",
  head: str = "",
  tag: str = "",
  commit_hash: str = "",
  location: str = "",
):
  """Install package into project
  """
  p = Project.load("project.refl")
  if p.exists(name):
    log.info(f"Package {name} is already installed")
    return
  else:
    if local:
      assert name is not None, "Please pass the name of the package: --name <name>"
    if git and name is None:
      name = git_parse(url).repo if name is None else name
    target_location = ".refl"

    if git:
      origin = Origin.GIT
      options = GitOptions(git_url=url, head=head, commit_hash=commit_hash, tag=tag)
    elif local:
      origin = Origin.LOCAL
      options = LocalOptions(local_url=location)

    i = InstallPackage(name=name, origin=origin, options=options)
    i(target_location)
    p.add_dependency(
      name=name,
      git=git,
      local=local,
      url=url,
      head=head,
      tag=tag,
      commit_hash=commit_hash,
      location=location,
    )


@project.command('uninstall')
@click.option('-n', '--name', 'name', type=str, help='Name of the package')
@click.option('-s', '--soft', 'soft', type=bool, is_flag=True, help='Do a soft-string match')
def uninstall(name: str, user: bool = False, global_install: bool = False, pwd: bool = False, soft: bool = True):
  """Uninstall package from project
  """
  target_location = ".refl"
  p = Project.load("project.refl")
  if not p.exists(name):
    log.info(f"Package {name} is not installed")
    return
  u = UninstallPackage(name=name)
  removed = u(target_location, non_exact=soft)
  p.remove_dependency(name=name)


@project.command('update')
@click.option('-n', '--name', 'name', type=str, help='Name of the package')
@click.option('-g', '--git', 'git', type=bool, is_flag=True, help='Install this package from git')
@click.option('-l', '--local', 'local', type=bool, is_flag=True, help='Install this package from a local directory')
@click.option('-u', '--url', 'url', type=str, help='Git: url of the git repository')
@click.option('-h', '--head', 'head', type=str, help='Git: head of the git repository')
@click.option('-t', '--tag', 'tag', type=str, help='Git: tag of the git repository')
@click.option('-c', '--commit_hash', 'commit_hash', type=str, help='Git: commit_hash of the git repository')
@click.option('-g', '--location', 'location', type=str, help='Local: Location of the local package')
def update(
  name: str,
  git: bool = False,
  local: bool = False,
  url: str = "",
  head: str = "",
  tag: str = "",
  commit_hash: str = "",
  location: str = "",
):
  """Update a package
  """
  target_location = ".refl"
  p = Project.load("project.refl")

  dependencies = [x for x in p.project.dependencies if x.name == name]
  dependency: Optional[Package] = None
  if len(dependencies) > 0:
    dependency = dependencies[0]

  if dependency is None:
    log.error("Could not find the dependency, maybe try with --soft")
    return
  if not git and not local:
    git = Origin.parse(dependency.origin) is Origin.GIT
    local = Origin.parse(dependency.origin) is Origin.LOCAL
  if git:
    url = dependency.options["git_url"] if url is None else url
    name = git_parse(url).repo if name is None else name
    origin = Origin.GIT
    options = GitOptions(git_url=url, head=head, commit_hash=commit_hash, tag=tag)
  elif local:
    location = dependency.options["location"] if location is None else location
    assert name is not None, "Please pass the name of the package: --name <name>"
    origin = Origin.LOCAL
    options = LocalOptions(local_url=location)

  i = InstallPackage(name=name, origin=origin, options=options)
  i(target_location)

  # Uninstall the current package
  u = UninstallPackage(name=name)
  removed = u(target_location, non_exact=False)

  p.remove_dependency(name=name)
  p.add_dependency(
    name=name,
    git=git,
    local=local,
    url=url,
    head=head,
    tag=tag,
    commit_hash=commit_hash,
    location=location,
  )


@project.command('init')
def init():
  """Initialize a new project
  """
  name = prompt("Name of this project:")
  include = prompt("Name of the project's source directory: [default:src]")
  include = "src" if include is None or include == "" else include

  Project.init(".", name, [include])
