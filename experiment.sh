#!/bin/sh
echo ""
echo "-------- Columba ---------"
wc -l columba*.dat
echo "--------------------------"
echo ""
python rank-compare.py columba 0 yes
python rank-compare.py columba 26 no
python rank-compare.py columba 53 no
python rank-compare.py columba 79 no

echo ""
echo "-------- JEdit ---------"
wc -l jedit*.dat
echo "------------------------"
echo ""
python rank-compare.py jedit 0 yes
python rank-compare.py jedit 7 no
python rank-compare.py jedit 14 no
python rank-compare.py jedit 21 no

echo ""
echo "-------- jgit ---------"
wc -l jgit*.dat
echo "-----------------------"
echo ""
python rank-compare.py jgit 0 yes
python rank-compare.py jgit 26 no
python rank-compare.py jgit 53 no
python rank-compare.py jgit 79 no
