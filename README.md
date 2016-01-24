# sharelatex-platex-patch
ShareLatex のコンパイラに platex を設定するなど，日本語論文に対応するためのパッチ．

# クイックスタート
すべてのファイルを，ShareLatex ディレクトリにコピーする
```
 cd sharelatex-platex-patch
 sudo cp -r * /var/www/sharelatex
```
パッチを適用する
```
 cd /var/www/sharelatex
 sudo python patch.py --compile
```
 
## パッチを取り消す
```
 sudo python patch.py --unpatch
```
