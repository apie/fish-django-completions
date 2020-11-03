# Django Fish Completions

[![Build Status](https://travis-ci.com/apie/fish-django-completions.svg?branch=master)](https://travis-ci.com/apie/fish-django-completions)

A script to generate Django completions for Fish Shell.

## Quickstart

1. Determine if you want the pre-generated file or if you want to generate your own:
	- If you just want the general completions, download the file for your Django version and save it to the fish functions:
	```
	wget https://raw.githubusercontent.com/apie/fish-django-completions/master/output/django2.2/__fish_complete_django.fish -O ~/.config/fish/functions/__fish_complete_django.fish
	```
	- If you want completions for Django and also for your own management commands, copy the file `fish_django_completions.py` into the folder with your other management commands. Then run:
	```
	./manage.py fish_django_completions -f ~/.config/fish/functions/__fish_complete_django.fish
	```
2. Append the following to `~/.config/fish/config.fish` to activate the completions:
```
    __fish_complete_django django-admin.py
    __fish_complete_django manage.py
```

## Known Issues

* `python manage.py` cant be completed at the moment, use `./manage.py`

## License

The [original repository](https://github.com/Duncaen/fish-django-completions) did not specify a license. I am however publicing it under the MIT license.
