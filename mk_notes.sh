D=$(date +%m-%d-%Y.md)
# atom -w $D
vim $D
~/GitHub/projects/./notes_cat.py
git add *.md
git commit -m "Add $D"
# ~/GitHub/projects/./gits.sh
git push
