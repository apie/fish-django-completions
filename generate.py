from django.core.management import get_commands, load_command_class
from django.conf import settings

settings.configure()

head = """# completion for django
function __fish_complete_django -d "Completions for django and its aliases" --argument-names cmd
\techo "load django completions for: $cmd"
\tcomplete -x -c $cmd
\techo $cmd
"""

foot = """
end
"""

dj_commands = get_commands()
dj_options = {}

commands = []
options = []

for cmd in dj_commands.keys():
    c = load_command_class(dj_commands[cmd], cmd)
    commands.append('complete -c $cmd -n \'__fish_use_subcommand\' -a %s -d "%s"' % (cmd, c.help.replace("\n", "").replace('"', '\\"')))
    for opt in c.option_list:
        if not opt in dj_options:
            dj_options[opt] = []
        dj_options[opt].append(cmd)

for opt in dj_options.keys():
    s = '-s %s' % opt._short_opts[0][1:] if opt._short_opts else None
    l = '-l %s' % opt._long_opts[0][2:] if opt._long_opts else None
    d = '-d "%s"' % opt.help.replace("\n", "").replace('"', '\\"') if opt.help else None
    a = '-a "%s"' % ' '.join(opt.choices) if opt.choices else None
    options.append('complete -c $cmd -n \'__fish_seen_subcommand_from %s\' %s' % (
        ' '.join(dj_options[opt]),
        ' '.join(filter(None, [s, l, d, a]))
    ))

f = open('django.fish', 'w')
f.write(head)
f.write("\n\n\t")
f.write("\n\t".join(commands))
f.write("\n\n\t")
f.write("\n\t".join(options))
f.write(foot)
f.close()
