# About

This is a fast-start boilerplate repo for my various python projects.

## How to use

1. Create a new github repo from template and assign current repo as template
1. Select a branch you want to use as a starting point (more on this - in the next section)
1. Delete LICENCE file and cleanup README.md
1. Search using grep for 'placeholder' value and replace it with the name of your project: `grep -rnHi -I  "placeholder" .`
1. Use `find` tool to search for any folders or files which might have 'placeholder' name and change it to your project name
1. Delete `fastipy/` folder in the root (it might be used to automate stuff in the future)
1. I use some opinionated settings which will be outlined below...

## Branches

Branches are structured as a "directories tree" where each next "subdirectory" builds on top of previous one
by adding more specific choices / packages.

Currently I have following:

1. `master` - Baseline, using `uv` as a package manager, pytest/pytest-mock for testing + ruff/isort for linting
1. `django` - Use when you need plain django setup
1. `django/drf` - django with Django Rest Framework on top

### Django

Django branch:
* installs `python-dotenv`, `Django`, `psycopg2` packages
* sets up standard Django project structure with default settings
* overrides default Django user with custom defined one, without username

### Django DRF

Builds on top of Django and:
* adds `drf` package
* sets additional api configurations, like pagination, viewsets, rate-limiting and other general drf settings
