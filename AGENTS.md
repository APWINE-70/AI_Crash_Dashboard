# AGENTS.md - AI Crash Dashboard Knowledge Base

Welcome to the **AI Crash & Incident Dashboard** codebase. This document serves as the persistent repository memory, operational runbook, and architectural guide for AI agents working in this project.

---

## 1. Project Overview & Mission

- **Repository**: `AI_Crash_Dashboard`
- **Remote Origin**: `https://github.com/APWINE-70/AI_Crash_Dashboard.git`
- **Default Branch**: `main`
- **Domain**: AI/ML Reliability, Model Crash Telemetry, Incident Analytics, and MTTR (Mean Time to Recovery) tracking.
- **Goal**: Provide a high-performance, real-time dashboard for engineering teams to detect, analyze, and mitigate failures across multi-model AI production environments (OOMs, rate limits, latency spikes, hallucinations, context overflows).

---

## 2. Technical Architecture & Stack

| Layer | Technology | Details |
| :--- | :--- | :--- |
| **Runtime** | Python 3.10+ | Strict type hinting encouraged for utilities |
| **Frontend UI** | Streamlit (>=1.30.0) | Interactive wide-layout web interface |
| **Analytics & Data** | Pandas (>=2.0.0), NumPy | Telemetry aggregation, log filtering, time-series resampling |
| **Visualization** | Plotly (>=5.18.0) | Interactive responsive charts (`px.line`, `px.pie`, `px.bar`) |
| **Version Control** | Git / GitHub | Trunk-based development on `main` |

---

## 3. Directory Layout

```text
C:\adisak\AI (Repository Root)
├── .git/               # Git metadata and remote bindings
├── .gitignore          # Git exclusion rules (venv, caches, secrets)
├── AGENTS.md           # This agent knowledge base and instructions
├── README.md           # Developer onboarding and user documentation
├── requirements.txt    # Python package dependencies
└── app.py              # Main Streamlit dashboard application
```

*Future modularization guidelines:*
- Place reusable data processing routines under `src/analytics/` or `utils/`.
- Place chart builders and component styling under `src/components/`.
- Mock or synthetic data fixtures should reside under `tests/fixtures/` or `data/sample/`.

---

## 4. Git & Repository Conventions

### 4.1 Branching Strategy
- `main`: Production-ready branch. All changes must be tested before merging.
- Feature branches: `feat/<feature-name>`, `fix/<issue-name>`, `docs/<topic>`.

### 4.2 Commit Message Standard
Follow Conventional Commits:
- `feat: add new GPU temperature telemetry chart`
- `fix: resolve division by zero in MTTR calculation when incidents are empty`
- `docs: update AGENTS.md with new incident taxonomy`
- `refactor: extract data loading logic into utils/loader.py`
- `chore: update requirements.txt dependencies`

### 4.3 Clean Workspace Hygiene
- Never commit virtual environments (`.venv/`, `venv/`), IDE configuration (`.vscode/`, `.idea/`), or OS cache files (`Thumbs.db`).
- Never commit `.env` or secrets (API keys, connection strings).

---

## 5. Development & Verification Runbook

### 5.1 Environment Setup
```powershell
# Create virtual environment
python -m venv .venv

# Activate environment (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 5.2 Syntax and Compilation Verification
Before committing any Python changes, agents **must** verify syntax:
```powershell
python -m py_compile app.py
```

### 5.3 Running the Application
```powershell
streamlit run app.py
```

---

## 6. Learned Knowledge & Agent Best Practices

### 6.1 Streamlit State & Caching Patterns
- Use `@st.cache_data` for functions that load, process, or filter telemetry DataFrames. This prevents expensive recalculation on every UI interaction.
- Use `@st.cache_resource` for database connections, API clients, or ML model sessions.
- Always check for empty DataFrames before rendering charts or computing statistical metrics (`.mean()`, `.sum()`) to avoid runtime crashes.

### 6.2 Data Schema Standard for Incidents
Every incident event in the system must conform to the following schema:
```python
{
    "Incident ID": str,            # Unique identifier, e.g. "INC-1042"
    "Timestamp": datetime,         # Event timestamp
    "Model": str,                  # e.g. "GPT-4o", "Claude-3.5-Sonnet", "Gemini-1.5-Pro"
    "Incident Type": str,          # Taxonomy: "OOM / GPU Memory Leak", "API Rate Limit (429)", etc.
    "Severity": str,              # "Critical" | "High" | "Medium" | "Low"
    "Recovery Time (min)": float,  # Duration until recovery
    "Status": str                  # "Resolved" | "Investigating"
}
```

### 6.3 Plotly Visualizations in Streamlit
- Always use `use_container_width=True` when rendering `st.plotly_chart(fig, use_container_width=True)` so charts adapt to different screen resolutions.
- Set explicit chart heights (e.g. `height=320` to `height=380`) to maintain balanced visual hierarchy.
- Use standard color maps for severity levels to maintain intuitive cognitive feedback:
  - **Critical**: `#FF4B4B` (Red)
  - **High**: `#FFAA00` (Orange)
  - **Medium**: `#0068C9` (Blue)
  - **Low**: `#29B5E8` (Light Blue)

### 6.4 Safety & Guardrails for AI Agents
1. **Verify Before Push**: Always run `git status` and test code syntax before staging and pushing.
2. **Atomic Commits**: Group related changes logically.
3. **Preserve User Intent**: Do not remove existing components or filters without explicit instruction.
4. **Update Knowledge**: When adding new modules, conventions, or troubleshooting fixes, update `AGENTS.md` to ensure future agents inherit the context.
