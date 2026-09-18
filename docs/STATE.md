# Current state

## Accepted version

- Version: `v001`
- Artifact: `artifacts/Lasyusha-v001.blend`
- Source work file: `Lasyusha-ShoulderFlow-Fixed.blend`
- Date: 2026-09-18

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

次に形状を触る前に `v001` を再適用して差分を小さくする。肩や襟の修正は全景と拡大の両方で確認する。

2026-09-18のリポジトリ作成時、開いていたBlender GUIは古い `Lasyusha-SurfaceLocal-Stage12.blend` だった。未保存状態を壊さないため自動適用はしていない。作業再開時は対象シーンを確認してから `python tools/hairflow.py apply` を実行する。
