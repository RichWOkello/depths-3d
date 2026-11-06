# Update your local `depths-3d` repository to v5.0.0

This ZIP is a **drop-in update** for your existing local clone of `RichWOkello/depths-3d`. It contains repository files **at the ZIP root**, not inside an additional versioned folder. You will push the changes yourself.

## Windows Explorer workflow (no command-line copying required)

1. In your existing `depths-3d` local repository, **commit any unfinished changes or make a backup**. Keep the `.git` folder untouched.
2. Extract `Depths3D_v5.0.0_GitHub_Ready.zip` to a temporary folder (for example, Downloads).
3. Open that extracted folder and **select its contents**, including the hidden `.github` directory and dotfiles if visible.
4. Copy the contents into your **existing local `depths-3d` folder**. Choose **Replace files in destination** when prompted. Do not replace the `.git` folder; none is included.
5. Open the local repository in VS Code or a terminal. You should see `index.html`, `src/`, `depths_3d.ipynb`, `README.md`, `CHANGELOG.md`, `RELEASE_NOTES.md` and `.github/` directly at the repository root.
6. Review the changed files with `git status` before committing.

## Commands to validate, commit and push

Run in your local `depths-3d` directory, **not** the temporary extracted folder:

```powershell
python build.py
node --check src/game.js
python -m json.tool depths_3d.ipynb > $null
git status
git add -A
git commit -m "release: Depths 3D v5.0.0 — The Abyssal Expansion"
git push origin main
```

If Node.js is not installed, skip the `node --check` line, but run the game in your browser before publishing. If `python` on Windows is unavailable but the Python launcher is installed, use `py build.py` instead.

The generated build output is already included in the package. Running `build.py` confirms the four outputs match the local source.

## Verify GitHub Pages

The screenshots show GitHub Pages has **already deployed** from your existing repository. After the push, open:

**https://richwokello.github.io/depths-3d/**

If GitHub Pages still shows the old game, check GitHub → **Actions** or **Settings → Pages**, wait for the deployment to complete, and hard-refresh your browser (`Ctrl+F5`).

## Optional Git tag and GitHub Release

Your repository already contains tags. First check whether `v5.0.0` exists:

```powershell
git tag -l v5.0.0
```

If it does **not** exist, run:

```powershell
git tag -a v5.0.0 -m "Depths 3D v5.0.0 — The Abyssal Expansion"
git push origin v5.0.0
```

In GitHub, open **Releases → Draft a new release**, select `v5.0.0`, and paste the text from `RELEASE_NOTES.md` (you can upload the ZIP as an optional release asset). Creating a GitHub Release is separate from updating Pages.

## Files that matter most

| File or folder | Why it matters |
| --- | --- |
| `index.html` | GitHub Pages launches this page. |
| `src/game.js`, `src/game.html`, `src/*.webp` | Canonical game source and art. |
| `depths_3d.ipynb` | Google Colab version and README badge target. |
| `build.py` | Keeps browser and Colab builds aligned. |
| `README.md` | Main GitHub landing page. |
| `.github/workflows/verify.yml` | Automatic syntax/build verification on GitHub. |

**Important:** No GitHub upload, commit, tag or release is performed by this package. You control when to publish.
