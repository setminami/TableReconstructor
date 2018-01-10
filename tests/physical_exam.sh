#!/usr/bin/env sh
TEST_TMPDIR=./tests/tmp
if [ ! -d $TEST_TMPDIR ]; then
  # no -p because './test' must be
  mkdir TEST_TMPDIR
fi

RIGHT_DATA_DIR=./tests/right_data

# generate test
TESTINGOUTS_EXT=.test.txt
# ----------------------------------------------------------
TEST=$TEST_TMPDIR/h$TESTINGOUTS_EXT
RIGHT_DATA=$RIGHT_DATA_DIR/h.txt

./jsonica/jsonica.py g -h > $TEST
diff $RIGHT_DATA $TEST

if [ $? -eq 1 ]; then
  echo 'test has fail! "g -h"'
  exit 1
else
  echo 'pass!'
fi

# ----------------------------------------------------------

./jsonica/jsonica.py gen -h > $TEST
diff $RIGHT_DATA $TEST
if [ $? -eq 1 ]; then
  echo 'test has fail! "gen -h"'
  exit 1
else
  echo 'pass!'
fi

./jsonica/jsonica.py generate -h > $TEST
diff $RIGHT_DATA $TEST
if [ $? -eq 1 ]; then
  echo 'test has fail! "generate -h"'
  exit 1
else
  echo 'pass!'
fi
# ----------------------------------------------------------

TEST=$TEST_TMPDIR/g-i$TESTINGOUTS_EXT
RIGHT_DATA=$RIGHT_DATA_DIR/g-i.txt
./jsonica/jsonica.py g -i ./Samples/cheatsheet.xlsx > $TEST
diff $RIGHT_DATA $TEST

if [ $? -eq 1 ]; then
  echo 'test has fail! "g -i"'
  exit 1
else
  echo 'pass!'
fi

TEST=$TEST_TMPDIR/g-i$TESTINGOUTS_EXT
./jsonica/jsonica.py g > $TEST
diff $RIGHT_DATA $TEST

if [ $? -eq 1 ]; then
  echo 'test has fail! "g"'
  exit 1
else
  echo 'pass!'
fi

TEST=$TEST_TMPDIR/g-i$TESTINGOUTS_EXT
RIGHT_DATA=$RIGHT_DATA_DIR/g-i.txt
./jsonica/jsonica.py g -i ./Samples/cheatsheet.xlsx > $TEST
diff $RIGHT_DATA $TEST

if [ $? -eq 1 ]; then
  echo 'test has fail! "g -i ./Samples/cheatsheet.xlsx"'
  exit 1
else
  echo 'pass!'
fi

TEST=$TEST_TMPDIR/g-i-o-of$TESTINGOUTS_EXT
RIGHT_DATA=$RIGHT_DATA_DIR/g-i-o-of.txt
./jsonica/jsonica.py gen -i ./Samples/cheatsheet.xlsx -o ./output -of tsv:./output > $TEST
diff $RIGHT_DATA $TEST

if [ $? -eq 1 ]; then
  echo 'test has fail! "gen -i ./Samples/cheatsheet.xlsx -o ./output -of tsv:./output"'
  exit 1
else
  echo 'pass!'
fi

git diff --exit-code
if [ $? -eq 1 ]; then
  echo 'Found difference'
  exit 1
else
  echo 'all green'
fi
