from enum import Enum
import subprocess
from typing import Tuple
from typing import Optional


import click
import typer
# from cleo.commands.command import Command
# from poetry.core.semver.version import Version
from semver import VersionInfo as Version


REPO = 'https://github.com/diadorer/bomb'


class Rule(str, Enum):
    prerelease = "prerelease"
    prepatch = "prepatch"
    preminor = "preminor"
    patch = "patch"
    minor = "minor"


def is_unstable(version: Version):
    return bool(version.prerelease)


class ShellError(Exception):
    ...


def shell(command: str, *args: Tuple[str], capture_output: bool = False) -> Optional[str]:
    out = subprocess.run(command.split(' ') + list(args), capture_output=capture_output)
    if out.returncode > 0:
        if capture_output:
            typer.echo(out.stdout or out.stderr)
        raise ShellError(f'Shell command returns code {out.returncode}')

    if capture_output:
        return out.stdout.decode()


def main(rule: Rule):
    try:
        shell('gh auth status')
    except ShellError:
        # Please, auth with command: \n${BOLD}gh auth login --web${RESET}
        typer.secho(
            f'Please, auth with command:\n' +
            # typer.style("good", fg=typer.colors.GREEN, bold=True)
            typer.style("gh auth login --web", bold=True)
        )
        return

    prev_version = Version.parse(
        shell('poetry version --short', capture_output=True)
    )

    package_name = shell('poetry version', capture_output=True).split(' ')[0]

    if is_unstable(prev_version) and rule in {Rule.prepatch, Rule.preminor}:
        typer.secho(
            f'\nYou should use "{Rule.prerelease}" command to update unstable releases',
            bold=True
        )
        return

    prerelease_prefix, is_prerelease = '', False
    if rule in {Rule.prerelease, Rule.prepatch, Rule.preminor}:
        prerelease_prefix, is_prerelease = 'PRE-', True

    if not click.confirm(f'Do you really want to {prerelease_prefix}release {package_name}', default=False):
        typer.echo("Ok...", err=True)
        return

    shell(f'poetry version {rule}')

    version = shell('poetry version --short', capture_output=True).rstrip()
    message = f':bomb: {prerelease_prefix}release {version}'

    shell(f'git checkout -b release/{version}')
    shell('git commit -am', message)
    shell(f'git push -u origin release/{version}')

    shell(f'gh pr create --title', message, '--body', f'''\
Great!
Please visit {REPO}/releases/edit/{version} to describe **release notes!**

Also you can find publishing task here {REPO}/actions/workflows/publish.yml''')

    current_branch = shell('git rev-parse --abbrev-ref HEAD', capture_output=True)
    gh_release_args = ('--prerelease', ) if is_prerelease else ()
    shell(
        f'gh release create "{version}"',
        '--title', message,
        '--notes', 'In progress...',
        '--target', current_branch,
        *gh_release_args,
    )
    shell('gh pr view --web')

    typer.secho('Done!', fg=typer.colors.GREEN, bold=True)

    # print('')
    # gh release create "$version" \
    #   --title "$message" \
    #   --notes "In progress..." \
    #    --target $CURRENT_BRANCH \
    #    $GH_CREATE_RELEASE_ARGS

# if [[ $PRERELEASE = true ]]; then
#   GH_CREATE_RELEASE_ARGS='--prerelease'
# fi
# gh release create "$version" \
#   --title "$message" \
#   --notes "In progress..." \
#    --target $CURRENT_BRANCH \
#    $GH_CREATE_RELEASE_ARGS
# gh pr view --web
#
# echo -e "\n${GREEN}${BOLD}Done!${RESET}"
#


#     gh pr create --title "$message" --body "# Great!
# Please visit $REPO/releases/edit/$version to describe **release notes!**
#
# Also you can find publishing task here $REPO/actions/workflows/publish.yml"
#
# CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
# if [[ $PRERELEASE = true ]]; then
#   GH_CREATE_RELEASE_ARGS='--prerelease'
# fi
# gh release create "$version" \
#   --title "$message" \
#   --notes "In progress..." \
#    --target $CURRENT_BRANCH \
#    $GH_CREATE_RELEASE_ARGS
# gh pr view --web
#
# echo -e "\n${GREEN}${BOLD}Done!${RESET}"

# parser = argparse.ArgumentParser()
# parser.add_argument(
#     'rule',
#     choices=['preminor', 'prepatch', 'prerelease', 'minor', 'patch'],
# )
#
# args = parser.parse_args()
# print(args.rule)
#
# package_name = subprocess.run('poetry version'.split(' '), capture_output=True).decode().split(' ')[0]
# prev_version = Version(subprocess.run('poetry version --short'.split(' '), capture_output=True).decode())
#
# if prev_version.is_unstable() and args.rule in {'preminor', 'prepatch'}:
#     raise ValueError('You should use "prerelease" command for update unstable releases')


if __name__ == "__main__":
    typer.run(main)