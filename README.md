<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## Table of Contents

- [refl](#refl)
  - [Install](#install)
- [Agda switcher](#agda-switcher)
  - [Install a new version of Agda](#install-a-new-version-of-agda)
  - [List available versions of Agda](#list-available-versions-of-agda)
- [Package manager](#package-manager)
  - [Install package](#install-package)
    - [Location](#location)
      - [In present working directory](#in-present-working-directory)
      - [For current user](#for-current-user)
      - [Globally](#globally)
    - [Options](#options)
      - [From git with specific commit hash](#from-git-with-specific-commit-hash)
      - [From git with specific tag](#from-git-with-specific-tag)
      - [From git with specific commit head or branch](#from-git-with-specific-commit-head-or-branch)
  - [Uninstall Package](#uninstall-package)
    - [Location](#location-1)
      - [From current directory](#from-current-directory)
      - [From current user's packages](#from-current-users-packages)
      - [Globally](#globally-1)
    - [Options](#options-1)
      - [Uninstall packages specifically](#uninstall-packages-specifically)
      - [Uninstall packages by package name](#uninstall-packages-by-package-name)
      - [Uninstall packages by approx matches](#uninstall-packages-by-approx-matches)
  - [List Installed Packages](#list-installed-packages)
  - [Project operations](#project-operations)
    - [Initialize a new project](#initialize-a-new-project)
    - [Install a package](#install-a-package)
      - [From git](#from-git)
      - [From a local location](#from-a-local-location)
    - [Update a package](#update-a-package)
      - [Pull a new version from github](#pull-a-new-version-from-github)
      - [Pull a new version from local](#pull-a-new-version-from-local)
    - [Uninstall a package](#uninstall-a-package)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# refl

A swiss army knife for working with [Agda](https://github.com/agda/agda).

## Install

Refl is hosted on [pypi](https://pypi.org). To install the latest release of refl:

Global install:

```bash
pip install refl
```

Install for current user only:

```bash
pip install refl --user
```

# Agda switcher

## Install a new version of Agda

```bash
refl version switch
```

## List available versions of Agda

```bash
refl version list
```

# Package manager

## Install package

### Location

#### In present working directory

```bash
refl pkg install --git --url git@github.com:marcelosousa/smtlib.git --pwd
```

#### For current user

```bash
refl pkg install --git --url git@github.com:marcelosousa/smtlib.git --user
```

#### Globally

```bash
refl pkg install --git --url git@github.com:marcelosousa/smtlib.git --global
```

### Options

#### From git with specific commit hash

```bash
refl pkg install \
  --git \
  --url git@github.com:marcelosousa/smtlib.git \
  --commit_hash c152c6fe59a0546c88e048f1ea50d193b997ef15 \
  --pwd
```

#### From git with specific tag

```bash
refl pkg install \
  --git \
  --url git@github.com:gallais/agdarsec.git \
  --tag v0.3.0 \
  --pwd
```

#### From git with specific commit head or branch

```bash
refl pkg install \
  --git \
  --url git@github.com:pcapriotti/agda-base.git \
  --head computational-isos \
  --pwd
```

## Uninstall Package

### Location

#### From current directory

```bash
refl pkg uninstall --git --name smtlib --pwd
```

#### From current user's packages

```bash
refl pkg uninstall --git --name smtlib --user
```

#### Globally

```bash
refl pkg uninstall --git --name smtlib --global
```

### Options

#### Uninstall packages specifically

```bash
refl pkg uninstall --name smtlib-c152c6fe59a0546c88e048f1ea50d193b997ef15 --pwd
```

#### Uninstall packages by package name

```bash
refl pkg uninstall --name agda-categories --pwd
```

#### Uninstall packages by approx matches

```bash
refl pkg uninstall --name aga-cegries --pwd --soft
```

## List Installed Packages

```bash
refl pkg list
```

## Project operations

### Initialize a new project

Creates a new project file for tracking dependencies. It is an interactive command.

```bash
refl project init
> Name of this project:
> Name of the project's source directory: [default:src]
```

### Install a package

#### From git

```bash
refl project install\
  --name smtlib \
  --git \
  --url git@github.com:marcelosousa/smtlib.git \
  --commit_hash c152c6fe59a0546c88e048f1ea50d193b997ef15
```

#### From a local location

```bash
refl project install\
  --local \
  --name agda-categories \
  --location ~/src/hott/agda-categories
```

### Update a package

#### Pull a new version from github

```bash
refl project update --name smtlib --head master
```

#### Pull a new version from local

```bash
refl project update --name agda-categories --location ~/src/hott/agda-categories-new
```

### Uninstall a package

```
refl project uninstall --name agda-categories
```
