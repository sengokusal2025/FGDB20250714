# Functional Graph Database (FGDB) システム

## 概要
Functional Graph Database (FGDB) は、数学的関数の実行履歴を管理するデータベースシステムです。関数の依存関係と実行順序を2つのグラフ構造で管理し、タイムスタンプ付きの実行履歴を記録します。

## 設計思想
1. **関数実行の解釈**: `y=f(x)`なる関数が与えられた場合、xを引数にとるfの実行(operation)によりyが生じると解釈
2. **実行履歴の管理**: operation毎に新しいy（y+timestamp）が生成され、実行履歴として記録
3. **グラフベースの管理**: 関数の構成要素と実行履歴を2つの有向グラフで管理

## 設計上の重要な変更点

### グラフ形状の改良
1. **ルートノード**: ひし形で表示し、グラフの起点を明確化
2. **Function Block**: 矩形で表示し、データノードとの視覚的区別を強化
3. **独立変数の接続**: Operation Graphでは独立変数を必ずルートノードから接続

### バッチファイル生成の統一と自動化
- すべての関数実行は `python ./f/func.py` 形式で統一
- ファイル名は `{operation_name}.bat` 形式で生成
- タイムスタンプ付き出力変数名の自動生成
- **operation.py実行時に自動的にバッチファイルを生成**

## プロジェクト構成
```
fgdb/
├── lib.py                 # FGDBメインライブラリ（FunctionalGraphクラス）
├── init.py               # 初期化スクリプト
├── configure.py          # 関数・変数登録スクリプト
├── operation.py          # 関数実行履歴記録スクリプト
├── show_fgdb.py          # グラフ可視化スクリプト
├── operation.txt         # 関数記述ファイル（サンプル）
├── function_analysis.py  # 従来の関数解析プログラム
├── fgdb.pickle          # FGDBデータファイル（実行時生成）
├── README.md            # このファイル
└── requirements.txt     # 必要なライブラリ
```

## FGDB の構成要素

### Functional Graph (FG)
FGは複数のgraphからなるgraph groupで、以下の2つのグラフで構成されます：

#### 1. Management Graph (MG) - 構成要素の管理
- **目的**: 関数と変数の登録順序を管理
- **構造**: ノードは登録順に接続（新規登録ノードの親は直前に登録したノード）
- **ノード**: Function Block (FB) と Data Block (DB)
- **エッジ**: 登録順序を表す

#### 2. Operation Graph (OG) - 実行履歴の管理
- **目的**: 関数実行による変数間の依存関係を記録
- **構造**: 実行する関数の独立変数を親、従属変数を子とする
- **ノード**: Data Block (DB) のみ
- **エッジ**: 関数名が付与され、実行関係を表す

### グラフの要素

#### Function Block (FB)
- **定義**: 関数の呼称
- **MG**: ノードとして存在
- **OG**: エッジとして存在（関数名がエッジに付与）

#### Data Block (DB)
- **定義**: （独立・従属）変数の呼称
- **MG・OG**: 両方でノードとして存在
- **タイムスタンプ**: 従属変数には実行時にタイムスタンプが付与

## 使用方法

### 1. セットアップ
```bash
# 必要なライブラリのインストール
pip install -r requirements.txt
```

### 2. 基本的な実行手順
```bash
# 1. FGDB初期化（ルートノード作成）
python init.py

# 2. 関数・変数の登録
python configure.py -i operation.txt

# 3. 関数実行履歴の記録（バッチファイル自動生成）
python operation.py -i operation.txt

# 4. グラフの可視化
python show_fgdb.py
```

### 3. 関数記述ファイルの形式
`operation.txt`の例：
```
y1=f1(x1)
y2=f2(y1)
y3=f3(y1,y2)
y4=f4(x2,x3,x4)
```

## コマンドライン詳細

### init.py - 初期化
```bash
python init.py [output_path]
```
- `output_path`: FGDBファイルの保存先（デフォルト: fgdb.pickle）

### configure.py - 構成
```bash
python configure.py -i operation.txt [-f fgdb_file]
```
- `-i, --input`: 関数記述ファイル（必須）
- `-f, --fgdb`: FGDBファイルのパス（デフォルト: fgdb.pickle）

### operation.py - 実行
```bash
python operation.py -i operation.txt [-f fgdb_file]
```
- `-i, --input`: 関数記述ファイル（必須）
- `-f, --fgdb`: FGDBファイルのパス（デフォルト: fgdb.pickle）

### show_fgdb.py - 可視化
```bash
python show_fgdb.py [-f fgdb_file] [--mg-only] [--og-only] [--save-mg file] [--save-og file] [--no-summary]
```
- `-f, --fgdb`: FGDBファイルのパス（デフォルト: fgdb.pickle）
- `--mg-only`: Management Graphのみ表示
- `--og-only`: Operation Graphのみ表示
- `--save-mg`: Management Graphを画像ファイルに保存
- `--save-og`: Operation Graphを画像ファイルに保存
- `--no-summary`: サマリー情報を非表示

## バッチファイル自動生成機能

`operation.py`を実行すると、自動的に対応するバッチファイルが生成されます。

**生成例:**
- 入力: `operation.txt` → 出力: `operation.bat`
- 入力: `my_task.txt` → 出力: `my_task.bat`

### 生成されるバッチファイル例（operation.bat）
```batch
@echo off
REM Auto-generated batch file from operation.txt
REM Generated at: 2025-07-10 14:30:25.123456

REM Operation 1: y = f(x)
python ./f/func.py -i x -o y_20250710_143025_001
if errorlevel 1 goto error

echo All operations completed successfully.
goto end

:error
echo Error occurred during operation execution.
exit /b 1

:end
```

## 実行例

### コマンド実行例
```bash
# 基本的な実行フロー
python init.py
python configure.py -i operation.txt
python operation.py -i operation.txt  # operation.batが自動生成される
python show_fgdb.py

# カスタムファイル名での実行
python operation.py -i my_functions.txt  # my_functions.batが生成される
```

## 技術仕様

### 使用ライブラリ
- **NetworkX**: グラフ構造の管理と操作
- **Matplotlib**: グラフの可視化
- **Pickle**: データの永続化
- **Datetime**: タイムスタンプ生成

### データ形式
- **ファイル形式**: pickle形式でシリアライズ
- **グラフ構造**: NetworkX DirectedGraph
- **タイムスタンプ**: YYYYMMDD_HHMMSS_mmm形式

## 可視化機能

### Management Graph (MG)
- **赤色・ひし形**: ルートノード
- **水色・矩形**: Function Block（関数）
- **緑色・円形**: 独立変数
- **オレンジ色・円形**: 従属変数
- **灰色**: その他

### Operation Graph (OG)
- **赤色・ひし形**: ルートノード
- **緑色・円形**: 独立変数（ルートノードから接続）
- **オレンジ色・円形**: 従属変数
- **青色**: エッジ（関数実行を表す）
- **エッジラベル**: 関数名

## エラーハンドリング
- ファイルの存在チェック
- 不正な関数記述の警告
- 欠損変数の自動補完
- グラフ描画エラーの処理

## 拡張可能性
- 新しい関数形式への対応
- 実際の数値計算との連携
- Web UIでの可視化
- より高度なグラフレイアウト
- データ分析機能の追加

## 従来システムとの関係
このFGDBシステムは、既存の`function_analysis.py`をベースとして拡張されており、関数解析機能も引き続き利用可能です。

## ライセンス
このプロジェクトは仕様書に基づいて開発されており、教育・研究目的での使用を想定しています。
