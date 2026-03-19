# Claude Handoff: `gh auth login` を恒久化するための実行手順

## 目的

このリポジトリを GitHub に push し，GitHub Pages で公開する前提として，`gh auth login` の認証状態を恒久化する．

現状は `GH_TOKEN` 環境変数が優先されており，`gh` の保存型認証が使えていない可能性がある．
そのため，`GH_TOKEN` 依存を解除したうえで，GitHub CLI の資格情報ストアに認証情報を保存する．

## 現状整理

- 作業ディレクトリ: `C:\Users\takum\Downloads\products\スライド生成デモ`
- ローカルgitリポジトリ: 初期化済み
- ブランチ: `main`
- スライド成果物: `outputs/ポケモン現環境最強構築_スライド.html`
- `gh auth status` 実行結果:
  - `You are not logged into any GitHub hosts.`
- ユーザーが `gh auth login` を実行した際の表示:
  - `The value of the GH_TOKEN environment variable is being used for authentication.`

つまり，このシェルまたはOS環境に `GH_TOKEN` が存在し，`gh` の通常ログインを妨げている．

## ゴール

以下の状態にする．

- `GH_TOKEN` に依存せず，`gh auth status` が成功する
- GitHub.com に対して `gh` が恒久的に使える
- 以後，このリポジトリで `gh repo create`，`git push`，`gh api` などが実行できる

## Claude に実行してほしい内容

### 1. `GH_TOKEN` の存在場所を確認する

PowerShell で以下を確認する．

```powershell
Get-ChildItem Env:GH_TOKEN
[Environment]::GetEnvironmentVariable("GH_TOKEN","User")
[Environment]::GetEnvironmentVariable("GH_TOKEN","Machine")
```

確認ポイント:

- 現在のシェルにだけ設定されているのか
- ユーザー環境変数に設定されているのか
- システム環境変数に設定されているのか

### 2. `GH_TOKEN` を無効化する

まずは現在のシェルから消す．

```powershell
Remove-Item Env:GH_TOKEN -ErrorAction SilentlyContinue
```

ユーザー環境変数に入っている場合は削除する．

```powershell
[Environment]::SetEnvironmentVariable("GH_TOKEN",$null,"User")
```

システム環境変数に入っている場合は，必要に応じて削除する．

```powershell
[Environment]::SetEnvironmentVariable("GH_TOKEN",$null,"Machine")
```

注意:

- `Machine` の変更は管理者権限が必要な場合がある
- 既存の運用上，`GH_TOKEN` が他用途で必要なら，削除ではなくこの作業用シェルでのみ無効化してもよい

### 3. 新しい PowerShell を開き直す

環境変数の影響を避けるため，新しい PowerShell セッションで作業する．

再確認:

```powershell
Get-ChildItem Env:GH_TOKEN
[Environment]::GetEnvironmentVariable("GH_TOKEN","User")
[Environment]::GetEnvironmentVariable("GH_TOKEN","Machine")
```

理想状態:

- すべて空

### 4. `gh auth login` を保存型で実行する

以下を実行する．

```powershell
gh auth login
```

推奨選択:

- Host: `GitHub.com`
- Protocol: `HTTPS`
- Authenticate Git with your GitHub credentials: `Yes`
- Login method: ブラウザ認証またはデバイスコード認証

期待する結果:

- ログイン成功
- 認証情報が GitHub CLI 側の資格情報ストアに保存される

### 5. ログイン状態を確認する

```powershell
gh auth status
```

成功条件:

- `github.com` に対してログイン済みと表示される
- 認証ユーザー名が表示される

### 6. Git操作に使えるか確認する

このリポジトリで以下を確認する．

```powershell
cd "C:\Users\takum\Downloads\products\スライド生成デモ"
git status
gh repo view
```

まだリモート未作成なら `gh repo view` は失敗してよい．
ただし `gh` 自体が認証エラーなく動くことを確認する．

## ここまで完了したら次にやる作業

認証が恒久化できたら，次の順で進める．

1. GitHub リポジトリを新規作成する
2. `origin` を設定する
3. `main` を push する
4. GitHub Pages 公開用の導線を追加する
5. Pages URL を確認する

## 次の担当者向けメモ

- この環境からは Claude 自体を直接呼び出す機能はない
- したがって，本ファイルは「Claude に貼って実行させるための handoff 文書」として使う
- Claude 側でMCPや端末操作が可能なら，上記手順をそのまま実行すればよい

## 完了条件

以下を満たしたらこの handoff は完了．

- `GH_TOKEN` に依存しない
- `gh auth status` が成功する
- 次のセッションでも `gh` が認証済みのまま使える
