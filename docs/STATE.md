# Current state

## Accepted version

- Version: `v002`
- Artifact: `artifacts/Lasyusha-v002.blend`
- Source work file: `Lasyusha-ShoulderFlow-Fixed.blend`
- Date: 2026-09-18

`v002` is a reproducibility-only update. It preserves the accepted `v001`
geometry and adds `ShoulderWisps_Subtle` as the seventh managed hair mesh, so a
restore can recreate that object and its armature setup if it is missing.

## What is good

- これまでの中でユーザー評価が最もよい流れを基準にしている。
- 頭サイズと前髪の生え際は概ねよい。
- 元商品の横へ流す前髪、顔まわりから胸元へ続くカーブ、長い後ろ髪を維持。
- 切断跡を補い、肩付近の大きな跳ね上がりを修正済み。

## Remaining limits

- 静止したBlender上の確認まで。
- すべての細かな服との交差をゼロと保証していない。
- 2026-09-19: Unityで前後左右の表示とPlay Modeへの読み込みを確認。多様な動作・PhysBoneの全姿勢での接触は未検証。
- 商品は片面メッシュで、ソリッド表示では透過テクスチャ適用時より板状に見える。

## Next practical step

次に形状を触る前に開いているシーンと未保存編集を確認する。保存版に戻す必要がある場合だけ `v002` を再適用する。肩や襟の修正は全景と拡大の両方で確認する。

2026-09-19: Computer Useで現在の `Lasyusha-ShoulderFlow-Fixed.blend` を確認。形状変更は行わず、補完毛束を含めた7メッシュの復元を修正した。優先順位は大きな毛束の折れ、目立つ浮き・大きな貫通、毛先の順。微小な貫通は許容する。

古い下書き・バックアップ45個と旧v001スナップショットを削除。現在の作業ファイル、v002、比較用baselineを残した。Unity側が本体であり、Blenderは下書きとして扱う。

## Unity反映済み — 2026-09-19

- Scene: `Assets/sepha-outfits.unity` を保存。
- 配置先: `Sepha (SPS) (ChichiwoMore)/lasyusha_Blender_v002`。
- Prefab: `Assets/HairFit_Lasyusha/v002/lasyusha_Blender_v002.prefab`。
- 採用版の評価済み完成形を転送し、既存骨・マテリアル・PhysBone・MA Merge Armatureを引き継いだ。商品用の頭サイズShape Changerは新Prefabから除外。
- 元の7メッシュを有効化。ShoulderWisps_Subtleは復元したbackと重複するため、採用版どおり非表示で同梱。
- 旧シーン髪 `lasyusha` は非表示で保持。戻す際は新Prefabを無効化して旧髪を有効化する。
- BakeMeshの完成形比較: 最大位置差約6.04e-7m。Computer Useで正面・両側面・後面を確認。Play Modeで髪の表示と読み込みを確認し、編集モードへ戻した。
- 新メッシュはシェイプキー評価結果を焼き込んだ専用品。元の髪シェイプキーは残らない。
- 再利用手順: `docs/UNITY_TRANSFER.md`。データを含む中間JSON・FBXはGit対象外。
