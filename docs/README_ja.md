[![Waffle.io - Columns and their card count](https://badge.waffle.io/setminami/TableReconstructor.png?columns=all)](https://waffle.io/setminami/TableReconstructor?utm_source=badge)

# JSON_XLSX_Manager
## What I wanna do and Where advantage
  - テストや設定データの中で興味があるところのみにこだわり、平易に管理したい
    - 雑音を排除し、必要条件を満たすことに集中できる
  - Excelなど抽象表現からJSON, Yaml, md...etcの具象表現を振り分け自動生成したい
    - 抽象表現を建てることにより、∃具象表現のみを必要とするだけで他は必要になるまで出力の必要がなくなる
    - 抽象的に興味の対象を記述することで、未認知含め∀具象表現はそれぞれの下層レイヤでの限定都合で整形することに集中できる
  - 小粒度ファイルを多人数にmap, reduceして作業の集中と並列化を図る
    - 例えば、初期化したexcelからsheetをばらして配って各自入力、回収時finalizeすると巨大なJSONファイルが出力されるとか。
    - 詳細仕様は一部の人間だけが握って正確に記述することで、各自は担当する部位だけ知っていればすむような、知識の分散管理を図りたい

## excel構築と編集
  - git管理をする場合は必ずxlsx形式であること
  - 1階層1sheetとして管理すること
  - root itemを示すsheetは`root`をシート名とすること
    - `-r sheet名`で指定、`-r`がない場合のみxlsxは`root`という名前のsheetを持たなければならない
  - カラムはキーとして解釈されること
    - 各カラムには、該当itemについてのjsonschemaを**コメントで**書き入れる
    - xlsx初期化コマンドで、yamlからjsonschemaの設定内容が読み込まれ、上述コメントが埋め込まれたテンプレートファイルを生成する
    - schemaで'type':'array'の場合はsheet内全てのitem配列、'object'の場合はsheet**最後のrow**をobjectとして追加される
  - 1階層下にitemを持たせる場合は別sheetとし、item名カラムにsheetへのハイパーリンクを張ること
    - 1階層下を配列にしたくない場合はカラム行とコンテンツ1行とする
    - 1階層下が配列の場合は、コンテンツ行が2行以上存在させることで対応する
  - cell内に文字列で`sheet://sheet名`とすることにより個別sheetを指すこと
    - Excelからいちいちメニューを選んで別シートへのハイパーリンクを張るのが思いのほかめんどくさい
    - 操作ライブラリでのhyperlink記述がExcel記入方法、OSにより揺れることがあるため、リンクする際は手動とする
    - `sheet://`以降をそのままsheet名とするため、encode上whitespaceを許す
    - typoが見つかった場合は、コマンドのエラーとして上げる see. エラー
  - Excelの仕様に振られないため、余計なマクロは極力上書きしない

## Sample Files
  - META descriptor and `table_reconstructor.py gen -of csv -hr 2` output sample
    - [xlsx & genarated json](https://github.com/setminami/TableReconstructor/tree/master/Samples)
  - local git環境に設定調整を強要しないxlsx git管理の模索
    - [xlsx git management (trial)](https://github.com/setminami/TableReconstructor/tree/master/output/cheatsheet.xlsx)
  - xlsx初期化用template yamlファイル
    - [template.yaml](https://github.com/setminami/TableReconstructor/blob/master/template.yaml)
  - xlsxに基づいて出力される生成json についてのjsonschema (TBD)

## Usage Sample
```
# generate
$ table_reconstructor.py gen -i ./Samples/cheatsheet.xlsx -o ./output -of tsv:./output
Analyzing... /Users/set/Desktop/Github/JSON_XLSX_Manager/Samples/cheatsheet.xlsx
Output json Success ➡️ ./output/cheatsheet.json

$ table_reconstructor.py gen -i ./Samples/cheatsheet.xlsx -o ./output/test.json -of tsv:./output
Analyzing... /Users/set/Desktop/Github/JSON_XLSX_Manager/Samples/cheatsheet.xlsx
Output json Success ➡️ ./output/test.json

$ table_reconstructor.py g -o - -of tsv:./output
[{"color": "fff000", "title": "Anchors", "items": [{"sign": "^", "desc-en": "Matches at the start of string or start of line if multi-line mode is enabled. Many regex implementations have multi-line mode enabled by default."}, {"sign": "$", "desc-en": "Matches at the end of string or end of line if multi-line mode is  enabled. Many regex implementations have multi-line mode enabl....

$ table_reconstructor.py g -i ./Samples/cheatsheet.xlsx -hr 2 -o - -of tsv:./output
[
  {
    "color": "fff000",
    "items": [
....

# check silent outputs
$ ls ./output
cheatsheet.json	cheatsheet.xlsx	test.json

$ ls ./output/cheatsheet.xlsx/
items-Anchors.tsv		items-Modifiers.tsv		items-bracketEx.tsv
items-Case Modifiers.tsv	items-POSIX-CHAR.tsv		items-spchar.tsv
items-CharClass.tsv		items-Quantifiers.tsv		root.tsv
items-Groups.tsv		items-assertion.tsv

# ☝️ can see on github.io like...
# https://github.com/setminami/TableReconstructor/tree/master/output/cheatsheet.xlsx
```

## Appendix.1 Errors
sys.exit by each index.

```python
errors = ['OK',
            'sheets link not found.', 'schema not found.', # 1, 2
            'root sheet not found.', 'Unrecognized item type were found.', # 3, 4
            'Unknown accumulator!', 'Output json has failed.', # 5, 6
            'Unsupported table filetype found.', 'setting yaml file not found']
```

## Appendix 2. Help
```
$ table_reconstructor.py -h
usage: table_reconstructor.py [-h] [-v] [-e {python built-in codec}]  ...

generate complex structure JSON with analyzing META descripted file.

positional arguments:
                        sub-commands
    initialize (init, i)
                        create formated workbook template.
    generate (gen, g)   generate analyzed files as TEXT from META descritor
                        file. (e.g., Excel)

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -e {python built-in codec}, --encoding {python built-in codec}
                        Set default charactor encode. When not set this, it is
                        treated as "utf-8". see also. https://docs.python.org/3.6/library/codecs.html#standard-encodings

# initialize subcommand help
$ ./table_re_constructor/table_reconstructor.py init -h
usage: table_reconstructor.py initialize [-h] [-tx [path/to/outputfile.xlsx]]

optional arguments:
  -h, --help            show this help message and exit
  -tx [path/to/outputfile(.xlsx)], --template_xlsx [path/to/outputfile(.xlsx)]
                        This is an initialize helper option. Generate template
                        xlsx file based on same filename.yaml. **And if you
                        set this, other options are ignored.** will be
                        subcommand.

# generate subcommand help
$ table_reconstructor.py gen -h
usage: table_reconstructor.py generate [-h] [-v] [-i [path/to/inputfile]]
                                       [-hr tabsize] [-r [sheetname]]
                                       [-o [path/to/outputfile.json]]
                                       [-of [(csv | tsv):path/to/outputdir]]

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -i [path/to/inputfile], --input [path/to/inputfile]
                        Set path/to/input xlsx filename.
  -hr tabsize, --human_readable tabsize
                        set indent size by numeric value, Output humanreadable
                        json files.
  -r [sheetname], --root_sheet [sheetname]
                        set a sheetname in xlsx book have. construct json tree
                        from the sheet as root item. "root" is Default root
                        sheet name.
  -o [path/to/outputfile(.json)], --output [path/to/outputfile(.json)]
                        Output interpreted json. If this set which endswith
                        ".json" as set full filename, output jsonfile treated
                        as the name. But when not set ".json", adopt original
                        xlsx filename, like
                        path/to/outputfile/[source_METAFile_name].json (-o has
                        special filename "-" as STDOUT, and when set like "-o
                        -", all other stdout messages were masked.)
  -of [(csv | tsv):path/to/outputdir], --output_format [(csv | tsv):path/to/outputdir]
                        Output with the format, If you set this, output
                        formfiles to
                        path/to/[source_METAFile_name].xlsx/[sheetname.?sv]s
                        It'll be recommended, if you want to have
                        communication with non Tech team without any
                        gitconfiging.
```

## Appendix 3. MindMap
[mindnode](https://my.mindnode.com/vWDYEyp9p7s2kFgCr4yzuVrokfimz3Cx2nvGR1Xg/em#97,31,-2)
