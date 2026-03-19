# Claude Handoff: GitHub リポジトリ作成と GitHub Pages 公開

## 目的

ローカルで作成済みのスライドリポジトリを GitHub に公開し，`outputs/ポケモン現環境最強構築_スライド.html` を GitHub Pages 経由で閲覧できるようにする．

## 前提

- 作業ディレクトリ:
  - `C:\Users\takum\Downloads\products\スライド生成デモ`
- ローカル git リポジトリ:
  - 初期化済み
  - ブランチ: `main`
- メイン成果物:
  - `outputs/ポケモン現環境最強構築_スライド.html`
- 追加済みドキュメント:
  - `README.md`
  - `AGENTS.md`p
  - `docs/claude_handoff_gh_auth_persistence.md`
- 現時点で `docs/` が未コミットの可能性あり
- Codex 側セッションでは `gh auth status` が未ログイン扱いになっていたが，ユーザーは別セッションでログインできていると言っている

## Claude にお願いしたいこと

### 1. 現在の認証状態を確認する

PowerShell で以下を実行する．

```powershell
cd "C:\Users\takum\Downloads\products\スライド生成デモ"
gh auth status
```

成功したら次へ進む．失敗したら，先に `docs/claude_handoff_gh_auth_persistence.md` の手順に従って `gh auth login` を恒久化する．

### 2. 未コミット変更を確認してコミットする

```powershell
git status --short
```

`docs/` など未コミットの変更があれば，以下でコミットする．

```powershell
git add README.md AGENTS.md docs outputs .gitignore
git commit -m "Add handoff docs and finalize slide deck guidance"
```

もしコミット対象が `docs/` のみなら，そのまま `git add docs` でもよい．

### 3. GitHub リポジトリを新規作成する

リポジトリ名は，この作業ディレクトリ名に合わせて次を第一候補とする．

- `slide-generation-demo`

日本語ディレクトリ名そのままではなく，GitHub 向けに英数字ハイフンへ正規化した名前を使う．

公開リポジトリで問題なければ以下を実行する．

```powershell
gh repo create slide-generation-demo --public --source . --remote origin --push
```

もし同名が埋まっている場合は，次の候補を使う．

- `pokemon-slide-demo`
- `pokemon-meta-slide-deck`

### 4. リモート設定と push を確認する

```powershell
git remote -v
git branch --show-current
git status
```

期待状態:

- `origin` が設定済み
- `main` が push 済み
- ワークツリーが clean

### 5. GitHub Pages 公開用の導線を追加する

最も単純なのは，リポジトリルートに `index.html` を置いて，`outputs/ポケモン現環境最強構築_スライド.html` へリダイレクトする方法．

以下の内容で `index.html` を作る．

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url=./outputs/%E3%83%9D%E3%82%B1%E3%83%A2%E3%83%B3%E7%8F%BE%E7%92%B0%E5%A2%83%E6%9C%80%E5%BC%B7%E6%A7%8B%E7%AF%89_%E3%82%B9%E3%83%A9%E3%82%A4%E3%83%89.html">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Redirecting...</title>
</head>
<body>
  <p><a href="./outputs/%E3%83%9D%E3%82%B1%E3%83%A2%E3%83%B3%E7%8F%BE%E7%92%B0%E5%A2%83%E6%9C%80%E5%BC%B7%E6%A7%8B%E7%AF%89_%E3%82%B9%E3%83%A9%E3%82%A4%E3%83%89.html">スライドを開く</a></p>
</body>
</html>
```

その後コミットする．

```powershell
git add index.html
git commit -m "Add index page for GitHub Pages entrypoint"
git push
```

### 6. GitHub Pages を有効化する

GitHub CLI または Web UI で，Pages の公開元を `main` ブランチの `/ (root)` に設定する．

CLIで可能なら以下を試す．

```powershell
gh api `
  -X POST `
  repos/:owner/slide-generation-demo/pages `
  -f source[branch]=main `
  -f source[path]=/
```

もしすでに Pages が設定済みで上記が失敗する場合は，設定確認に切り替える．

```powershell
gh api repos/:owner/slide-generation-demo/pages
```

CLI で難しければ，GitHub の Web UI から以下を設定する．

- Repository Settings
- Pages
- Build and deployment
- Source: `Deploy from a branch`
- Branch: `main`
- Folder: `/ (root)`

### 7. 公開URLを確認する

通常は以下の形式になる．

```text
https://<github-user>.github.io/slide-generation-demo/
```

Pages 設定後，数分待ってからアクセス確認する．

必要なら直接スライド本体のURLも確認する．

```text
https://<github-user>.github.io/slide-generation-demo/outputs/%E3%83%9D%E3%82%B1%E3%83%A2%E3%83%B3%E7%8F%BE%E7%92%B0%E5%A2%83%E6%9C%80%E5%BC%B7%E6%A7%8B%E7%AF%89_%E3%82%B9%E3%83%A9%E3%82%A4%E3%83%89.html
```

### 8. 完了後に報告してほしい内容

Claude からユーザーへは以下を返してほしい．

- GitHub リポジトリ URL
- GitHub Pages URL
- 実行したコミットID
- もし Pages の反映待ちがあるならその旨

## 補足

- この handoff は，Codex 側セッションで認証状態を確認できなかったため作成した
- Claude 側で端末操作とGitHub操作が可能なら，上記を順番に実行すればよい
