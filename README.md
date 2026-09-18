# Blender Hair Workflow

VRChat向け髪調整を、軽い数値ループと必要時だけの目視確認に分けて回すためのローカルリポジトリです。

このリポジトリでは、商用髪の元データを再生成し直しません。確定した `.blend` をローカルの版スナップショットとして保存し、`canonical/hair_vNNN.py` がその髪データを現在の作業シーンへ冪等に適用します。品質と再現性を優先した、実用寄りの構成です。

## 最短の使い方

Blender MCP Serverを起動してから、PowerShellで実行します。

```powershell
cd E:\BlenderHairWorkflow
python tools\hairflow.py status
python tools\hairflow.py apply
python tools\hairflow.py validate
python tools\hairflow.py view front-right
```

視覚確認が必要か判断します。

```powershell
python tools\hairflow.py gate --silhouette-changed --unresolved-visual
```

`VISUAL_REVIEW_REQUIRED` のときだけComputer Useで確認します。明らかな跳ね、折れ、隙間は拡大して前後両側から見ます。

Blenderで手動修正した方が速い場合は、修正後の `.blend` を保存して次版へ昇格できます。

```powershell
python tools\promote.py --source "D:\path\fixed.blend" --version v002
```

## 現在の正本

- バージョン: `v001`
- 適用スクリプト: `canonical/hair_v001.py`
- ローカル版スナップショット: `artifacts/Lasyusha-v001.blend`
- 元の比較用スナップショット: `artifacts/Lasyusha-baseline.blend`
- 元作業ファイル: `Lasyusha-ShoulderFlow-Fixed.blend`

`.blend` は商品データを含むためGit管理対象外です。リポジトリの外へ公開・配布しないでください。

詳しい運用は [docs/WORKFLOW.md](docs/WORKFLOW.md)、現在の判断基準は [docs/KNOWLEDGE.md](docs/KNOWLEDGE.md) を参照してください。

