---
title: 'Wed 03 · Harness Engineering: Building the System Around Your AI Coding Agent'
---


# 14:00 Harness engeneering

[▶ Video](https://youtu.be/6N6qFqn1_Uo)


[Harness Engineering: Building the System Around Your AI Coding Agent](https://m.devoxx.com/events/dvbe26/talks/4087/harness-engineering-building-the-system-around-your-ai-coding-agent) by [JI Darwish](https://m.devoxx.com/events/dvbe26/speaker/46151/ji-darwish)
Room 5 · Conference · 14:00-14:50

## Summary

AI coding agents are fundamentally simple: prompt a model, execute tool calls, feed results back, and repeat. This talk builds such an engine in Java, then iteratively adds context, constraints, and feedback to show how real tools improve reliability, safety, and understanding of their limits.

## Timeline

### [03:00](https://youtu.be/6N6qFqn1_Uo?t=180)
- Rebuilt something existing to learn
- ⚠ maintability is the hard point

![](images/04m02.jpg)

### [05:00](https://youtu.be/6N6qFqn1_Uo?t=300)
- gartner 40% Back Becouse un maintainable
- Agent = model + Harness
- Harness-engenering martin fowler

![](images/07m03.jpg)

### [09:41](https://youtu.be/6N6qFqn1_Uo?t=581)
![](images/09m41.jpg)

![](images/11m01.jpg)

### [13:00](https://youtu.be/6N6qFqn1_Uo?t=780)
- he speek about Budget and take core of it

### [14:00](https://youtu.be/6N6qFqn1_Uo?t=840)
- Boeckeler's a women
- 1- lint ? (java)

### [17:41](https://youtu.be/6N6qFqn1_Uo?t=1061)
![](images/17m41.jpg)

### [23:50](https://youtu.be/6N6qFqn1_Uo?t=1430)
![](images/23m50.jpg)

### [28:00](https://youtu.be/6N6qFqn1_Uo?t=1680)
- lint

![](images/28m48.jpg)

![](images/29m52.jpg)

### [31:00](https://youtu.be/6N6qFqn1_Uo?t=1860)
- MC [?] Bring lib for Angular
- lot about java test and Deterministic tool But not about hardness [?] until now

![](images/31m57.jpg)

### [35:16](https://youtu.be/6N6qFqn1_Uo?t=2116)
![](images/35m16.jpg)

![](images/37m27.jpg)

### [38:00](https://youtu.be/6N6qFqn1_Uo?t=2280)

### [49:46](https://youtu.be/6N6qFqn1_Uo?t=2986)
- workshops https://github.com/JiDarwish/outer-harness-workshop

![](images/49m46.jpg)

## Extra notes

Voici un panorama des principaux outils de linting et d'analyse statique, classés selon leur rôle et leur écosystème.

### 1. Écosystème Java

En Java, l'outillage est généralement segmenté entre le style, la détection de bugs profonds et les règles d'architecture :

- **Checkstyle :** Contrôle le respect des conventions de codage (nommage, indentation, imports inutilisés, visibilité). S'intègre directement via Maven/Gradle.
- **SpotBugs (successeur de FindBugs) :** Analyse le bytecode Java compilé pour détecter des patterns de bugs concrets (déréférencements `null`, fuites de descripteurs, failles de concurrence).
- **Google Error Prone :** S'exécute comme un plugin direct de `javac`. Il intercepte les erreurs courantes à la compilation et peut suggérer des correctifs automatiques.
- **PMD :** Analyse l'AST (arbre syntaxique) du code source pour repérer le code mort, la complexité cyclomatique excessive ou les patterns sous-optimaux.
- **ArchUnit :** Écrit des règles d'architecture sous forme de tests JUnit ordinaires. Permet de vérifier les dépendances de packages, les conventions d'annotations et les frontières de couches (ex. DDD / Hexagonale).
- **Spotless :** Formateur polyvalent de code souvent combiné avec `palantir-java-format` ou `google-java-format` pour garantir un formattage strict sans intervention manuelle.

### 2. Outils pour agents IA et contextes de développement

Ces linters ciblent spécifiquement les instructions, contextes et configurations fournies aux modèles de code :

- **agentlint (`agentlint.sh`) :** Analyse les fichiers `AGENTS.md` ou `CLAUDE.md` pour valider que les fichiers cités existent, que les commandes de build fonctionnent et qu'il n'y a pas de dérive de contexte.
- **repomix / repolint :** Outils d'audit pour vérifier la structure et la taille des dépôts avant de les injecter dans le contexte d'un LLM.
- **dotenv-linter :** Vérifie la syntaxe, les clés dupliquées et l'ordre des variables d'environnement (`.env`), évitant les erreurs de configuration d'environnement pour les agents locaux.

### 3. Autres écosystèmes majeurs

| Langage / Périmètre         | Outils de référence                                                               | Points forts                                                                                                                             |
| --------------------------- | --------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **TypeScript / JavaScript** | **ESLint** (règles & logique) **Biome / Prettier** (formatage rapide)             | Standard industriel de l'écosystème web ; règles modulaires et plugins de typage.                                                        |
| **Python**                  | **Ruff** **Mypy**                                                                 | `Ruff` (écrit en Rust) remplace Flake8, Black et isort avec une vitesse d'exécution quasi-instantanée. `Mypy` assure le typage statique. |
| **Go**                      | **golangci-lint**                                                                 | Méta-linter agrégeant des dizaines d'outils Go (`govet`, `staticcheck`, etc.) en parallèle.                                              |
| **Rust**                    | **Clippy**                                                                        | Fourni avec la toolchain standard de Rust ; détecte les inefficiences et idiomes non recommandés.                                        |
| **Infrastructure / DevOps** | **Hadolint** (Dockerfiles) **TFLint** (Terraform) **actionlint** (GitHub Actions) | Prévient les erreurs de configuration d'infrastructure avant l'exécution en CI/CD.                                                       |



CodeQL (développé par GitHub / Semmle) va bien au-delà d'un simple linter : il s'agit d'un moteur d'analyse sémantique et de sécurité par le code (Code-as-Data).
Plutôt que d'analyser du texte ou simplement l'AST (comme Checkstyle ou PMD), CodeQL compile le code source pour construire une véritable base de données relationnelle représentant :

 * L'arbre syntaxique abstrait (AST)
 * Le graphe de flot de contrôle (Control Flow Graph / CFG)
 * Le graphe de flot de données (Data Flow Graph)
 * L'analyse de propagation des données non fiables (Taint Tracking)
Pourquoi CodeQL est différent d'un linter standard

| Critère | Linter classique (Checkstyle, SpotBugs, ESLint) | CodeQL |
|---|---|---|
| Périmètre | Local (fichier par fichier ou classe par classe) | Global / Interprocédural (suit les données à travers tout le projet) |
| Objectif principal | Conventions, bugs courants, qualité de code | Failles de sécurité critiques (CWE, CVE, OWASP Top 10) |
| Mécanisme clé | Filtrage de patterns AST / Bytecode | Requêtes déclaratives (langage QL) sur le flux de données (Taint Analysis) |
| Exemple typique | « Variable non utilisée » ou « Égalité d'objets suspecte » | « Une entrée HTTP non filtrée atteint une requête SQL à travers 5 services » |
L'intérêt majeur : le Taint Tracking
Le concept central de CodeQL repose sur trois éléments :

 * Source : Un point d'entrée non sécurisé (ex. un paramètre @RequestParam Spring, un argument CLI, un header HTTP).
 * Sink : Une fonction sensible où l'exécution de données non assainies est dangereuse (ex. EntityManager.createNativeQuery(), Runtime.getRuntime().exec(), LDAPContext.search()).
 * Sanitizer : Une méthode qui nettoie ou valide la donnée (ex. un cast vers un entier, une validation par regex).
CodeQL trace mathématiquement le chemin reliant la Source au Sink. S'il n'y a pas de Sanitizer valide sur le chemin, la règle lève une alerte.
CodeQL dans un monde d'Agents IA
Pour un agent de développement (ex. OpenCode, Claude Code, GitHub Copilot) :

 * Garde-fou contre le code "halluciné" non sécurisé : Les LLMs ont tendance à générer du code qui compile et passe les tests unitaires, mais qui contient des failles de désérialisation, des injections SQL ou des SSRF subtiles. CodeQL bloque ces propositions en amont.
 * Format SARIF standardisé : CodeQL produit ses rapports au format standard SARIF (Static Analysis Results Interchange Format). Ce format JSON structuré inclut les coordonnées exactes du fichier, les extraits de code et le chemin complet du flux vulnérable, ce qui permet à un agent IA de parser le problème et d'itérer directement pour corriger la faille.
En résumé, si les linters veillent à la propreté et à la cohérence architecturale quotidienne, CodeQL constitue le scanner d'intégrité de sécurité approfondi exécuté lors de la compilation ou en pipeline CI/CD.

## My take

