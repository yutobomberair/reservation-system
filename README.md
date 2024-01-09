# reservation-system

## 環境構築
* venvで仮想環境を作成する 
    - python3 -m venv venv

* venv環境の立ち上げ
    - (mac)source venv/bin/activate
    - (windows)./venv/Scripts/activate

* 必要なライブラリのインストール
    - pip3 install -r repuirements.txt

＊ エイリアス登録
    - 煩わしいのでpython、pipでコマンドが通るようにエイリアスを設定しておいた方が楽です。

## 実行
下記コマンドを実行してください
* python3 main_process.py

## 内部処理
main_window.pyが画面上のレイアウトを決定しています。
ここにあるmain_windowクラスを継承して、main_processクラスが定義されています。
main_processには各ボタンをクリックした時に実行される処理が定義されています。
予約データやシフトデータはreserve_dataディレクトリ内にあるcsvで管理しています。