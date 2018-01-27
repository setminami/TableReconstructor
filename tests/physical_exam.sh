#!/usr/bin/env sh
TEST_TMPDIR=./tests/tmp
if [ ! -d $TEST_TMPDIR ]; then
  # no -p because './test' must be
  mkdir -p $TEST_TMPDIR
else
  echo 'workspace OK'
fi

if [ $TRAVIS == true ]; then
  echo 'TRAVIS BUILD RUNNING...'
  RIGHT_DATA_DIR=./tests/data/travis_right_data
else
  echo 'LOCAL BUILD RUNNING...'
  RIGHT_DATA_DIR=./tests/data/local_right_data
fi

TESTINGOUTS_EXT=.test.txt

# ----------------------------------------------------------
TEST=$TEST_TMPDIR/h$TESTINGOUTS_EXT
RIGHT_DATA=$RIGHT_DATA_DIR/h.txt
echo 'test help'
./jsonica/jsonica.py -h > $TEST
diff $RIGHT_DATA $TEST
if [ $? -eq 1 ]; then
  echo '🔴  test has fail! "-h"'
  exit 1
else
  echo '✅  pass!'
fi

# generate test
# ----------------------------------------------------------
TEST=$TEST_TMPDIR/g-h$TESTINGOUTS_EXT
RIGHT_DATA=$RIGHT_DATA_DIR/g-h.txt
echo 'test g -h'
./jsonica/jsonica.py g -h > $TEST
diff $RIGHT_DATA $TEST

if [ $? -eq 1 ]; then
  echo '🔴  test has fail! "g -h"'
  exit 1
else
  echo '✅  pass!'
fi

# ----------------------------------------------------------
echo 'test gen -h'
./jsonica/jsonica.py gen -h > $TEST
diff $RIGHT_DATA $TEST
if [ $? -eq 1 ]; then
  echo '🔴  test has fail! "gen -h"'
  exit 1
else
  echo '✅  pass!'
fi
echo 'test generate -h'
./jsonica/jsonica.py generate -h > $TEST
diff $RIGHT_DATA $TEST
if [ $? -eq 1 ]; then
  echo '🔴  test has fail! "generate -h"'
  exit 1
else
  echo '✅  pass!'
fi
# ----------------------------------------------------------

TEST=$TEST_TMPDIR/g-i$TESTINGOUTS_EXT
RIGHT_DATA=$RIGHT_DATA_DIR/g-i.txt
echo 'test generate defaults'
./jsonica/jsonica.py g > $TEST
diff $RIGHT_DATA $TEST
if [ $? -eq 1 ]; then
  echo '🔴  test has fail! "g"'
  exit 1
else
  echo '✅  pass!'
fi

TEST=$TEST_TMPDIR/g-i$TESTINGOUTS_EXT
echo 'test generate -i'
./jsonica/jsonica.py g -i ./Samples/cheatsheet.xlsx > $TEST
diff $RIGHT_DATA $TEST

if [ $? -eq 1 ]; then
  echo '🔴  test has fail! "g -i ./Samples/cheatsheet.xlsx"'
  exit 1
else
  echo '✅  pass!'
fi

TEST=$TEST_TMPDIR/g-i-o-of$TESTINGOUTS_EXT
RIGHT_DATA=$RIGHT_DATA_DIR/g-i-o-of.txt
./jsonica/jsonica.py g -i ./Samples/cheatsheet.xlsx -o ./output -of tsv:./output > $TEST
diff $RIGHT_DATA $TEST

if [ $? -eq 1 ]; then
  echo '🔴  test has fail! "g -i ./Samples/cheatsheet.xlsx -o ./output -of tsv:./output"'
  exit 1
else
  echo '✅  pass!'
fi

TEST=$TEST_TMPDIR/g-o--of$TESTINGOUTS_EXT
RIGHT_DATA=$RIGHT_DATA_DIR/g-o--of.txt
echo 'test generate -o -'
./jsonica/jsonica.py g -o - -of tsv:./output > $TEST
diff $RIGHT_DATA $TEST

if [ $? -eq 1 ]; then
  echo '🔴  test has fail! "g -o - -of tsv:./output"'
  exit 1
else
  echo '✅  pass!'
fi

TEST=$TEST_TMPDIR/g-o--of-hr_2$TESTINGOUTS_EXT
RIGHT_DATA=$RIGHT_DATA_DIR/g-o--of-hr_2.txt
echo 'test generate -o - -hr 2'
./jsonica/jsonica.py g -o - -of tsv:./output -hr 2 > $TEST
diff $RIGHT_DATA $TEST

if [ $? -eq 1 ]; then
  echo '🔴  test has fail! "g -o - -of tsv:./output -hr 2"'
  exit 1
else
  echo '✅  pass!'
fi

TEST=$TEST_TMPDIR/g-o--of-hr_4$TESTINGOUTS_EXT
RIGHT_DATA=$RIGHT_DATA_DIR/g-o--of-hr_4.txt
echo 'test generate -o - -hr 4'
./jsonica/jsonica.py g -o - -of tsv:./output -hr 4 > $TEST
diff $RIGHT_DATA $TEST

if [ $? -eq 1 ]; then
  echo '🔴  test has fail! "g -o - -of tsv:./output -hr 4"'
  exit 1
else
  echo '✅  pass!'
fi

# initialize tests
TEST=$TEST_TMPDIR/i-h$TESTINGOUTS_EXT
RIGHT_DATA=$RIGHT_DATA_DIR/i-h.txt
echo 'test initialize -h'
./jsonica/jsonica.py i -h > $TEST
diff $RIGHT_DATA $TEST
if [ $? -eq 1 ]; then
  echo '🔴  test has fail! "i -h"'
  exit 1
else
  echo '✅  pass!'
fi

./jsonica/jsonica.py init -h > $TEST
diff $RIGHT_DATA $TEST
if [ $? -eq 1 ]; then
  echo '🔴  test has fail! "init -h"'
  exit 1
else
  echo '✅  pass!'
fi

./jsonica/jsonica.py initialize -h > $TEST
diff $RIGHT_DATA $TEST
if [ $? -eq 1 ]; then
  echo '🔴  test has fail! "initialize -h"'
  exit 1
else
  echo '✅  pass!'
fi

TEST=$TEST_TMPDIR/i-tx$TESTINGOUTS_EXT
RIGHT_DATA=$RIGHT_DATA_DIR/i-tx.txt
echo 'test init -tx'
./jsonica/jsonica.py i -tx ./template.xlsx > $TEST
diff $RIGHT_DATA $TEST
if [ $? -eq 1 ]; then
  echo '🔴 test has fail! "initialize -tx ./template.xlsx" phase1/3'
  exit 1
else
  echo '✅  pass!'
fi

TEST=$TEST_TMPDIR/template$TESTINGOUTS_EXT
RIGHT_DATA=$RIGHT_DATA_DIR/template.txt
SVTEST=$TEST_TMPDIR/_sv
./jsonica/jsonica.py g -i ./template.xlsx -o - -of tsv:$SVTEST -hr 2 > $TEST
diff $RIGHT_DATA $TEST
if [ $? -eq 1 ]; then
  echo '🔴 test has fail! "initialize -tx ./template.xlsx" phase2/3'
  exit 1
else
  # openpyxlによる再作成の問題 binary書き換わるため
  # おそらく新規に作成し直している
  # ToDo: ここだけのためにgo導入のおしつけはあり得ないのでAdHoc対応のまま保留
  rm ./template.xlsx
  echo '✅  pass!'
fi
TEST=$SVTEST/template.xlsx
RIGHT_DATA=$RIGHT_DATA_DIR/_sv/template.xlsx
diff $RIGHT_DATA $TEST
if [ $? -eq 1 ]; then
  echo '🔴 test has fail! "initialize -tx ./template.xlsx" phase3/3'
  exit 1
else
  # Memo: 空なので意味があるとはいえない
  echo '✅  pass!'
fi

# final Debug無し コミット後にテストが前提
git diff --exclude *.xlsx --exit-code
if [ $? -eq 1 ]; then
  echo '🔸 Found difference'
else
  echo '✅  all green'
fi
