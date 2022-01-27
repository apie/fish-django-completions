#!/usr/bin/env python3
import logging
import os
import sys
from pathlib import Path
from shutil import copy

from django.core.management import get_commands, load_command_class
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-f', '--filename', type=str)
        parser.add_argument(
            '--enable',
            help="Place completion script in Fish config folder",
            action="store_true"
        )

    def handle(self, filename, **options):
        if options.get("enable"):
            file = enable_completions()
            self.stdout.write(self.style.SUCCESS(f'Successfully saved {file}'))
        else:
            generate_completions(filename)


def enable_completions() -> str:
    """Copy `manage.py.fish` to Fish's completion directory."""
    xdg_config_home = Path(os.getenv("XDG_CONFIG_HOME", "~/.config"))
    completions_folder = (xdg_config_home / "fish" / "completions").expanduser()
    completions_folder.mkdir(parents=True, exist_ok=True)
    target = completions_folder / "manage.py.fish"

    completion_file =  (Path(__file__).parents[2] / "manage.py.fish").resolve()
    copy(completion_file, target)
    return target



def clean_help(h):
    return h.replace("\n", "").replace('"', '\\"')


def generate_completions(filename, **options):
    commands, options = set(), set()
    dj_options = {}
    dj_commands = get_commands()

    # generate subcommands
    for cmd in dj_commands:
        if cmd == 'pipchecker':
            continue  # Broken
        try:
            c = load_command_class(dj_commands[cmd], cmd)
        except AttributeError as e:  # Some mgmt cmds are util files and not really commands
            logger.exception(e)
            continue

        commands.add('complete -c manage.py -n \'__fish_use_subcommand\' -a %s -d "%s"' % (cmd, clean_help(c.help)))
        # collect all options in a list
        # to group them at the end
        parser = c.create_parser('', cmd)
        dj_options[cmd] = parser._option_string_actions

    # generate options
    for cmd, opts in dj_options.items():
        for _, opt in opts.items():
            short = long = None
            if hasattr(opt, 'option_strings'):
                for opt_string in opt.option_strings:
                    if len(opt_string) == 2:
                        short = '-s %s' % opt_string[1:]
                    else:
                        long = '-l %s' % opt_string[2:]
            description = '-d "%s"' % clean_help(opt.help) if hasattr(opt, 'help') and opt.help else None
            alternatives = '-a "%s"' % ' '.join([str(choice) for choice in opt.choices]) if hasattr(opt, 'choices') and opt.choices else None
            options.add('complete -c manage.py -n \'__fish_seen_subcommand_from %s\' %s' % (
                cmd,
                ' '.join(filter(None, [short, long, description, alternatives]))
            ))

    with open(filename, 'w') if filename else sys.stdout as f:
        f.write("complete --erase -c manage.py\n")
        f.write("complete -x -c manage.py\n")
        f.write("complete -c django-admin --wraps manage.py\n")
        f.write("complete -c django-admin.py --wraps manage.py\n")
        f.write("\n".join(sorted(commands)))
        f.write("\n".join(sorted(options)))


if __name__ == '__main__':
    import django
    import argparse
    from django.conf import settings
    p = argparse.ArgumentParser()
    p.add_argument('-a', '--apps', nargs='+', type=str)
    p.add_argument('-f', '--filename', type=str)
    kwargs = vars(p.parse_args())
    # configure django default settings
    settings.configure()
    if kwargs['apps']:
        settings.INSTALLED_APPS += tuple(kwargs['apps'])
    django.setup()
    generate_completions(**kwargs)
