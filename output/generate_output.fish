#!/usr/bin/fish
for version in 2.2 3.0 3.1
	virtualenv --python=python3.7 venv$version
	eval venv$version/bin/python -m pip install --upgrade Django~=$version
	eval venv$version/bin/python ../fish_django_completions.py --filename django$version/__fish_complete_django.fish
end
