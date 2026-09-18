# 運用フロー

## 状況に応じて使うコマンド

リポジトリのルートで実行する。Blenderへ通信するコマンドにはBlender側のサーバーが必要。

| コマンド | 用途 |
| --- | --- |
| `python tools/hairflow.py status` | ローカル保存版とハッシュの確認。開いているBlenderシーンは確認しない |
| `python tools/hairflow.py apply` | 保存版で対象6メッシュを置換。作業中の編集を保全し、復元・版適用が必要なときだけ実行 |
| `python tools/hairflow.py validate` | 頂点数などを期待値と照合。貫通・見た目の検査ではない |
| `python tools/hairflow.py view front-right --closeup` | 確認用の視点設定 |
| `python tools/promote.py --source "D:/path/fixed.blend" --version v002` | 保存した修正版を新しいローカル版と適用スクリプトに登録 |

## 修正と確認

スクリプトとComputer Useのうち、対象を自然に直しやすい方法を選ぶ。手動編集のためにもComputer Useを使える。変更箇所を前後両側から拡大し、仕上げに周囲一周の外形を確認する。各微調整のたびに全方向を撮り直す必要はない。

`gate --silhouette-changed --unresolved-visual` は任意の補助コマンドで、内部で `validate` を再実行する。直前に検証済みなら重ねて呼ぶ必要はない。数値不一致の原因調査や初期状態の確認にもComputer Useを使える。

毛先の削除などで頂点数が変わることはある。差分が意図どおりかを確認して期待値を更新し、再検証する。エラーを消すためだけに期待値を合わせない。

手動修正は作業前後に別名保存し、修正版を `promote.py` で昇格する。期待値と `docs/STATE.md`、`CHANGELOG.md` に必要な変更だけ記録する。`templates/review.md` は複数人への引き継ぎに必要なときだけ使う。

## 保存と通信

Gitにはスクリプトと判断理由を保存し、商品データを含む `.blend` はローカルに保持する。`canonical/hair_vNNN.py` は保存版を適用するもので、毎回髪を生成するスクリプトではない。

通常はAstraがComputer Useを中心に修正・確認・保存まで続けて担当する。既存CLIや直接のMCP呼び出しも使える。以前の直MCP禁止hookとTerraへの既定モデル指定は撤去した。

Computer Use・直MCPで変えたシーンは、既存のPythonや保存版と異なる状態になる。別名保存するまで `apply` しない。修正版 `.blend` を昇格して新しい適用スクリプトの参照先にすることで、手操作の結果も再現可能になる。

Terraへ引き継ぐ場合は、修正版 `.blend` の絶対パス、変更箇所、確認結果・未確認事項を渡す。必要なら画像も添える。Terraは修正版を読み込んで次版と期待値に反映し、古いスクリプトで上書きしない。Pythonだけを読んで画面上の変更を把握したことにしない。
