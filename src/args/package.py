#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import click
from giturlparse import parse as git_parse

from packages import GitOptions, InstallPackage, LocalOptions, Origin, RemoteOptions

CONTEXT_SETTINGS = {
  'max_content_width': 200,
  # 'short_help_width':  400,
  'color': True
}


@click.group(chain=True, invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
def pkg():
  """Manage Agda packages
  """
  pass


@pkg.command('install')
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
@click.option('-g', '--user', 'user', type=bool, is_flag=True, help='Install for user, typically at ~/.refl')
@click.option('-g', '--global', 'global_install', is_flag=True, type=bool, help='Install globally, typically at /usr/lib/refl')
@click.option('-g', '--pwd', 'pwd', type=bool, is_flag=True, help='Install for current project, typically at ./.refl')
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
  user: bool = False,
  global_install: bool = False,
  pwd: bool = False,
):
  """Install package
  """
  name = git_parse(url).repo if name is None else name
  target_location = os.path.join(os.path.expanduser("~"), ".refl")
  if global_install:
    target_location = "/usr/lib/refl"
  if pwd:
    target_location = "./.refl"

  if git:
    origin = Origin.GIT
    options = GitOptions(git_url=url, head=head, commit_hash=commit_hash, tag=tag)
  elif local:
    origin = Origin.LOCAL
    options = LocalOptions(local_url=location)
  elif remote:
    origin = Origin.REMOTE
    options = RemoteOptions(url=path)

  i = InstallPackage(name=name, origin=origin, options=options)

  i(target_location)


@pkg.command('uninstall')
@click.option('-n', '--name', 'name', type=str, help='Package name')
def uninstall():
  """Uninstall package
  """
  pass


@pkg.command('search')
@click.option('-n', '--name', 'name', type=str, help='Package name')
def search():
  """Search for a package (WIP)
  """
  raise NotImplementedError()
