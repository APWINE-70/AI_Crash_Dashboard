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

---

## 7. Data Analysis & Dashboard Quality Benchmark (Vocational Competition Standard 2568 - 2572)

For full regulatory specifications and scoring rubrics, refer to [COMPETITION_RULES_DATA_ANALYSIS.md](COMPETITION_RULES_DATA_ANALYSIS.md). Any data pipelines, analytic scripts, or dashboard features developed in this workspace should adhere to the following gold-standard rubric criteria:

### 7.1 Data Preparation & Integrity (18 pts benchmark)
- **Completeness**: Validate primary keys, schema types, domain units (`°C`, `THB`), missing key fields $\le 1\%$, deduplication on primary/business keys, referential integrity (FK match rate $\ge 99\%$).
- **Cleaning & Outliers**: Explicit missing strategies (drop vs. impute with domain rationale), outlier detection (IQR / Z-score) with before-and-after reconciliation notes.
- **Reproducibility**: Maintain a clear Data Dictionary (field name, description, type, domain, examples) and deterministic execution pipelines.

### 7.2 Exploratory Data Analysis & Insights (18 pts benchmark)
- **Statistical Rigor**: Report central tendency and dispersion (`mean`, `median`, `std`, `IQR`, `min-max`).
- **Trends & Correlation**: Provide time series roll-ups, correlation heatmaps, cross-group comparisons (bar/box/violin), and faceted interactions.
- **Actionable Insights**: Provide 3–5 bullet points highlighting concrete decisions ("What $\rightarrow$ So What $\rightarrow$ Now What") backed by metrics ($\Delta\%$, rates, confidence/std).

### 7.3 Visualization & Dashboard Usability (26 pts benchmark)
- **Hierarchy**: Strict `Overview (KPIs) → Drill-down Details` flow.
- **Chart Selection**: Pick the right chart for the data type (categorical $\rightarrow$ bar; distribution $\rightarrow$ histogram/box; correlation $\rightarrow$ scatter + trend; time $\rightarrow$ line/area). Avoid misleading truncated axes.
- **Interactive Controls**: Filters, search bars, sortable tables, and export options (CSV/Excel/PDF).
- **Graceful State Handling**: Never leave blank empty screens upon filtering; provide descriptive empty-state messaging and quick reset actions.

### 7.4 Performance & Deployment (8 pts benchmark)
- **Response Latency**: Fast initial page load / TTI and sub-second interaction latency for filters.
- **Deployment Resilience**: Online web dashboard as primary target, accompanied by offline fallback scripts/Docker.

---

## 8. Competition Task & Primary Dataset Scope (1_crash_reports.csv)

For complete task specifications and deliverables, refer to [COMPETITION_TASK_CRASH_ANALYSIS.md](COMPETITION_TASK_CRASH_ANALYSIS.md).

### 8.1 Dataset Profile (`1_crash_reports.csv`)
- **Records**: 194,726 rows | **Fields**: 39 columns
- **Data Domain**: Road traffic crash reports spanning Temporal (`Crash Date/Time`), Geospatial (`Latitude`, `Longitude`, `Road Name`), Causality (`Weather`, `Driver Distracted By`, `Collision Type`), and Severity (`ACRS Report Type`, `Injury Severity`).
- **Data Preprocessing Invariants**:
  - **Missing Values**: Impute behavioral fields (`Driver Substance Abuse`, `Driver At Fault`) with appropriate domain category (e.g. `'UNKNOWN'`). Manage missing in `Route Type`, `Road Name`, `Cross-Street Name`, `Weather`, `Surface Condition`, `Traffic Control`.
  - **Outliers**: Handle invalid `Vehicle Year` (e.g. 0, 9999) and uncalibrated `Speed Limit` (0 mph/kph).
  - **Data Dictionary**: Document field definitions, transformed data types, domain units, and sample values.

### 8.2 Three Core Analytical Questions (Insight Targets)
1. **Driver Distraction & Severity**: How does `Driver Distracted By` correlate with accident severity (`Injury Crash`, `Fatal Crash`)?
   - *Target*: Rank high-risk behaviors causing highest injuries and fatalities.
2. **Environmental & Nighttime Impact**: How do `Weather & Surface Condition` during nighttime (`Dark`) impact `Collision Type` and severity?
   - *Target*: Segment accidents with limited visibility to isolate environmental risk.
3. **Off-Peak Geographic Hotspots**: Which locations (`Road Name` / `Municipality`) experience high crash density outside peak hours (10:00 AM – 4:00 PM), and how does `Traffic Control` correlate with crash frequency?
   - *Target*: Identify non-rush hour black spots for traffic control and signage optimization.

### 8.3 Deliverables Alignment
- **Web Dashboard**: Interactive Streamlit app providing overview KPIs, temporal filters, interactive heatmaps/charts, and tabular exploration.
- **User Documentation**: Infographic User Manual and quick start guide.
- **Presentation**: 15-minute slide deck with structured story (Problem $\rightarrow$ Method $\rightarrow$ Findings $\rightarrow$ Recommendations).


