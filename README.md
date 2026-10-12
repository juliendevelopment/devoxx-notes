# Devoxx notes

Site Astro + Starlight des notes Devoxx de Julien, publié sur
https://juliendevelopment.github.io/devoxx-notes/

Le contenu vient du vault Obsidian parent (`talks/`) :

- `talks/general note.md` → page d'accueil (takeaways, top talks) ;
- `talks/<Day NN> - …/note.md` + `images/` → une page « raw notes » par talk ;
- `talks/talks-to-see-by-theme.md` → « Talks I didn't see », sans les talks déjà notés.

Les notes du vault restent verbatim. Les passages en français sont traduits dans
`translations/<année>/<slug>.yml` (bloc `fr` exact → bloc `en`). Le sync signale
les traductions périmées et les lignes encore en français.

Mettre à jour le site :

```sh
python3 sync.py                   # vault parent, année 2026
npm run dev                       # aperçu sur http://localhost:4321/devoxx-notes/
git add -A && git commit -m "Update talks" && git push
```

La GitHub Action `Publish site` build le site (`npm run build`) et le publie sur GitHub Pages.
`src/content/docs/` et `src/sidebar.json` sont générés : ne pas les éditer à la main.
