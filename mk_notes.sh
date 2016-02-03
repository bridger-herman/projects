D=$(date +%m-%d-%Y.md)
atom -w $D
notes_cat
git add *.md
git commit -m "Add $D"
gits
git push
