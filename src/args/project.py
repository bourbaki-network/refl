#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
from click_help_colors import HelpColorsGroup
from giturlparse import parse as git_parse
from prompt_toolkit import prompt

from packages import GitOptions, InstallPackage, LocalOptions, Origin, Project, UninstallPackage
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
@click.option('-r', '--remote', 'remote', type=bool, is_flag=True, help='Install this package after downloading as an archive')
@click.option('-u', '--url', 'url', type=str, help='Git: url of the git repository')
@click.option('-h', '--head', 'head', type=str, help='Git: head of the git repository')
@click.option('-t', '--tag', 'tag', type=str, help='Git: tag of the git repository')
@click.option('-c', '--commit_hash', 'commit_hash', type=str, help='Git: commit_hash of the git repository')
@click.option('-g', '--location', 'location', type=str, help='Local: Location of the local package')
@click.option('-g', '--path', 'path', type=str, help='Remote: URL of the remote package')
@click.option('-g', '--identifier', 'identifier', type=str, help='Remote: Name / identifier of the package')
def install(
  name: str,
  git: bool = False,
  local: bool = False,
  remote: bool = False,
  url: str = "",
  head: str = "",
  tag: str = "",
  commit_hash: str = "",
  location: str = "",
  path: str = "",
  identifier: str = "",
):
  """Install package into project
  """
  p = Project.load("project.refl")
  if p.exists(name):
    log.info(f"Package {name} is already installed")
    return
  else:
    if local or remote:
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
def update(
  user: bool = False,
  global_install: bool = False,
  pwd: bool = False,
):
  """Update all project dependencies
  """
  pass


@project.command('init')
def init():
  """Initialize a new project
  """
  name = prompt("Name of this project:")
  include = prompt("Name of the project's source directory: [default:src]")
  include = "src" if include is None or include == "" else include

  Project.init(".", name, [include])
