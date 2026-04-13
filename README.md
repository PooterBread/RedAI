# RedAI (Work in progress)

RedAI is a Python tool for **authorized security testing**. It combines a local exploit database with an LLM (OpenAI or Anthropic) to match your target and goal to known methods or to draft new step-by-step approaches. Execution is gated by confirmations and safety checks.

It can run as a normal desktop app or be adapted for **Udoo Key** (RP2040 + ESP32) and optional **dual-chipset** setups where AI logic and execution are split across boards.

## Disclaimer

Use only on systems you own or have **explicit written permission** to test. Unauthorized access is illegal. You are responsible for how you use this software. The authors accept no liability for misuse.

## What it does

- Takes a **target** (e.g. URL or system) and a **testing goal** in plain language.
- **Searches** a SQLite database of exploits and methods.
- **Asks the AI** to pick an existing exploit or outline a new one when nothing fits well.
- **Runs** steps through a controlled executor (timeouts, blocked dangerous patterns, optional confirmation).
- **Records** execution history for review.

## Repository layout

**Single-machine (default)**

| File | Role |
|------|------|
| `main.py` | Entry point (interactive or CLI) |
| `ai_engine.py` | LLM integration |
| `database.py` | SQLite access |
| `exploit_executor.py` | Step execution and safety |
| `config.py` | Paths, provider, limits |
| `init_sample_data.py` | Optional sample rows |

**Dual chipset (RP2040 + ESP32 over UART)**

- RP2040 side: AI, database, decisions (`rp2040_ai_chipset.py`, shared `chipset_communication.py`).
- ESP32 side: network-oriented execution (`esp32_execution_chipset.py`, `network_exploits.py`).

See `DUAL_CHIPSET_SETUP.md` for wiring and roles. See `UDOO_KEY_SETUP.md` for MicroPython and hardware notes.

## Requirements

- Python 3.8+
- API key for **OpenAI** or **Anthropic** (cloud models keep the device light; no local GPU required for the default path)

## Install

```bash
pip install -r requirements.txt
```

## Configure

Set environment variables or a `.env` file in the project root:

**OpenAI**

```bash
export AI_PROVIDER=openai
export OPENAI_API_KEY=your_key
export MODEL_NAME=gpt-4o-mini
```

**Anthropic**

```bash
export AI_PROVIDER=anthropic
export ANTHROPIC_API_KEY=your_key
```

Optional: `DUAL_CHIPSET_MODE=true`, `CHIPSET_TYPE`, `UART_BAUDRATE` (see `config.py`).

## Initialize data

```bash
python init_sample_data.py
```

Recommended for a richer catalog:

```bash
python populate_vulnerability_database.py
```

That script adds many categorized entries (OWASP-style themes, common web and network patterns, etc.) for the matcher and AI to use.

## Run

**Interactive menu**

```bash
python main.py
```

Menu: run a test, browse exploits, add an exploit manually, view history, exit.

**CLI (target and goal on the command line)**

```bash
python main.py --target http://example.com --goal "test authentication behavior"
```

Optional: `--auto-confirm` skips execution confirmation (dangerous; only for fully trusted automation).

Typical flow: analyze target and goal, reuse or generate a method, confirm unless skipped, execute with logging under `logs/`.

## Configuration reference

| Setting | Meaning |
|---------|---------|
| `AI_PROVIDER` | `openai`, `anthropic`, or `local` (local needs extra setup in `ai_engine.py`) |
| `MODEL_NAME` | Model id for the provider |
| `MAX_EXECUTION_TIME` | Seconds cap per run (default 300) |
| `REQUIRE_CONFIRMATION` | Prompt before running steps (default true) |
| `LOG_LEVEL` | Python logging level |

## Database

SQLite (default path under `database/exploits.db`):

- **exploits** — metadata (name, description, target type, …)
- **methods** — ordered steps per exploit
- **execution_results** — past runs

## Safety behavior

The executor validates structure, can require confirmation, applies timeouts, blocks high-risk command patterns, and writes logs. This reduces accidental damage; it does not replace legal authorization or professional judgment.

## Troubleshooting

- **Missing API key** — Set the key and ensure `AI_PROVIDER` matches the provider.
- **Empty or sparse exploits** — Run `init_sample_data.py` and/or `populate_vulnerability_database.py`.
- **Failed runs** — Check reachability of the target, network, and `logs/execution.log`.

## Contributing

Contributions should preserve the educational and authorized-use focus, improve safety and clarity, and avoid encouraging abuse.

## License

Educational use. Use responsibly and only where you are allowed to test.
