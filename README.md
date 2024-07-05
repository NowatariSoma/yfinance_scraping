# 仕様書

## 概要
このプログラムは、Yahoo!ファイナンスのコメントセクションからコメントをスクレイピングし、CSVファイルに出力するものです。ChromeのWebDriverを用いてページを読み込み、BeautifulSoupを使ってコメントを抽出します。また、Shift-JISエンコードに対応できない文字を削除してからCSVファイルに保存します。

## 使用技術
- Python
- Selenium
- BeautifulSoup
- pandas

## 必要なライブラリ
- selenium
- webdriver_manager
- beautifulsoup4
- pandas

## 機能詳細

### `setup_driver()`
Chromeドライバをセットアップし、webdriverプロパティを削除して自動操作を隠蔽します。

#### 引数
なし

#### 戻り値
`webdriver.Chrome`オブジェクト

### `load_page(driver, url)`
指定したURLのページを読み込み、ページの最下部までスクロールします。

#### 引数
- `driver`: WebDriverオブジェクト
- `url`: 読み込むページのURL

#### 戻り値
ページのHTMLソース

### `extract_comments(page_source)`
ページソースからコメントを抽出します。

#### 引数
- `page_source`: ページのHTMLソース

#### 戻り値
コメントのリスト（各コメントは辞書形式）

### `generate_url(base_url)`
ベースURLからコメントページのURLリストを生成します。

#### 引数
- `base_url`: ベースとなるURL

#### 戻り値
URLのリスト

### `remove_non_shift_jis(text)`
Shift-JISにエンコードできない文字を削除します。

#### 引数
- `text`: 対象のテキスト

#### 戻り値
Shift-JISにエンコードできる文字のみを含むテキスト

### `main()`
全体の処理を行います。具体的には以下のステップを実行します。
1. WebDriverのセットアップ
2. URLリストの生成
3. 各URLのページを読み込み、コメントを抽出
4. 抽出したコメントをデータフレームに変換
5. データをShift-JISにエンコードできる文字のみを含む形式にクリーニング
6. CSVファイルに出力

## 使い方
1. 必要なライブラリをインストールします。
   ```bash
   pip install selenium webdriver_manager beautifulsoup4 pandas
   ```
2. プログラムを実行します。
   ```bash
   python script.py
   ```
3. `output.csv`というファイルにスクレイピングしたコメントが保存されます。

## 注意点
- Yahoo!ファイナンスのページ構造が変更された場合、プログラムが動作しない可能性があります。
- Shift-JISにエンコードできない文字は削除されるため、元のコメントの情報が一部失われる可能性があります。