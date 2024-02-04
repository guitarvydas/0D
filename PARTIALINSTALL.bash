#!/bin/bash
git init
git submodule add https://github.com/guitarvydas/0D
cp 0D/templates/* .
mv dot-gitignore .gitignore
npm install ohm-js yargs
sed -e "s/___/$1/g" <Makefile >temp
rm -f Makefile
mv temp Makefile
mv ___.drawio $1.drawio


