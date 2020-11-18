#!/bin/bash
rm -rf dist
pyinstaller nydus.spec
if [ $? -ne 0 ]; then
    exit 1
fi
sudo chmod -R 777 dist
cp -r src/plugins dist
mkdir dist/data
mkdir dist/data/logs
find dist | grep -E "(__pycache__|\.gitignore$)" | xargs rm -rf

# remove f2habitbreaker, the overlays cannot be
# above sc2 running in wine so it doesnt work
rm -rf dist/plugins/F2HabitBreaker

exit 0
