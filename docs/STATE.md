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
- Unity表示、アニメーション、PhysBoneは未検証。
- 商品は片面メッシュで、ソリッド表示では透過テクスチャ適用時より板状に見える。

## Next practical step

次に形状を触る前に開いているシーンと未保存編集を確認する。保存版に戻す必要がある場合だけ `v002` を再適用する。肩や襟の修正は全景と拡大の両方で確認する。

2026-09-19: Computer Useで現在の `Lasyusha-ShoulderFlow-Fixed.blend` を確認。形状変更は行わず、補完毛束を含めた7メッシュの復元を修正した。優先順位は大きな毛束の折れ、目立つ浮き・大きな貫通、毛先の順。微小な貫通は許容する。

古い下書き・バックアップ45個と旧v001スナップショットを削除。現在の作業ファイル、v002、比較用baselineを残した。Unity側が本体であり、Blenderは下書きとして扱う。
