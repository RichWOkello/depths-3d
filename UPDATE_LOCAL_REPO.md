# Publish Depths 3D v6.0.0 to your existing GitHub repository

Target repository: `https://github.com/RichWOkello/depths-3d`  
Local Windows project: `myProjects\depths-3d`

1. Download the **Depths3D_v6.0.0_GitHub_Ready.zip** package. Extract it and **copy the files inside the extracted folder**, not the outer folder itself.
2. Paste into your existing local `myProjects\depths-3d` and select **Replace files in the destination**. Do **not** delete the old directory or its hidden `.git` directory.
3. In that original repository folder, open Git Bash or terminal and run:

```bash
git status
git add -A
git commit -m "Release Depths 3D v6.0.0 - The Bestiary Expansion"
git push origin main
git tag -a v6.0.0 -m "Depths 3D v6.0.0 - The Bestiary Expansion"
git push origin v6.0.0
```

4. Open https://github.com/RichWOkello/depths-3d/releases/new, select the `v6.0.0` tag and use `RELEASE_NOTES.md` as the description. Publish the GitHub release.
5. After Pages deploys, check https://richwokello.github.io/depths-3d/ and verify the menu displays **v6.0.0**.

**Important:** Only tag this version once. If `v6.0.0` already exists, stop and inspect the existing tag; never force-push a release tag without deliberate review. The generated ZIP does not contain `.git`; all your repo history is preserved when you paste into your existing directory. GitHub Pages must be configured to serve `/ (root)` of `main` or its corresponding deployment workflow.

### Verification before tagging
Run `node --check src/game.js` and `python build.py`, then test `index.html` and `PLAY_DIRECTLY.html` in a browser. These checks do not certify real GPU performance or full gameplay.

**Windows shortcut:** After pasting into the original repo folder, run `PUBLISH_V6_WINDOWS.cmd` from there. It checks for `.git` and tag collisions before committing, pushing and tagging. Review its source before running.
