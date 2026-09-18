# Blender Hair Workflow

VRChat向け髪調整を、軽い数値ループと必要時だけの目視確認に分けて回すためのローカルリポジトリです。

このリポジトリでは、商用髪の元データを再生成し直しません。確定した `.blend` をローカルの版スナップショットとして保存し、`canonical/hair_vNNN.py` がその髪データを現在の作業シーンへ冪等に適用します。品質と再現性を優先した、実用寄りの構成です。

## 最短の使い方

Codex Desktopでは、リポジトリを開いて次の一言で始められます。

```text
$hairflow 肩の跳ね上がった毛先を自然な流れに直して
```

Astraが修正・目視・保存まで続けて担当する運用です。Computer Useを基本に、MCPや下記CLIも選べます。Terraとの工程ごとの往復は不要です。画面やMCPで直した結果は既存Pythonに自動反映されないため、修正版 `.blend` を保存して次版に取り込みます。

CLIでBlenderに接続する場合はBlender MCP Serverを起動し、必要なコマンドを選んで実行します。

```powershell
cd E:\BlenderHairWorkflow
python tools\hairflow.py status
python tools\hairflow.py validate
python tools\hairflow.py view front-right
```

`apply` は保存版への置換です。現在の編集を保全し、復元・適用が必要な場合だけ実行します。

以下のゲートは任意です。数値検証を内部で再実行するので、検証済みなら省略できます。

```powershell
python tools\hairflow.py gate --silhouette-changed --unresolved-visual
```

形状変更の仕上がりはComputer Useで確認します。初期状態の確認や手動修正にも使えます。明らかな跳ね、折れ、隙間は拡大して前後両側から見ます。

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
