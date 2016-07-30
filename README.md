# sharelatex-platex-patch
ShareLatex のコンパイラに platex を設定するなど，日本語論文に対応するためのパッチ．

解説記事はこちら --> http://ken1row.net/archives/47

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

# Sharelatex のプロセスを止める
Sharelatex が動いたままだと，コンパイル時にエラーが発生します．
そのため，sharelatex のプロセスを止める必要があります．

### `grunt run` でプロセスを開始したとき
各プロセスの ID をしらべて，`kill` コマンドで停止します．
```
ps -ax | grep sharelatex
kill [PID]
```

### Upstart でプロセスを開始しているとき
Upstart で起動しているときは，`kill` でプロセスを停止させても自動的に新しいプロセスが開始されます．

次のコマンドで，upstart で管理しているプロセスを列挙できます．
```
 initctl list | grep sharelatex
```

プロセスを停止するには，以下のコマンドを実行します．
```
 sudo initctl stop sharelatex-web
```
sharelatex-web が停止します．他のプロセスについても同様に停止させます．

プロセスを開始するには，以下のコマンドを実行します． 
```
 sudo initctl start sharelatex-web
```
