[![Waffle.io - Columns and their card count](https://badge.waffle.io/setminami/TableReconstructor.png?columns=all)](https://waffle.io/setminami/TableReconstructor?utm_source=badge)
# JSON_XLSX_Manager
## What I wanna do and What is convenient
  - テストや設定データを興味を持つところのみにこだわり、平易に管理したい
    - 雑音を排除し、必要条件を満たすことに集中できる
  - Excelなど抽象表現からJSON, Yaml, md...etcの具象表現を振り分け自動生成したい
    - 抽象表現を建てることにより、∃具象表現のみを必要とするだけで他は必要になるまで出力の必要がなくなる
    - 抽象的に興味の対象を記述することで、未認知含め∀具象表現はそれぞれの下層レイヤでの限定都合で整形することに集中できる
  - 小粒度ファイルを多人数にmap, reduceして作業の集中と並列化を図る
    - 例えば、初期化したexcelからsheetをばらして配って各自入力、回収時finalizeすると巨大なJSONファイルが出力されるとか。

## excel構築と編集
  - git管理をする場合は必ずxlsx形式であること

  1. 1階層1sheetとして管理すること
  2. root itemを示すsheetは`root`をシート名とすること
  3. カラムはキーとして解釈されること
  4. 1階層下にitemを持たせる場合は別sheetとし、item名カラムにsheetへのハイパーリンクを張ること
    - 1階層下を配列にしたくない場合はカラム行とコンテンツ1行とする
    - 1階層下が配列の場合は、コンテンツ行が2行以上存在させることで対応する
    - よって、`{"parent1":[{"child1":"foo", "child2": "bar"}]}`のような1itemしかない配列は表現できないことを許容する
  5. cell内に文字列で`sheet://sheet名`とすることにより個別sheetを指すこと
    - Excelからいちいちメニューを選んで別シートへのハイパーリンクを張るのが思いのほかめんどくさい
    - 操作ライブラリでのhyperlink記述がExcel記入方法、OSにより揺れることがあるため、リンクする際は手動とする
    - `sheet://`以降をそのままsheet名とするため、encode上whitespaceを許す
    - typoが見つかった場合は、コマンドのエラーとして上げる see. エラー
  6. Excelの仕様に振られないため、余計なマクロは極力上書きしない

## エラー
  - root sheetがない
  - 指定されたシートが見つからない
