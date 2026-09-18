# 運用フロー

## 1. 安い編集ループ

日常の変更はスクリプトとMCPだけで回します。

```powershell
python tools\hairflow.py apply
python tools\hairflow.py validate
```

エラー、頂点数、オブジェクト数、寸法はこの段階で解決します。スクリーンショットは取りません。

## 2. 視覚確認ゲート

次の条件をすべて満たす場合だけComputer Useを使います。

1. `apply` が成功した。
2. `validate` が成功した。
3. 前回確認以降に外形や毛流れへ影響する変更が入った。
4. 跳ね、折れ、量感、隙間など数値で決められない問題が残る。

```powershell
python tools\hairflow.py gate --silhouette-changed --unresolved-visual
```

## 3. 視点固定と目視

```powershell
python tools\hairflow.py view front
python tools\hairflow.py view front-right
python tools\hairflow.py view right
python tools\hairflow.py view back
python tools\hairflow.py view left
```

局所修正では `--closeup` を使い、Computer Useで対象へ寄せます。全景だけで合格にしません。肩の毛先は前寄りと後ろ寄りの両側から確認します。

## 4. 手動修正

形状が明らかにおかしく、頂点を直接動かす方が早い場合はBlenderで手動修正して構いません。

1. 作業前に別名保存する。
2. Blenderで少数の頂点・束に限定して直す。
3. 同じ問題箇所を拡大し、反対側の角度でも確認する。
4. 修正版を新しい `.blend` として保存する。
5. `tools/promote.py` で次版へ昇格する。
6. `config/project.json` の期待値と `CHANGELOG.md` を更新する。

## 5. 修正指示

指摘は [templates/review.md](../templates/review.md) の形式にします。定数名まで分からなくても、対象オブジェクト、位置、症状、望む流れを分けて書けば十分です。

## 正本の考え方

このリポジトリは厳密なプロシージャル生成ではありません。

- Git管理: 適用スクリプト、検証スクリプト、判断理由、ノウハウ。
- ローカル管理: 商品データを含む版スナップショット `.blend`。
- 再現: `hair_vNNN.py` が版スナップショットの6メッシュを現在の作業シーンへ置き換える。

これにより、手動作業の速さと、結果を何度でも戻せる再現性を両立します。

