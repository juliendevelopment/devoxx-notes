# Devoxx notes

Site MkDocs des notes de talk Devoxx, une section par année (`docs/<année>/`).
Chaque année vient d'un vault Obsidian : `<vault>/talks/<Day NN> - …/note.md` + `images/`.

Mettre à jour le site :

```sh
python3 sync.py                   # vault parent, année 2026
python3 sync.py <vault> <année>   # une autre édition
git add -A && git commit -m "Update talks" && git push
```

La GitHub Action `Publish site` construit le site et le publie sur GitHub Pages.
`docs/` est généré : ne pas l'éditer à la main.
