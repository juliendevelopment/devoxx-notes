---
title: Loop Engineering, beyond prompt, context, and harness engineering
description: 'Raw notes from Devoxx Belgium 2026: Guillaume Laforge, Wietse Venema'
banner:
  content: ⚠️ These are raw notes, typed or handwritten live during the talk. Expect transcription errors, typos and video timestamps that can be a few minutes off. <a href="/devoxx-notes/2026/notes/#how-to-read-these-notes">More</a>
---

<a class="video-button" href="https://youtu.be/A7ZIf8LkSvE" target="_blank" rel="noopener">▶ Watch the video</a>

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

Quick comparison of the loop commands in the three tools (as of October 2026):

/goal

|                                 | **Codex CLI** (OpenAI)                                                    | **Antigravity** (Google)                                   | **Claude Code** (Anthropic)                                         |
| ------------------------------- | ------------------------------------------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------- |
| **"Until the goal" loop**       | `/goal <objective>`                                                       | `/goal <objective>`                                        | `/goal <condition>`                                                 |
| **Available since**             | v0.128.0 (end of April 2026)                                              | Antigravity 2.0 (IDE, desktop app, CLI `agy`)              | v2.1.139 (11 May 2026)                                              |
| **Who decides it's done**       | The agent itself, via continuation prompts injected at the end of a turn  | The agent, in its plan → execute → verify → fix loop       | A separate evaluator model (Haiku), via a Stop hook                 |
| **Safeguard**                   | Configurable token budget                                                 | Build/test command on the last line of the prompt          | "…or stop after N turns", 1 goal per session, 4000 characters max   |
| **Periodic loop**               | — (via external plugins/scripts)                                          | `/schedule`                                                | `/loop <interval> <prompt>`                                         |
| **Preparation before the loop** | `GOAL.md` + `AGENTS.md` (community convention)                            | `/grill-me` to freeze the spec                             | `/plan` then `/goal`                                                |

/learn

|                               | **Codex CLI**                            | **Claude Code**                                       | **GitHub Copilot CLI**                                          | **Google Antigravity**                                                       |
| ----------------------------- | ---------------------------------------- | ----------------------------------------------------- | --------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| **Native `/learn`**            | No                                       | No                                                    | No                                                              | No                                                                           |
| **Persistent memory**         | `AGENTS.md`, written by hand             | `CLAUDE.md` via `/init`, then `/memory` to edit it    | Copilot Memory, automatic, driven by `/memory on\|off\|show`    | Knowledge Items, automatic, plus hand-written rules and workflows            |
| **Who writes the learning**   | You, or the agent if you ask it          | You, or the agent if you ask it                       | The agent, continuously                                         | A dedicated sub-agent, at the end of each conversation                       |
| **Turn into a skill**         | Skills (`SKILL.md`)                      | Skills, plus a skill-creator                          | Skills in `~/.copilot/skills/`                                  | Skills in `.agents/skills/` (project) or `~/.gemini/config/skills` (global)  |
| **Governance**                | Files versioned in Git                   | Files versioned in Git                                | Repo and user settings on GitHub                                | Local Knowledge folder, browsable in the IDE                                 |

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
| **Reader**        | A human                                                       | An AI agent                                                                                                    |
| **Trigger**       | Someone decides to open it and follow it                      | The agent loads it itself when the frontmatter `description` matches the task, or via `/skill-name`            |
| **Loading**       | Read in full, once                                            | Progressive: only the name and description stay in context, the body is loaded only when needed               |
| **Content**       | Text, checklists, screenshots                                 | Instructions plus scripts, templates and reference files the agent can run                                     |
| **Tone**          | Prescriptive, exhaustive, often for audit and compliance      | Decision-oriented, with only what the model doesn't already know                                               |
| **Execution**     | The human acts                                                | The agent acts, possibly by running the provided script                                                        |
| **Verification**  | Signature, quality control                                    | Test or build command the agent can run itself                                                                 |

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
| **Nature**          | Deterministic transformation engine (AST)               | AI agent, used interactively or headless       | The same agent, driven from code                              |
| **Result**          | Identical on every run                                  | Variable                                       | Variable                                                      |
| **Who decides**     | The recipe                                              | The agent, guided by you                       | The agent, framed by your code                                |
| **Best for**        | Mechanical transformations over thousands of files      | One-off work, exploration, small loops         | Complex, repeated orchestration                               |
| **Cost**            | Free                                                    | Premium requests                               | Premium requests                                              |
| **Theseos example** | `javax` → `jakarta`, framework API renaming             | "Migrate this service and make the tests pass" | Migrate 80 modules in parallel, with a report and PR per module |

### **CLI headless**.

Often, yes. The CLI in headless mode (`copilot -p "..."`) called from a bash script or a CI job already covers a large part of the needs:

```bash
for m in $(cat modules.txt); do
  git worktree add ../wt-$m
  (cd ../wt-$m && copilot -p "Apply the refactor-theseos skill to $m, then mvn -pl $m test until green")
done
```

It fits in ten lines, everyone can read it, and it doesn't depend on any preview library.

### The ladder to follow

Only move up one step when the step below is no longer enough:

1. **OpenRewrite alone**, if the transformation is fully mechanical.
2. **Interactive CLI with a skill**, to tune the workflow by hand.
3. **Headless CLI in a script or in CI**, to repeat it. Often enough.
4. **SDK**, when you need orchestration, fine control or integration.
