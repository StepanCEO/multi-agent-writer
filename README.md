# multi-agent-writer

Multi-agent pipeline where four LLM agents collaborate to write an article:
a **Researcher** outlines the topic, a **Writer** drafts, a **Critic** reviews
(and sends the draft back for revision), and an **Editor** does the final polish.

Built on the plain OpenAI SDK — no frameworks, so the orchestration logic is
fully visible in ~60 lines of [pipeline.py](multi_agent_writer/pipeline.py).

```
topic ──> Researcher ──> Writer ──> Critic ──┐
                           ▲                 │ approved?
                           │    no (≤ N)     │
                           └─────────────────┤
                                             │ yes / limit reached
                                             ▼
                                          Editor ──> article.md
```

## Quickstart

```bash
git clone https://github.com/StepanCEO/multi-agent-writer
cd multi-agent-writer
pip install -r requirements.txt
cp .env.example .env          # add your OPENAI_API_KEY
python -m multi_agent_writer "Why RAG beats fine-tuning for FAQ bots"
```

The article lands in `output/<topic-slug>.md`.

```
$ python -m multi_agent_writer "Why RAG beats fine-tuning for FAQ bots"
Researcher: gathering key points for 'Why RAG beats fine-tuning for FAQ bots'
Writer: drafting
Critic: reviewing draft (attempt 1)
Writer: revising (revision 1 of 2)
Critic: reviewing draft (attempt 2)
Critic: approved
Editor: final polish

Done: output/why-rag-beats-fine-tuning-for-faq-bots.md (revisions: 1)
```

Works with topics in any language — agents answer in the language of the topic.

## How it works

| Agent | Role | Output |
|-------|------|--------|
| Researcher | Turns the topic into an angle + outline + key points | research notes |
| Writer | Writes a 600–900 word markdown draft; revises on feedback | draft |
| Critic | Scores structure/clarity/completeness, returns JSON verdict | `{approved, feedback}` |
| Editor | Final grammar/flow pass, guarantees a `# Title` | final article |

The Writer↔Critic loop is bounded by `MAX_REVISIONS` (default 2). If the critic
never approves, the editor still runs — best effort beats no article.

Each agent gets a `complete(system, user) -> str` callable instead of a client
object, so the whole pipeline is unit-tested with a scripted fake LLM — no API
key needed to run the tests.

## Configuration (.env)

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | — | required |
| `MODEL` | `gpt-4o-mini` | any chat completions model |
| `MAX_REVISIONS` | `2` | max Writer↔Critic loops |
| `TEMPERATURE` | `0.7` | sampling temperature |

## Tests

```bash
pip install pytest
pytest
```

## Project structure

```
multi_agent_writer/
├── __main__.py        # CLI entry point
├── config.py          # .env settings
├── llm.py             # thin OpenAI wrapper
├── pipeline.py        # orchestration + revision loop
└── agents/
    ├── researcher.py
    ├── writer.py
    ├── critic.py      # JSON verdict parsing
    └── editor.py
tests/
└── test_pipeline.py   # fake-LLM tests of the orchestration
```

## License

MIT
