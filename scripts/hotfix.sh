#!/bin/bash

GREEN=`tput setaf 2`
BOLD=`tput bold`
RESET=`tput sgr0`

poetry version patch

version=$(poetry version --short)
message=":bomb: release $version"

git commit -am "$message"
gh release create "$version" --title "$message" --notes ":TBD:" 

echo -e "\n${GREEN}${BOLD}Done!${RESET}"
echo "${BOLD}Please add release notes — https://github.com/diadorer/bomb/releases/edit/$version${RESET}"

