#!/bin/bash
fix_date=""
amend=0

# Gather arguments
while getopts ":a:f:" opt; do
    case "$opt" in
        a) amend=1;;
        f) fix_date=$OPTARG;;
        h) echo "-a  Amend to current date";
           echo "-f  Fix date (yyyy-mm-dd)";;
    esac
done

# Create the necessary directories
for d in src tmp tex pdf
do
    if [ \! -d $d ]
    then
        mkdir -p $d
    fi
done


# Go back and fix notes from a particular day
if [[ $fix_date != "" ]]
then
    name=$fix_date
else
    name=$(date +%Y-%m-%d)
fi

fancy_date=$(date +"%A, %B %d, %Y" -d $name)
work_dir=${PWD##*/}
modified_files=""

# Only create the new file if it doesn't already exist
if [ ! -f src/$name.md ]
then
    echo "% Notes from $name" >> src/$name.md
    echo "% Bridger Herman" >> src/$name.md
    echo "% $fancy_date" >> src/$name.md
fi

# Edit the notes
vim src/$name.md
modified_files+="src/$name.md"

# Join the markdown files
rm -f src/notes.md
for f in $(ls src)
do
    printf "\n\n---\n" >> tmp/notes.md
    cat src/$f >> tmp/notes.md
done
cp tmp/notes.md src/notes.md
modified_files+=" src/notes.md"

# Convert the Markdown into LaTeX
pandoc -o tex/$name.tex --template template_$work_dir.tex src/$name.md

# Generate the LaTeX PDF
cd tmp
pdflatex ../tex/$name.tex
mv $name.pdf ../pdf
modified_files+=" pdf/$name.pdf"

# Join all the PDFs from the notes
cd ../pdf
pdfjoin $(ls)

# Create the joined PDF of all notes
mv *-joined.pdf ../notes.pdf
modified_files+=" notes.pdf"

# Clean up
cd ..
rm -r tmp tex

# Add to git
git add $modified_files
git status

# Push to GitHub
read -p "Look good? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    push_opts=""

    if [ $amend -eq 1 ]
    then
        git commit --amend
        push_opts="-f"
    else
        git commit -m "Update notes for $name"
    fi

    git push $push_opts
fi

