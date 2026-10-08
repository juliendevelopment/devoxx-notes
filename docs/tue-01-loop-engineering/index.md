---
title: Tue 01 · Loop Engineering, beyond prompt, context, and harness engineering
---


# 09:30 loop

[▶ Video](https://youtu.be/A7ZIf8LkSvE)


[Loop Engineering, beyond prompt, context, and harness engineering](https://m.devoxx.com/events/dvbe26/talks/22912/loop-engineering-beyond-prompt-context-and-harness-engineering) by [Guillaume Laforge](https://m.devoxx.com/events/dvbe26/speaker/2951/guillaume-laforge) and [Wietse Venema](https://m.devoxx.com/events/dvbe26/speaker/24160/wietse-venema)
Room 8 · Deep Dive · 09:30-12:30

## Summary

This session introduces “Loop Engineering,” where developers build automated systems that steer coding agents autonomously. It covers core primitives, loop architectures, and safety practices for creating self-driving workflows that investigate, implement, and verify code, replacing manual prompting with robust AI-driven automation.

## Key points ⭐

- 2:18:00 Video Zack Lloyd

## Timeline

### [02:00](https://youtu.be/A7ZIf8LkSvE?t=120)
- stop prompting   start engeneering
- agg [?]   /goal   /learn

![](images/03m57.jpg)

Comparatif rapide des commandes de boucle dans les trois outils (état octobre 2026) :

/goal

|                                 | **Codex CLI** (OpenAI)                                                    | **Antigravity** (Google)                                   | **Claude Code** (Anthropic)                                         |
| ------------------------------- | ------------------------------------------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------- |
| **Boucle « jusqu'au but »**     | `/goal <objectif>`                                                        | `/goal <objectif>`                                         | `/goal <condition>`                                                 |
| **Disponible depuis**           | v0.128.0 (fin avril 2026)                                                 | Antigravity 2.0 (IDE, app desktop, CLI `agy`)              | v2.1.139 (11 mai 2026)                                              |
| **Qui décide que c'est fini**   | L'agent lui-même, via des prompts de continuation injectés en fin de tour | L'agent, dans sa boucle plan → exécute → vérifie → corrige | Un modèle évaluateur séparé (Haiku), via un Stop hook               |
| **Garde-fou**                   | Budget de tokens configurable                                             | Commande de build/test en dernière ligne du prompt         | « …or stop after N turns », 1 goal par session, 4000 caractères max |
| **Boucle périodique**           | — (via plugins/scripts externes)                                          | `/schedule`                                                | `/loop <intervalle> <prompt>`                                       |
| **Préparation avant la boucle** | `GOAL.md` + `AGENTS.md` (convention communautaire)                        | `/grill-me` pour figer la spec                             | `/plan` puis `/goal`                                                |

/learn

|                               | **Codex CLI**                            | **Claude Code**                                       | **GitHub Copilot CLI**                                          | **Google Antigravity**                                                       |
| ----------------------------- | ---------------------------------------- | ----------------------------------------------------- | --------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| **`/learn` natif**            | Non                                      | Non                                                   | Non                                                             | Non                                                                          |
| **Mémoire persistante**       | `AGENTS.md`, rédigé à la main            | `CLAUDE.md` via `/init`, puis `/memory` pour l'éditer | Copilot Memory, automatique, piloté par `/memory on\|off\|show` | Knowledge Items, automatiques, plus des rules et workflows écrits à la main  |
| **Qui écrit l'apprentissage** | Vous, ou l'agent si vous le lui demandez | Vous, ou l'agent si vous le lui demandez              | L'agent, en continu                                             | Un sous-agent dédié, à la fin de chaque conversation                         |
| **Transformer en skill**      | Skills (`SKILL.md`)                      | Skills, plus un skill-creator                         | Skills dans `~/.copilot/skills/`                                | Skills dans `.agents/skills/` (projet) ou `~/.gemini/config/skills` (global) |
| **Gouvernance**               | Fichiers versionnés dans Git             | Fichiers versionnés dans Git                          | Paramètres repo et utilisateur côté GitHub                      | Dossier Knowledge local, consultable dans l'IDE                              |

### [15:00](https://youtu.be/A7ZIf8LkSvE?t=900)
- quote

![](images/19m55.jpg)

### [18:00](https://youtu.be/A7ZIf8LkSvE?t=1080)
- Prompt , Context , Harness , loop , and graph

![](images/20m56.jpg)

### [21:36](https://youtu.be/A7ZIf8LkSvE?t=1296)
![](images/21m36.jpg)

### [25:00](https://youtu.be/A7ZIf8LkSvE?t=1500)
- graph -> multi loop

### [28:00](https://youtu.be/A7ZIf8LkSvE?t=1680)
- SOP   standard operated procédure

![](images/29m32.jpg)

![](images/30m02.jpg)

SOP vs skill

|                   | **SOP**                                                       | **Skill** (Claude Code, Codex, Antigravity…)                                                                   |
| ----------------- | ------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| **Lecteur**       | Un humain                                                     | Un agent IA                                                                                                    |
| **Déclenchement** | Quelqu'un décide de l'ouvrir et de le suivre                  | L'agent le charge lui-même quand la `description` du frontmatter correspond à la tâche, ou via `/nom-du-skill` |
| **Chargement**    | Lu en entier, une fois                                        | Progressif : seuls le nom et la description restent en contexte, le corps n'est chargé qu'au besoin            |
| **Contenu**       | Texte, checklists, captures d'écran                           | Instructions plus scripts, templates et fichiers de référence exécutables par l'agent                          |
| **Ton**           | Prescriptif, exhaustif, souvent pour l'audit et la conformité | Orienté décision, avec seulement ce que le modèle ne sait pas déjà                                             |
| **Exécution**     | L'humain agit                                                 | L'agent agit, éventuellement en lançant le script fourni                                                       |
| **Vérification**  | Signature, contrôle qualité                                   | Commande de test ou de build que l'agent peut lancer lui-même                                                  |

### [36:17](https://youtu.be/A7ZIf8LkSvE?t=2177)
![](images/36m17.jpg)

### [39:21](https://youtu.be/A7ZIf8LkSvE?t=2361)
![](images/39m21.jpg)

### [45:12](https://youtu.be/A7ZIf8LkSvE?t=2712)
![](images/45m12.jpg)

![](images/47m53.jpg)

### [54:00](https://youtu.be/A7ZIf8LkSvE?t=3240)
- /Browser

### [57:00](https://youtu.be/A7ZIf8LkSvE?t=3420)
- Skills

### [1:05:00](https://youtu.be/A7ZIf8LkSvE?t=3900)
- every day loop   Demo

![](images/1h05m02.jpg)

### [1:27:00](https://youtu.be/A7ZIf8LkSvE?t=5220)
- Model get distracted By Todo in the code
- More High thinking is set the more is Distracted

![](images/1h29m57.jpg)

### [1:30:00](https://youtu.be/A7ZIf8LkSvE?t=5400)
- Ralph loop explayn

![](images/1h33m19.jpg)

### [1:52:08](https://youtu.be/A7ZIf8LkSvE?t=6728)
![](images/1h52m08.jpg)

### [1:53:00](https://youtu.be/A7ZIf8LkSvE?t=6780)
- self improving
- Andrej Karpathy's Auto research
- Really specific to a contexte

### [1:58:00](https://youtu.be/A7ZIf8LkSvE?t=7080)
- Failure Mode

![](images/1h59m04.jpg)

![](images/2h00m21.jpg)

### [2:01:24](https://youtu.be/A7ZIf8LkSvE?t=7284)
![](images/2h01m24.jpg)

### [2:06:00](https://youtu.be/A7ZIf8LkSvE?t=7560)
![](images/2h06m00.jpg)

![](images/2h06m59.jpg)

![](images/2h08m01.jpg)

### [2:09:39](https://youtu.be/A7ZIf8LkSvE?t=7779)
![](images/2h09m39.jpg)

### [2:15:00](https://youtu.be/A7ZIf8LkSvE?t=8100) [?]
- graph engeneering
- Move from Human prompt to Built Something

![](images/2h15m56.jpg)

### [2:18:00](https://youtu.be/A7ZIf8LkSvE?t=8280) ⭐
- Video Zack Lloyd
- https://m.youtube.com/watch?v=tUPPVhBBcoM

![](images/2h18m33.jpg)

![](images/2h20m13.jpg)

### [2:22:00](https://youtu.be/A7ZIf8LkSvE?t=8520)
![](images/2h22m00.jpg)

## Extra notes

open rewrite , cli , sdk

|                     | **OpenRewrite**                                         | **Copilot CLI**                                | **Copilot SDK**                                               |
| ------------------- | ------------------------------------------------------- | ---------------------------------------------- | ------------------------------------------------------------- |
| **Nature**          | Moteur de transformation déterministe (AST)             | Agent IA, utilisé en interactif ou en headless | Le même agent, piloté depuis du code                          |
| **Résultat**        | Identique à chaque exécution                            | Variable                                       | Variable                                                      |
| **Qui décide**      | La recette                                              | L'agent, guidé par vous                        | L'agent, encadré par votre code                               |
| **Idéal pour**      | Transformations mécaniques sur des milliers de fichiers | Travail ponctuel, exploration, petites boucles | Orchestration complexe et répétée                             |
| **Coût**            | Gratuit                                                 | Premium requests                               | Premium requests                                              |
| **Exemple Theseos** | `javax` → `jakarta`, renommage d'API du framework       | « Migre ce service et fais passer les tests »  | Migrer 80 modules en parallèle, avec rapport et PR par module |

### **CLI headless**.

Souvent, oui. Le CLI en mode headless (`copilot -p "..."`) appelé depuis un script bash ou un job CI couvre déjà une grande partie des besoins :

```bash
for m in $(cat modules.txt); do
  git worktree add ../wt-$m
  (cd ../wt-$m && copilot -p "Applique le skill refactor-theseos sur $m, puis mvn -pl $m test jusqu'au vert")
done
```

Ça tient en dix lignes, c'est lisible par tout le monde et ça ne dépend d'aucune librairie en preview.

### L'échelle à suivre

Il faut monter d'un cran seulement quand le cran inférieur ne suffit plus :

1. **OpenRewrite seul**, si la transformation est entièrement mécanique.
2. **CLI interactif avec un skill**, pour mettre au point le workflow à la main.
3. **CLI headless dans un script ou en CI**, pour le répéter. C'est souvent suffisant.
4. **SDK**, quand il faut de l'orchestration, du contrôle fin ou de l'intégration.

## My take

