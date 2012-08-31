import os
import shlex
import argparse
from collections import defaultdict

BASH_HISTORY = None
NUM_COMMANDS = 10

def _start():
    global BASH_HISTORY
    try:
        BASH_HISTORY = os.environ['HISTFILE']
    except KeyError:
        BASH_HISTORY = '%s/.bash_history' % os.environ['HOME']

    parse_args()
    command_counts = defaultdict(int)

    with open(BASH_HISTORY, 'r') as history_file:
        for command in history_file:
            unpiped_commands = [unpiped_command.strip() for unpiped_command in command.split('|')]
            for unpiped_command in unpiped_commands:
                count_command(command_counts, unpiped_command)

    sorted_counts = sort_counts(command_counts)
    report_counts(sorted_counts)
    
    aliases = find_aliases([count[0] for count in sorted_counts])
    report_aliases(aliases, sorted_counts)


def count_command(count_dict, command):
    token_string = ''
    try:
        tokens = shlex.split(command)
    except ValueError:  # thrown for unclosed quotations
        tokens = command.split()

    for token in tokens:
        if token.startswith('-'):
            break

        if token == '.':
            token = 'source'

        token_string = ' '.join([token_string, token]) if token_string else token
        count_dict[token_string] += 1


def sort_counts(command_counts):
    return sorted(command_counts.iteritems(), key=lambda (k,v): (v,k), reverse=True)[:NUM_COMMANDS]


def report_counts(sorted_counts):
    print 'Your top %s most used commands:' % NUM_COMMANDS
    for index, count_tuple in enumerate(sorted_counts):
        print ' #%s:\t%s (%s)' % (index+1, count_tuple[0], count_tuple[1])
    print '\n',


def find_aliases(commands):
    alias_dict = {}
    for command in commands:
        try:
            tokens = shlex.split(command)
        except ValueError:  # thrown for unclosed quotations
            tokens = command.split()

        # if a command is more than one token, add a prefix for each token
        prefix = ''
        if len(tokens) > 1:
            for token in tokens[:-1]:
                prefix = ''.join([prefix, token[0]])

        # append as many characters to the alias as needed to make it unique
        # note that key errors can't occur here, since the actual commands are unique
        char_index = 0
        alias = prefix
        append_to_alias = True
        while append_to_alias:
            # don't add . or / to the alias
            while tokens[-1][char_index] == '.' or tokens[-1][char_index] == '/':
                char_index += 1
            alias = ''.join([alias, tokens[-1][char_index]])
            char_index += 1
            append_to_alias = alias in alias_dict.itervalues()
        
        alias_dict[command] = alias

    return alias_dict


def report_aliases(aliases, command_counts):
    total_chars_saved = 0
    
    print 'Here are some aliases, and the amount of characters typed you would save per alias:'
    for command_tuple in command_counts:
        command = command_tuple[0]
        command_alias = aliases[command]

        chars_saved = len(command) - len(command_alias)
        times_used = command_tuple[1]

        print ' %s -> %s (%s characters / %s total)' % (command, command_alias, chars_saved, chars_saved*times_used)
      
        # for the total saved count, ensure that we don't count commands that start the same multiple times
        # TODO: rework storage of commands to reduce complexity of this operation?
        for other_command in command_counts:
            if other_command[0] == command: continue
            if other_command[0].startswith(command):
                times_used -= other_command[1]

        total_chars_saved += chars_saved*times_used
    
    with open(BASH_HISTORY, 'r') as history_file:
        history_length = len(history_file.read())

    percentage_of_total = (float(total_chars_saved) / history_length) * 100
    print '\nHowever, if all the aliases were in place, you would save %s characters in all - \
or about %s%% of your total bash history.' % (total_chars_saved, percentage_of_total)


def parse_args():
    global NUM_COMMANDS
    arg_parser = argparse.ArgumentParser(description='Reports most used bash commands.', add_help=False)
    arg_parser.add_argument('-n', type=int, required=False, dest='num_commands', metavar='NUM')
    args = arg_parser.parse_args()
    if args.num_commands and args.num_commands > 0:
        NUM_COMMANDS = args.num_commands        


if __name__ == '__main__':
    _start()

