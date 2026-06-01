# Publish checklist

Replace `YOUR_GITHUB_USER` and `maintainer-digest` if you choose a different repository name.

```bash
git init
git add .
git commit -m "Initial open-source maintainer digest CLI"
gh repo create YOUR_GITHUB_USER/maintainer-digest --public --source=. --remote=origin --push
git tag v0.1.0
git push origin v0.1.0
```

After publishing:

1. Enable GitHub Actions.
2. Run the `Maintainer digest` workflow manually.
3. Add the generated `examples/MAINTAINER_DIGEST.md` to the README if you want a visible demo.
4. Open 2-3 realistic issues for roadmap items so the repo shows maintainable work.
5. Avoid fake stars, fake issues, or claims of adoption.
