# Advent of Code Repository

My solutions for [Advent of Code](https://adventofcode.com/).

#### Table of Contents

- [Details](#details)
- [Description](#description)
- [Language Configuration Notes](#language-configuration-notes)
  - [Dart](#dart)
  - [Go](#go)
  - [Python](#python)
  - [TypeScript](#typescript)

## Details

| Year          | Language   |
| ------------- | ---------- |
| [2016](2016/) | Dart       |
| [2017](2017/) | Python     |
| [2018](2018/) | Python     |
| [2019](2019/) | Python     |
| [2020](2020/) | Python     |
| [2021](2021/) | TypeScript |
| [2022](2022/) | Go         |
| [2023](2023/) | Dart       |
| [2024](2024/) | TypeScript |

## Description

This is a polyglot repo to practice algorithms, languages, and new ways of writing code with Advent of Code (AoC) as the backdrop. Each subfolder contains my solutions for a given year of AoC.

## Language Configuration Notes

This section outlines how the development environment is set up for each language.

### Dart

#### Install

Using [fvm](https://fvm.app/) to manage multiple Flutter / Dart versions

1. `fvm use --force`
1. Select `3.13.6` (figure out how to make this project specific)

#### Run

```console
fvm dart [path]

fvm dart run --enable-asserts [path]
```

### Go

#### Install

Using [goenv](https://github.com/syndbg/goenv) to manage mutiple Go versions

1. Install version specified in `.go-version` file

### Python

#### Install

1. Create and activate virtual environment for Python version specified in `.python-version`
2. `make python-install` to install dependencies.

#### Run

```console
$ ipython
%run 2020/day01_expense_report.py
```

#### Test

```console
pytest 2020/day01_expense_report.py
```

### TypeScript

#### Install

1. Install node version specified in `.nvmrc`
1. `npm install`

#### Run

- VSCode: `F5`
- Terminal: `npx ts-node [path-to-file]`

#### Test

Need to figure out how to do it in TS. What testing framework works is a good fit here?

#### Debug

- install [vscode-ts-debug](https://github.com/hagishi/vscode-ts-debug) and set up launch configuration
- if there are linking errors: `npm link ts-node`
- Use `debugger;` keyword to add breakpoint
- `F5` to start debugger

#### Notes

- [TypeScript new project setup instructions](https://www.digitalocean.com/community/tutorials/typescript-new-project)
- [Lint and Style Your TypeScript Code with ESLint and Prettier](https://moduscreate.com/blog/lint-style-typescript/)
