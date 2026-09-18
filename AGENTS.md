# Hair workflow instructions

このリポジトリで髪を調整するエージェントは、最初に `config/project.json`、`docs/STATE.md`、`docs/KNOWLEDGE.md` を読む。

## MCPの入口

- Blender MCPツールを会話から直接呼ばない。`python tools/hairflow.py ...` だけをBlenderへの入口にする。
- MCPで実行する新しい処理が必要なら、先に `blender/` または `canonical/` に版管理するスクリプトとして追加し、`hairflow.py` 経由で実行・検証できる形にする。
- 直書きしたBlender Python、使い捨てのソケット接続、MCPの実行コードを会話から送らない。
- 手動編集はComputer Useで行ってよい。ただし保存後は `tools/promote.py` で次版の正本に昇格する。

最短の依頼は `$hairflow <修正内容>`。Skillがこのルールと通常ループを読み込む。

## 通常ループ

1. `canonical/hair_vNNN.py` または次版候補を編集する。
2. `python tools/hairflow.py apply` でBlenderへ適用する。
3. `python tools/hairflow.py validate` でオブジェクト数、頂点数、寸法を確認する。
4. 数値で直せる問題はComputer Useを起動せず修正する。
5. シルエットへ影響する変更があり、数値では判断できない項目が残る場合のみComputer Useで確認する。

## Computer Useの確認

- `python tools/hairflow.py view <angle>` で視点を固定する。
- 通常は `front`, `front-right`, `right`, `back`, `left` を見る。
- 肩や襟の修正では、問題箇所を拡大し、前寄り・後ろ寄りの両方から見る。
- 明らかな跳ね上がり、輪、鋭い折れ、空中の隙間は不合格にする。
- 全景だけの確認で合格扱いにしない。

## Blenderで直接編集した場合

手動編集は許可する。作業後に別名保存し、`tools/promote.py` で次版スナップショットと正本適用スクリプトを作る。手動編集だけを残して正本との差を放置しない。

## 範囲

髪のモデリング、形状調整、髪マテリアルまで。Unityへの反映、衣装自体の編集、リギングとアニメーションは別タスク。
