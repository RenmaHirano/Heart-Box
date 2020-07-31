# Introduction to VIM

ラズパイに"vim"を導入して楽に開発しよう。
ここでは、"vim"のインストールから".vimrc"の設定まで行う。

# Features

・ターミナル上で開発、実行が完結。

・自分流にカスタマイズしやすい。

・強そうに見える。

# Requirement

簡単なターミナルコマンドとvimのコマンドを覚える必要あり。

* [Macのターミナルコマンド一覧（基本編）](https://qiita.com/ryouzi/items/f9dee1540a04a0bfb9a3).
* [vimの使い方。](https://kekaku.addisteria.com/wp/20190129143137).

# Installation

(1)元から入っているvim-tinyをアンインストール
```bash
sudo apt-get --purge remove vim-common vim-tiny
```

(2)通常のvimをインストール
```bash
sudo apt-get install vim
```

(3)ホームディレクトリに.vimrcファイルを作成
```bash
vim .vimrc
```

(4)ホームディレクトリに.vimディレクトリを作成
```bash
mkdir .vim
```

(5).vimに移動
```bash
cd .vim
```

(6).vimにcolorsディレクトリを作成
```bash
mkdir colors
```

(7)jellybeansをダウンロード
```bash
git clone https://github.com/nanotech/jellybeans.vim.git
```

(8)設定ファイルを.vim/colorsにコピー
```bash
cp jellybeans.vim/colors/jellybeans.vim colors/
```

(9)不要になったjellybeansフォルダを削除
```bash
sudo rm -r jellybeans.vim/
```

# .vimrcの例

ホームディレクトリの.vimrcにvi .vimrcで編集。

```bash
syntax on ”色変

set nocompatible “矢印キーを使えるようにする。
set clipboard+=unnamed “クリップボードにコピペ可
set number “行番号を表示 
set cursorline “現在の行をハイライト
set autoindent
set tabstop=4
set shiftwidth=4
set cursorline
set background=dark

colorscheme jellybeans
```
# Note

方向キーが標準でABCDになっているので、
まずset nocompatibleを書いて保存してからやると楽。
