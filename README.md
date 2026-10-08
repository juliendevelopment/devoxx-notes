# Devoxx Belgium 2026 — talk notes

Site MkDocs des notes de talk du vault (`../talks/<Day NN> - …/note.md` + `images/`).

Mettre à jour le site :

```sh
python3 sync.py   # recopie les talks dans docs/
git add -A && git commit -m "Update talks" && git push
```

La GitHub Action `Publish site` construit le site et le publie sur GitHub Pages.
`docs/` est généré : ne pas l'éditer à la main.
