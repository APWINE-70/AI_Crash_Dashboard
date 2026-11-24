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

---

## 9. Cloud Deployment & Dual-Cloud Architecture Knowledge (Learned via /learn)

### 9.1 Streamlit vs Vercel Serverless Architecture Conflict
- **Root Cause**: Deploying a Streamlit repository to Vercel triggers `@vercel/python` auto-detection when `app.py` is at root, resulting in `[PYTHON_ENTRYPOINT_NOT_FOUND]` because Streamlit is not a WSGI/ASGI application.
- **Technical Incompatibility**: Streamlit requires long-running processes with persistent WebSockets (`/_stcore/stream`), whereas Vercel is built for stateless, short-lived HTTP serverless invocations.

### 9.2 The Gold-Standard Solution: Dual-Cloud Hybrid Architecture
1. **Analytics Engine (Streamlit Community Cloud)**:
   - Hosts `app.py` directly from GitHub (`main` branch).
   - Manages state, persistent WebSockets, and Parquet in-memory cache.
2. **Web Portal & Domain (Vercel)**:
   - Hosts `index.html` as a pure static showcase with an embedded dashboard viewer.
   - **Invariable Rule**: Always include `.vercelignore` listing `app.py`, `requirements.txt`, `src/`, `data/` so Vercel builds `index.html` as static and never triggers `@vercel/python`.

---

## 10. Native Next.js / React Web Dashboard Architecture (Learned via /learn)

### 10.1 Why Native Next.js Replaces Streamlit on Vercel
- **Zero Server Overhead**: Eliminates Python serverless cold starts, WebSocket disconnects, and iframe cross-origin latency.
- **Instant CDN Performance**: First Load JS is only ~223 KB, pre-rendered statically with sub-second TTI worldwide.
- **Full Interactivity**: Client-side React components (Recharts / Tailwind CSS) with real-time filtering, 24x7 matrix heatmap, and CSV export.

### 10.2 Pre-Aggregated Data Pipeline Pattern
- Run `python src/pipeline/generate_web_analytics.py` to compress 194,726 rows from Parquet into `public/data/web_analytics.json` and `app/web_analytics.json` (277 KB).
- Next.js imports this bundle statically, achieving zero latency and 100% reliability for vocational competition evaluation.

### 10.3 Vercel Ignore Matching & Plotly 7 Compatibility
- **Plotly Express 7 Breaking Change**: `px.scatter_mapbox` was replaced with `px.scatter_map` in Plotly 7+. Use `if hasattr(px, 'scatter_map'): ... else: px.scatter_mapbox(...)` check to ensure full cross-version compatibility across Streamlit Cloud deployments.
- **Root-anchored .vercelignore**: Always prefix root directory ignore patterns with leading slashes (e.g. `/data/`, `/app.py`) so nested folders like `public/data/` or internal app data imports are not unintentionally ignored during Vercel cloud builds.

---

## 11. Connected Repositories & External Workspaces Registry

### 11.1 MRG_pro_Seriously Workspace
- **Local Directory**: `C:\Users\Surface\Documents\MrG`
- **Remote Origin**: `https://github.com/APWINE-70/MRG_pro_Seriously.git`
- **Default Branch**: `main`
- **Committer / Identity**: Wine (`winekae172@gmail.com`)
- **Credential Helper**: Windows Credential Manager (`manager`)
- **Dedicated Knowledge Base**: `C:\Users\Surface\Documents\MrG\AGENTS.md`

### 11.2 Empty Remote Git Binding Runbook
When linking a brand new / empty remote GitHub repository to a local directory:
1. **Binding Command**:
   ```powershell
   cd C:\Users\Surface\Documents\MrG
   git clone https://github.com/APWINE-70/MRG_pro_Seriously.git .
   ```
   *Note: Git outputs `warning: You appear to have cloned an empty repository.`, which sets `origin` and tracks `refs/remotes/origin/*` automatically while pointing to `branch main` without requiring manual `git remote add`.*
2. **First Commit & Push Tracking**:
   Because the remote has no commits yet, the initial push must configure upstream tracking:
   ```powershell
   git add .
   git commit -m "chore: initial repository structure and AGENTS.md"
   git push -u origin main
   ```
3. **Workspace Initialization Standards**:
   Every new repository must immediately have:
   - `AGENTS.md`: Operational memory, repository runbook, and conventions.
   - `README.md`: Project documentation and quick start.
   - `.gitignore`: Preventing accidental commits of virtual environments, secrets, or OS caches.

---

## 12. Power Outage Reliability Data Competition Runbook & Invariants (/learn)

For full competition specifications, refer to [COMPETITION_TASK_POWER_OUTAGE.md](COMPETITION_TASK_POWER_OUTAGE.md).

### 12.1 The 14 Injected Data Quality Patterns (100% Ground Truth Resolution)
1. **Buddhist Era Dates**: Convert `dd/mm/YYYY-543` to CE.
2. **Typo Years**: Extract year from `outage_id` (e.g. `OUT-2023-` -> 2023) or `end_time.year` when year is 2014, 2042, 2204.
3. **Swapped Timestamps**: Swap `start_time` and `end_time` when `end < start`.
4. **Duration Unit**: If `dur * 60 == (end - start)`, duration was entered in hours; recompute from timestamps.
5. **Placeholder Values**: Strip `9999`, `99999`, `14400` and recalculate from timestamps.
6. **Feeder ID Normalization**: Normalize `^[A-Z]{3}-F\d{2}$` ensuring Foreign Key match rate $\ge 99.64\%$.
7. **Cross-System Duplication**: Deduplicate exact rows first, then deduplicate on business key (`feeder_id + start_time`).
8. **Feeder Length & Customers**: Divide length in metres (>1000m) by 1000. Reconcile missing `CMI-F02` (5,321) and `LPG-F12` (2,260) to achieve exact total of 212,196 customers.
9. **Weather Metrics**: Convert Lamphun Jun-Jul 2023 °F to °C. Replace `-999` with 0.0. Cast thunderstorm string (`'Y'`/`'N'`) explicitly.

### 12.2 Reliability Metrics Benchmarks (Exact Match with Judge Answer Key)
- **Year 2566 (2023)**: 1,180 unplanned events | SAIFI = 6.43 | SAIDI = 833.7 mins | CAIDI = 129.6 mins
- **Year 2567 (2024 with storm)**: 1,414 unplanned events (+19.8%) | SAIFI = 7.82 (+21.5%) | SAIDI = 1,176.9 mins (+41.2%)
- **Year 2567 (Without Chiang Rai 2-day storm)**: 1,335 events | SAIFI = 7.45 | SAIDI = 914.5 mins (+9.7%)
- **Top 5 Feeders to Invest (32.5% of total damage)**: `CRI-F11` (9.5%), `CRI-F03` (6.2%), `LPG-F09` (5.6%), `CRI-F13` (5.6%), `CRI-F04` (5.6%).
- **Aging Equipment Signal**: `CMI-F14` equipment failure jumped from 5 to 19 (+280%).
- **3 Strategic Proposals**: Reduce SAIDI by **360.0 mins (-30.6%)** down to 816.9 mins.






