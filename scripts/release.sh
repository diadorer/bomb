#!/bin/bash

REPO='https://github.com/diadorer/bomb'

GREEN=`tput setaf 2`
YELLOW=`tput setaf 3`
BOLD=`tput bold`
RESET=`tput sgr0`

read -p "${BOLD}Do you really want to release${RESET} $(poetry version)? ${YELLOW}(y/д)${RESET} " -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[YyДд]$ ]]
then
    [[ "$0" = "$BASH_SOURCE" ]] && exit 1 || return 1 # handle exits from shell or function but don't exit interactive shell
fi

poetry version minor

version=$(poetry version --short)
message=":bomb: release $version"

git checkout -b release/$version
git commit -am "$message"
git push -u origin release/$version

gh pr create --title "$message" --body "# Great!
Please visit $REPO/releases/edit/$version to describe **release notes!**

Also you can find publishing task here $REPO/actions/workflows/publish.yml"

gh release create "$version" --title "$message" --notes ":TBD:" 
gh pr view --web

echo -e "\n${GREEN}${BOLD}Done!${RESET}"
# echo "${BOLD}Please add release notes — $REPO/releases/edit/$version${RESET}"

