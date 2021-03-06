from __future__ import print_function
import glob
import os
import subprocess
import sys


IGNORES = [
    'bin',
    '.git',
    '.gitignore',
    'ST2-User',
    'My Twighlight.tmTheme',
]


def shell_out(command_args, verbose=False):
    if verbose:
        print(' '.join(command_args))

    subprocess.call(command_args)


def backup_file(link_name, verbose=False):
    old_dotfiles_path = '/tmp/olddotfiles'

    if os.path.islink(link_name):
        shell_out(['rm', link_name], verbose=verbose)
    elif os.path.lexists(link_name):
        subprocess.call(['mkdir', '-p', old_dotfiles_path])
        shell_out(['mv', link_name, os.path.join(old_dotfiles_path, os.path.basename(link_name))], verbose=verbose)


def link_st2(home_directory, verbose=False):
    filename = os.path.normpath(os.path.realpath('ST2-User'))
    link_name = os.path.join(home_directory, 'Library', 'Application Support', 'Sublime Text 2', 'Packages', 'User')
    backup_file(link_name, verbose=verbose)
    shell_out(['ln', '-s', filename, link_name], verbose=verbose)

    theme_name = os.path.normpath(os.path.realpath('My Twilight.tmTheme'))
    link_name = os.path.join(home_directory, 'Library', 'Application Support', 'Sublime Text 2', 'Packages', 'Color Scheme - Default', 'My Twilight.tmTheme')
    backup_file(link_name, verbose=verbose)
    shell_out(['ln', '-s', theme_name, link_name], verbose=verbose)


def setup_dotfiles(home_directory, verbose=False):
    dotfile_pattern = os.path.join('.*')
    dotfile_files = glob.glob(dotfile_pattern)
    setup_symlinks(home_directory, dotfile_files, verbose=verbose)

    regular_pattern = os.path.join('*')
    regular_files = glob.glob(regular_pattern)
    setup_symlinks(home_directory, regular_files, verbose=verbose)

    create_gitingore(home_directory, verbose=verbose)
    link_st2(home_directory, verbose=verbose)


def setup_symlinks(home_directory, files, verbose=False):
    for filename in files:
        ignored = False

        for ignore_me in IGNORES:
            if filename == ignore_me:
                ignored = True
                break

        if ignored:
            continue

        full_path = os.path.normpath(os.path.realpath(filename))
        link_name = os.path.join(home_directory, os.path.basename(filename))

        backup_file(link_name, verbose=verbose)
        shell_out(['ln', '-s', full_path, link_name], verbose=verbose)


def create_gitingore(home_directory, verbose=False):
    gitignore_path = os.path.join(home_directory, '.gitignore')
    backup_file(gitignore_path, verbose=verbose)

    gitignore_file = open(gitignore_path, 'w')
    gitignore_file.write('*.pyc\n')
    gitignore_file.write('.DS_Store\n')
    gitignore_file.close()


def usage():
    print("Usage: python bin/install.py [-v]")
    print("Please run from the top-level ``dotfiles`` directory.")
    sys.exit(1)


if __name__ == "__main__":
    verbose = False

    if len(sys.argv) > 2:
        usage()

    if not sys.argv[0].startswith('bin/'):
        usage()

    if len(sys.argv) == 2 and sys.argv[1] in ['-v', '--verbose']:
        verbose = True

    home_directory = os.path.expanduser('~')
    setup_dotfiles(home_directory, verbose=verbose)
