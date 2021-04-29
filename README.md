<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## Table of Contents

- [refl](#refl)
  - [Install](#install)
- [Agda switcher](#agda-switcher)
  - [Install a new version of Agda](#install-a-new-version-of-agda)
  - [List available versions of Agda](#list-available-versions-of-agda)
- [Package manager](#package-manager)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# refl

A swiss army knife for working with [Agda](https://github.com/agda/agda).

- [refl](#refl)
  - [Install](#install)
- [Agda switcher](#agda-switcher)
  - [Install a new version of Agda](#install-a-new-version-of-agda)
  - [List available versions of Agda](#list-available-versions-of-agda)
- [Package manager](#package-manager)

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

```
python ./src/refl.py pkg install \
  --git \
  --url git@github.com:bourbaki-network/backend.git \
  --commit_hash  10bbc29ffa385db156b2d4f6884a2d3f8d02338c \
  --pwd
```
