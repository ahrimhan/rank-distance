#!/bin/sh
echo ""
echo "-------- Columba ---------"
wc -l columba*.dat
echo "--------------------------"
python rank-compare.py columba 0 0 0
python rank-compare.py columba 26 26 26
python rank-compare.py columba 53 53 53
python rank-compare.py columba 79 79 79
python rank-compare.py columba 0 0 26
python rank-compare.py columba 0 0 53
python rank-compare.py columba 0 0 79

echo ""
echo "-------- JEdit ---------"
wc -l jedit*.dat
echo "------------------------"
python rank-compare.py jedit 0 0 0
python rank-compare.py jedit 7 7 7
python rank-compare.py jedit 14 14 14
python rank-compare.py jedit 21 21 21
python rank-compare.py jedit 0 0 7
python rank-compare.py jedit 0 0 14
python rank-compare.py jedit 0 0 21

echo ""
echo "-------- jgit ---------"
wc -l jgit*.dat
echo "-----------------------"
python rank-compare.py jgit 0 0 0
python rank-compare.py jgit 26 26 26
python rank-compare.py jgit 53 53 53
python rank-compare.py jgit 79 79 79
python rank-compare.py jgit 0 0 26
python rank-compare.py jgit 0 0 53
python rank-compare.py jgit 0 0 79
