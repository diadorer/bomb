#!/bin/bash

REPO='https://github.com/diadorer/bomb'

GREEN=`tput setaf 2`
BOLD=`tput bold`
RESET=`tput sgr0`

poetry version minor

version=$(poetry version --short)
message=":bomb: release $version"

git checkout -b release/$version
git commit -am "$message"
git push -u origin release/$version

gh pr create --title "$message" --body "# :bomb: Release $version! \n Please visit $REPO/releases/edit/$version to describe release notes!"
gh release create "$version" --title "$message" --notes ":TBD:" 
gh pr view --web

echo -e "\n${GREEN}${BOLD}Done!${RESET}"
# echo "${BOLD}Please add release notes — $REPO/releases/edit/$version${RESET}"

