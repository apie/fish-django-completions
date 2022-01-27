# Django Fish Completions

[![Build Status](https://travis-ci.com/apie/fish-django-completions.svg?branch=master)](https://travis-ci.com/apie/fish-django-completions)

A management command to generate Django completions for Fish Shell.

## Quickstart

1. Install this package to your Python environment:

  ```sh
  pip install fish-django-completions
  ```

2. Add it to the `INSTALLED_APPS` setting in your Django settings file.

  ```python
  INSTALLED_APPS += ["fish_django_completions"]
  ```

3. Run `./manage.py fish_completions --enable` to generate the Fish completion
   script. It will be stored in `$XDG_CONFIG_HOME/fish/completions/manage.py.fish`

4. Whenever you complete one of `./manage.py`, `django-admin` or
   `django-admin.py` the Fish completion script will fetch completions for
   your project via `manage.py fish_completions`.


## Known Issues

* `python manage.py` cant be completed at the moment, use `./manage.py`

