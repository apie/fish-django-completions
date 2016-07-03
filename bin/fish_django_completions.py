#!/usr/bin/env python3

import argparse
import sys

import django
from django.conf import settings
from django.core.management import get_commands, load_command_class


def clean_help(help):
    return help.replace("\n", "").replace('"', '\\"')


def generate_completions(filename=None, apps=None):
    commands, options = [], []
    dj_options = {}

    # configure django default settings
    settings.configure()

    # add extra apps
    if apps:
        settings.INSTALLED_APPS += tuple(apps)

    django.setup()

    dj_commands = get_commands()

    # generate subcommands
    for cmd in sorted(dj_commands):
        c = load_command_class(dj_commands[cmd], cmd)
        commands.append('complete -c $cmd -n \'__fish_use_subcommand\' -a %s -d "%s"' % (cmd, clean_help(c.help)))

        # collect all options in a list
        # to group them at the end
        parser = c.create_parser('', cmd)
        for opt in (parser._actions if c.use_argparse else parser.option_list):
            if not opt in dj_options:
                dj_options[opt] = []
            dj_options[opt].append(cmd)

    # generate options
    for opt in dj_options:
        s = '-s %s' % opt._short_opts[0][1:] if hasattr(opt, '_short_opts') and opt._short_opts else None
        l = '-l %s' % opt._long_opts[0][2:] if hasattr(opt, '_long_opts') and opt._long_opts else None
        if hasattr(opt, 'option_strings'):
            for opt_string in opt.option_strings:
                if len(opt_string) == 2:
                    s = '-s %s' % opt_string[1:]
                else:
                    l = '-l %s' % opt_string[2:]
        d = '-d "%s"' % clean_help(opt.help) if opt.help else None
        a = '-a "%s"' % ' '.join([str(choice) for choice in opt.choices]) if opt.choices else None
        options.append('complete -c $cmd -n \'__fish_seen_subcommand_from %s\' %s' % (
            ' '.join(dj_options[opt]),
            ' '.join(filter(None, [s, l, d, a]))
        ))

    if filename:
        f = open(filename, 'w')
    else:
        f = sys.stdout

    f.write(
        "# completion for django\n" +
        "function __fish_complete_django -d \"Completions for django\" --argument-names cmd" +
        "\n\tcomplete -x -c $cmd" +
        "\n\n\t"
    )
    f.write("\n\t".join(commands))
    f.write("\n\n\t")
    f.write("\n\t".join(sorted(options)))
    f.write("\nend")
    f.close()


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('-a', '--apps', nargs='+', type=str)
    p.add_argument('-f', '--filename', type=str)
    generate_completions(**vars(p.parse_args()))
