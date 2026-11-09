# このリポジトリでの作業手順

## ツール

- KiCad 10（`kicad-cli`、Python の `pcbnew`）
- Ghostscript（`docs/` の PNG 生成）
- Docker がある場合は `kicad/kicad:10.0` イメージで全部そろう
- 配線をやり直す場合のみ Freerouting 2.x CLI と Java 21+

`scripts/kicad.sh` はリポジトリを `/work` にマウントして、コンテナ内で
コマンドを実行します。rootless Docker で `/work` がコンテナ内で root 所有に
なる場合は、自動で `--user 0:0` に切り替えます。

```sh
./scripts/kicad.sh python3 scripts/gen_sch.py
./scripts/kicad.sh python3 scripts/gen_pcb.py
./scripts/kicad.sh ./scripts/export_fab.sh
./scripts/kicad.sh kicad-cli pcb drc --severity-error pico2-compat.kicad_pcb
```

## 生成物

| 生成物 | コマンド |
| --- | --- |
| 回路図 | `./scripts/kicad.sh python3 scripts/gen_sch.py` |
| 配置・外形 | `./scripts/kicad.sh python3 scripts/gen_pcb.py` |
| 配線 | `./scripts/route.sh`（要 Freerouting） |
| GND ベタ | `./scripts/kicad.sh python3 scripts/finish_pcb.py` |
| ガーバー、BOM、CPL、PDF | `./scripts/kicad.sh ./scripts/export_fab.sh` |
| `docs/` の画像 | `./scripts/kicad.sh ./scripts/gen_docs_images.sh` |

`scripts/gen_pcb.py` は **配置と外形だけ** を作り、配線は入れません。
実行すると既存の配線が消えるので、配置を変えた場合は `scripts/route.sh` で
配線をやり直してください。`scripts/design.py` が部品・ネットの単一ソースです。

## 検証

```sh
./scripts/kicad.sh kicad-cli sch erc --severity-all --exit-code-violations \
  -o erc.rpt pico2-compat.kicad_sch
./scripts/kicad.sh kicad-cli pcb drc --severity-error --exit-code-violations \
  -o drc.rpt pico2-compat.kicad_pcb
```

ERC は 0 件、DRC はエラー 0 件を保ってください。シルクの文字高や
シルクとパッドのクリアランスは警告として残る場合があります。

## コミットと PR

1. `main` から作業ブランチを切る。
2. 生成物を再生成し、`git diff` で意図したファイルだけが変わっているか確認する。
3. ERC と DRC を実行する。
4. 署名付きでコミットする（`commit.gpgsign=true`）。
5. PR 本文は一時ファイルに書いてから作成する。

## 注意

- `pico2-compat.kicad_pcb` は配線済みの最終基板です。`gen_pcb.py` を実行すると
  配線が消えるので、配置変更時は必ず `route.sh` まで実行してください。
- Type-C の向き、QFN のピン 1、CPL の回転は JLCPCB の実装プレビューで確認してください。
- PIO USB はデバイス専用です。1.5 kΩ D+ プルアップ（R11）を外さない限り
  ホスト用途には使えません。
