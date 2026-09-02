# Claude Code — Learning Notes

> Living document, updated as I learn. Source: CampusX "Claude Code" playlist + hands-on notes.

---

## 1. What Claude Code Is
Agentic coding assistant — plans, runs shell commands, edits files, iterates toward a goal. Shifts you from manual coder to builder/reviewer.

## 2. Vibe Coding vs. Agentic Coding
- **Vibe coding:** quick prompts, throwaway prototypes.
- **Agentic coding:** structured, iterative, production-grade. This course focuses on the latter.

## 3. Why Claude Code
Strong coding intelligence, handles large codebases well, agentic capabilities feel like a senior engineer pairing with you.

## 4. Prerequisites
Python, Flask, HTML/CSS, Git/GitHub.

## 5. Course Project
Expense Tracker App — dashboard, transaction management, filtering.

## 6. Practical Setup Notes
- Windows: use `python` (not `python3`).
- Create venv: `python -m venv venv`
- Activate: `source venv/Scripts/activate` (Git Bash) or `.\venv\Scripts\Activate.ps1` (PowerShell). Windows venvs use `Scripts/`, not `bin/`.
- Venv must be re-activated each new terminal session.
- Git default branch is `master`; GitHub defaults to `main` — push `master` or `git branch -M main` first.

## 7. Installation, Pricing & Setup
- Paid (~₹2000/mo). Free alt: Ollama cloud models or local models (e.g., Qwen 2.5).
- Setup flow: scaffold project → create/activate venv → run app → then bring in Claude Code.
- **Bash mode:** `!` — run terminal commands inline, kept in conversation context.
- Can query project structure/dependencies/functionality directly after init.
- Value: ongoing codebase tracking + automated bug fixes, not just one-off code gen.

## 8. Slash Commands
- **Sessions:** `claude -r` resumes; `/exit`, `/resume`, `/rename`.
- `/btw` — side question without polluting main context.
- `/export` — save chat to Markdown.
- `/model` — switch model (Opus: planning, Sonnet: implementation, Haiku: simple tasks).
- `/usage` — token consumption. `/permissions` — tool access control. `/voice` — voice mode. `/insights` — usage report.
- `/` alone lists all commands.

## 9. `/config`
- Central settings menu. Enable **thinking mode** here to see extended reasoning before answers.
- Also controls: default model, output verbosity, diff display style, notifications, theme, auto-compaction.
- Check `/config` first for anything that's a toggleable "mode."

## 10. Iterative Landing Page Updates (CampusX video)
- Core workflow: start session → prompt → review/apply changes → `git commit` + `git push`. Repeat per feature, one commit per logical change.
- **Footer links:** add Terms & Conditions / Privacy Policy links via a simple prompt-based edit.
- **New pages:** generate Terms & Conditions and Privacy Policy pages with routing + styling matched to the existing site theme, from a single prompt.
- **Hero section redesign:** Claude Code is multimodal — pass a reference image (mockup/screenshot) as context and it can redesign a section to match.
- **Modal popup:** implement a functional modal that embeds a YouTube video (e.g., "see how it works" explainer).
- Takeaway: iterative, prompt-driven development works well for maintaining/enhancing an existing codebase incrementally rather than big-bang rewrites.

## 11. Managing the Context Window (CampusX video)
- **What it is:** the model's "working memory" — max tokens it can process at once (4:16-7:51).
- **Real usable limit:** Claude Code models cap at 200k tokens, but system prompts, tool schemas, and the auto-compaction buffer eat into that — actual usable space is closer to 150k (8:47-20:19).
- **Why context burns fast:** every turn resends the *entire* conversation history, so longer sessions consume tokens exponentially. Split work into one session per feature rather than one marathon session (11:17-14:07).
- **Auto-compaction:** Claude automatically summarizes history once usage hits ~75-92% (23:25-25:54).
- **Manual `/compact`:** run it proactively (not reactively) when not mid-task, to control what gets summarized rather than leaving it to auto-compaction (25:54-29:49).
- **Sub-agents:** delegate isolated/parallel work to sub-agents — each gets its own fresh context window, keeping the main session lean (14:15-15:58).
- **`.claudecodeignore`:** exclude large, irrelevant files from context, same idea as `.gitignore` (30:56-33:26).
- **Best practices:**
  - One session per feature.
  - Use `/compact` proactively, not reactively.
  - Write focused, specific prompts.
  - Use sub-agents for exploratory work.

## 12. CLAUDE.md & the `.claude` Folder (CampusX video)
- **Why CLAUDE.md is necessary:** LLMs have no memory across sessions — without it you'd re-explain project structure and coding style from scratch every time (0:01-0:03).
- **Creating it:** write manually, or run `/init` to scan the project and auto-generate a foundational CLAUDE.md (0:05-0:08).
- **The `.claude` folder:** the project's "toolbox" — stores settings, custom slash commands, and sub-agents. Exists at two levels:
  - **Project level** — checked into the repo, shared with the team.
  - **Global/user level** — personal to your machine, not shared (0:17-0:21).
- **Auto Memory:** Claude Code can automatically learn and record patterns (e.g., project-specific preferences) into a `memory.md` file, loaded alongside CLAUDE.md in future sessions (0:39-0:41).
- **Best practices:**
  - Treat CLAUDE.md as a living document — audit it periodically (0:37-0:38).
  - Keep it under 200 lines for high-quality instruction following (0:32).
  - If the project grows large, split into rule files under `.claude/rules/`, or add sub-directory CLAUDE.md files scoped to that area (0:34-0:36).

## 13. Spec-Driven Development (CampusX video)
- **Vibe coding vs. Spec-Driven Development (SDD):** vibe coding is fast/accessible for prototypes but the AI makes significant unpredictable decisions, leading to a cycle of patches and corrections and loss of control (0:56-4:55). SDD prioritizes control and consistency by writing a detailed spec *before* any code — the spec becomes a "single source of truth" guiding the AI to build exactly what's intended (4:55-7:13).
- **The Spec-Driven Workflow** (a structured pipeline, not just prompting):
  1. **Spec Document** — the "why" and "what": problem statement, functional requirements, constraints, edge cases, acceptance criteria (7:13-12:40).
  2. **Technical Design Plan** — the "how": tech stack, data models, architecture (13:20-17:00).
  3. **Tasks, Coding & Validation** — break the design plan into discrete tasks, execute, then validate the final code against the original spec (17:00-19:00).
- **Implementation strategy (planned for upcoming videos):** integrate SDD with Git/GitHub —
  - New feature branch per task.
  - Use Claude to automate generating spec documents and technical plans.
  - Rigorous review at each stage (spec → design → validation), then PR to merge finished features (25:xx onward).
- Takeaway: SDD trades vibe-coding speed for predictability — worth it once a feature is non-trivial or touches shared/production code.

## 14. Open Questions / To Revisit
- (add as they come up)

---
*Last updated: 2026-09-01*
