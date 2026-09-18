---
name: hairflow
description: Adjust Blender hair shape, fit, penetration, and silhouette using the saved versions and visual criteria in BlenderHairWorkflow.
---

# Hairflow

このSkillを含むリポジトリを作業場所とし、ルートの `AGENTS.md` に従って依頼された髪の修正を進める。

通常はAstraが一貫して進め、Computer Use・MCP・既存CLIを必要に応じて選ぶ。画面やMCPで直した結果はPythonに自動反映されないため、保存した修正版 `.blend` を次版の基準にする。

`python tools/hairflow.py` の `status` は保存版の確認、`apply` は保存版の適用、`validate` はメッシュ数値の照合、`view <angle>` は視点設定に使う。すべてを毎回実行する手順ではない。

完了条件は、指摘された不自然さが改善し、周囲に新しい跳ね・折れ・浮きがなく、確認した結果を次版として保存できていること。結果と未確認事項を短く伝える。
