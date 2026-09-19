# LasyushaのUnity転送

## 最初に確認すること

- 開いているシーンの髪オブジェクトと実際のPrefab参照、未保存編集を読む。2026-09-19はシーンの `lasyusha` が商品Prefabを参照し、`lasyusha_SephaFit.prefab` は使っていなかった。
- Blenderの採用版は `artifacts/Lasyusha-v002.blend`。完成形は複数のシェイプキーとアーマチュアを評価した結果。基底メッシュだけを移さない。
- 対象は back / bangs side / base / pin / side1 / side2 / side3。ShoulderWisps_Subtleも保存されているが、backの17枝の復元後は重複回避のため意図的に非表示。追加オブジェクトを同梱しても、この無効状態を維持する。

## この案件で使う方式

`tools/export_unity_evaluated.py` は完成形の頂点・法線・UV・面・ボーン名とウェイト・表示状態をJSONへ取り出す。Unity Editorの転送コードと組み合わせ、現在の髪を複製して専用メッシュを割り当て、別Prefabとして保存する。旧髪は非表示で保持する。

Unity用座標はこのBlenderシーンの衣服参照作成コード `native-local.py` の逆変換に基づく `(-x, z+0.016, -y-0.0034)`。この補正値を別アバターへ流用しない。座標・単位・見た目を確認する。

ウェイトのボーン名を現在のUnityリグへ対応付け、現在姿勢からbindposeを作る。Lasyushaには `Head` という髪内部ボーンがなく、根元は `アーマチュア`。無ウェイト頂点は根元に固定する。SkinnedMeshRenderer.BakeMeshで転送元との位置差を確認し、Computer Useで前・後・両側を見る。

新メッシュのTransformは単位スケールにそろえてから頂点をローカル座標へ変換する。元のFBX由来の拡大率を二重に掛けない。Blender→Unityの上記変換は反射を含み、CCWからUnityの時計回りへ既に反転するので、三角形の頂点順をさらに逆転させない。表裏の誤りは正面だけで見逃しやすく、側面・後頭部も見る。

UnityのComponent取得はC#の `??` で補完せず、Unityのbool/null判定を使う。MeshRendererからSkinnedMeshRendererへ切り替えるpin等では、破棄したコンポーネントの擬似nullで失敗し得る。

完成形を焼き込む方式では、髪の元シェイプキーは新メッシュに残らない。既存の髪リグ・材質・PhysBoneを引き継ぐ。シーンへの配置、アバター配下への組み込み、Play Modeでの確認は区別して結果に記録する。

## 今回避けるべきだった回り道

- FBXは `AssetDatabase.LoadAssetAtPath<GameObject>` で読む。`LoadPrefabContents` は編集する .prefab 用。
- FBXのsharedMeshだけを既存rendererへ入れない。骨の順序・bindpose・座標・シェイプキー・Rendererの種類が一致するとは限らない。
- Blenderで非表示のリグやメッシュは選択書き出しから漏れ得る。必要物だけ出たことを名前・数・骨で確認する。非表示の理由を調べる前に全部を有効化しない。
- Unityのコンパイル完了後に適用コマンドを送る。再コンパイル前に送ると、旧コードのポーリング処理が先に消費することがある。
- 同じ不明点に対して小さな修正・再コンパイルを繰り返さず、対象の階層・実際のボーン名・renderer・参照をまとめて診断する。
- FBXバイナリを文字列検索して丸ごと出力しない。真偽・件数・必要な名前だけを出す。

商品メッシュを含む .blend / FBX / JSON / Unity mesh asset はローカル保持。Gitには転送コードと手順だけを入れる。

## 再利用するコードと確認結果

- `tools/export_unity_evaluated.py`: Blenderを採用版でバックグラウンド起動して実行。出力は `artifacts/unity-evaluated.json`。
- `tools/ApplyLasyushaV002.cs`: Unityプロジェクトの `Assets/HairFit_Lasyusha/Editor/` に配置して使用する、今回のリグ・シーン用Editorツール。Tools/HairFitから診断・転送できる。新しい版へ使う場合は版名とパスを更新し、既存のv002を重複配置しない。
- 自動実行時は `artifacts/unity-command.txt` に audit / apply / integrate / view 180 / save のいずれか一つを書き、`unity-result.txt` の更新を確認してから次へ進む。コンパイル中は書かない。integrateは名前が一致するSephaアバターへワールド座標を保って配置する。
- 2026-09-19の転送先は `Assets/HairFit_Lasyusha/v002/lasyusha_Blender_v002.prefab`。シーン保存済み、前後左右とPlay Modeの表示確認済み。頂点位置差は最大約6.04e-7m。全アニメーションの接触までは未確認。
- ウェイト・法線・UVを保持するため出力頂点は面コーナーごとに分かれる。ポリゴン数は増えないが、頂点数はBlenderの表示値より多くなる。
