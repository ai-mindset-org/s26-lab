---
name: research
description: "Unified, Exa-first, evidence-graded research skill. Modes: quick, scan, deep, update, self-stack. Presets: aim, edtech, competitor, market, product, video, visual, people, science, code. Use for quick lookup, diversified scans, deep multi-cycle research, temporal-diff updates, and source-graded synthesis."
version: 3.1-public
user_invocable: true
---

# /research – Exa-first, evidence-graded research skill

> **Public / anonymized version** shared from AI Mindset · Summer Lab S26.
> Personal plumbing (wrapper scripts, key locations, account status, absolute paths, sync jobs) has been removed. What remains is the **methodology**: how to run diversified, source-graded research instead of one generic search. Adapt the tool bindings to your own runtime.

Core principle: **do not run one generic search.** Define the question, split it into angles, run a semantic query fan-out, fetch key pages in full, grade the evidence, resolve contradictions, and synthesize into something you can act on.

Optimized for: strategy and market/competitor scans; product and technical research; people/experts/partners; deep research with update/diff over prior work; and inspecting/improving your own research stack.

---

## Command format

```text
/research [topic]                # auto mode
/research quick: [topic]         # 5-8 sources, direct answer
/research scan: [topic]          # 12-25 sources, diversified map
/research deep: [topic]          # 25-60 sources, multi-cycle synthesis
/research update: [topic]        # fresh research + temporal diff vs prior work
/research self-stack: [target]   # inspect local stack, diff docs, patch, visualize

/research aim|edtech|competitor|market|product|video|visual|people|science|code: [topic]
```

**Auto mode:** `quick` for a bounded factual question · `scan` for a landscape/options · `deep` for strategic, high-cost, or multi-angle decisions · `update` when a topic likely moved since prior work · `self-stack` when improving the research system itself.

---

## Tools

Use a semantic search provider (this skill assumes **Exa**) through whatever binding your runtime exposes (MCP or direct API). The practical loop is:

```text
web_search  →  web_fetch  →  advanced_search
```

| Capability | Use |
|-----------|-----|
| `web_search` | Semantic search. Inputs: query, numResults. |
| `web_fetch` | Full-page extraction of selected URLs. |
| `advanced_search` | Category, domain, date filters, highlights, summaries, subpages. |
| Agent / async runs | List-building, entity enrichment, structured output — only when a single search/fetch loop is the wrong shape. |

**Tool discipline:** search first, then fetch the most important URLs in full — do not rely on snippets alone. Do not invent tools your provider does not have. Read secrets from your local config; never hardcode or duplicate keys in the skill. Use sub-agents/parallelism only when explicitly asked.

---

## Query strategy

Semantic search returns pages close in embedding space, not exact keyword matches.

| Pattern | Use |
|---------|-----|
| **Describe the page** | Best default: `detailed case study of a cohort course improving completion and alumni engagement` |
| **Long specific query** | Beats short keywords |
| **Multiple phrasings** | Same intent, 2-3 framings, for source diversification |
| **Term-density query** | Exploratory discovery across a space |
| **Category filter** | `category:people`, `company`, `research paper`, `news`, `personal site` |

**Query fan-out**, per angle:
1. Generate 2-3 queries with different semantic shapes.
2. Search `numResults: 8-15`.
3. Deduplicate by canonical URL and domain.
4. Fetch 3-8 best URLs in full.
5. Record why each source was included or discarded.

**Advanced moves** (only when they improve precision): category sweeps per source class; highlights/summaries first on large result sets, then fetch survivors; domain-constrained validation on official docs/filings; recency sweeps for fast-moving markets; personal-site sweeps for practitioner insight; browser fallback only when a page is dynamic/auth-gated.

---

## Modes

### quick
Bounded lookup. 2-3 searches, fetch 1-3 URLs if snippets are thin. Output: **answer · sources · confidence · next steps.**

### scan
Diversified landscape. 4-6 angles → query fan-out → fetch best in full → source map → contradictions and gaps. Output: **summary · source map table · angle findings · gaps · recommendations.**

### deep — three cycles

**Cycle 1 — broad search.** Pick 4-5 streams, each a different lens:

| Lens | Finds |
|------|-------|
| **Analytical** | definitions, taxonomy, canonical sources |
| **Contrarian** | criticism, failures, null results, why-not |
| **Mechanistic** | causal chain, how it works |
| **Systems** | interactions, second-order effects |
| **Pragmatic** | implementation, pricing, workflows |

**Cycle 2 — critic + deep dives.** Run a critic pass (contradictions, weak evidence, missing angles, source concentration, hidden assumptions). Generate 3-5 hypotheses with test and priority. Run deep dives on the highest-information gaps. If a claim stays contested, mark it **genuinely uncertain** and state what evidence would resolve it — do not force resolution.

**Cycle 3 — synthesis + verification.** Synthesize across streams (do not retell them). Verify top numerical claims with separate searches. Output: exec summary · source ledger · evidence map · stream findings · cross-angle insights · contradictions · unknowns · recommendations.

### update / temporal diff
Re-research an existing topic. Run fresh research first (do not anchor on the old conclusion), then classify changes: **CONFIRMED · REVISED · CONTRADICTED · OBSOLETE · NEW.** Add a temporal-diff table and a stability score (`CONFIRMED / total claims`).

### self-stack
Improve the research system itself (skill body, tool routes, config, visual map). Read local truth first; collect external truth only where behavior can change outside the repo (API docs, pricing, changelog); diff behavior; patch the smallest source of truth; update the visual map; verify with grep/tests/smoke calls; report caveats separately from real failures.

---

## Evidence ledger + source-credibility firewall

The core mistake this prevents: **grading the container, not the claim — reading production polish as authority.**

Grade every source on **two independent axes**, then judge the claim separately:

- **Authority:** **P** primary (original data, peer-reviewed, official docs/specs, filings) · **S** secondary (named-author journalism with method, analyst reports showing methodology, practitioner write-ups linking primaries) · **T** tertiary (aggregators, listicles, SEO, undated/anonymous).
- **Independence:** **Ind** no stake · **Int** benefits if the claim is believed (vendor/competitor blog about its own category, sponsored, investor deck) · **Unknown** → treated as **Interested** for gating.
- **Sub-flags:** `⚠vendor` (interested first-party) · `manipulable` (Reddit/G2/Trustpilot/App-Store reviews — never an independent chain alone).
- **First-party-data carve-out:** raw first-party numbers are **Primary regardless of author interest**; the Interested flag attaches to the *interpretation*, not the raw data.

**Echo-chain rule:** two sources tracing to the same PR / dataset / wire story = **one** chain. Agreement across *opposing-interest* parties counts as near-independent (strong).

**Confidence floor by independence:**

| Evidence | Confidence |
|----------|-----------|
| ≥2 aligned independent chains, ≥1 Independent-Primary | **High** |
| Single Independent-Primary chain | **Medium** — thin but trustworthy (not crushed to Low) |
| Single Interested/Unknown chain, or all-Interested | **Low** — write as "X claims…", never bare fact |

**Vetting pass:** get a second opinion from a judge that did **not** do the collecting (your priors are anchored to the sources you skimmed). Multi-agent: a separate Source-Vetting judge. Single-context: an explicit adversarial re-read pass. Fail-open: if vetting is low-confidence, treat unvetted sources as Unknown = Interested and stamp "⚠ ledger degraded".

**Diversity:** no single domain > 25% of sources. Default results skew US/English — add a geographic qualifier if the topic is global.

**Credibility gate (before shipping scan/deep):** every load-bearing conclusion has ≥1 independent corroboration chain **or** is written as "X claims…" / flagged `⚠uncorroborated`. No corporate-blog claim about its own category is restated as bare fact.

```markdown
| ID | Source | Type | Date | Claim | Authority (P/S/T) | Independence (Ind/Int/Unknown) | sub-flag | Confidence |
```

> For **"where is the market fragile / how do we enter?"** questions, hand off to an `attack-surface` method (Unspoken Insights → Fragile Assumptions → Stress-Test → Opportunity Mapping). For **"decompose to fundamentals"**, hand off to a `first-principles` method.

---

## Domain adapters

Pick the closest and merge with mode instructions. Each names default angles and an A/B/C/D source hierarchy.

- **aim / education** — audience and pains · learning design · community and retention · content and distribution · ops and tooling · business model.
- **competitor / company** — product · market position · business model · go-to-market · user sentiment · risks. Red flags: revenue claim from one weak source; "market leader" without a metric; TAM with no bottom-up decomposition; no bear case.
- **market / macro** — demand · supply · economics · regulation · scenarios · risks. Prefer official stats and primary reports; treat consulting forecasts as directional.
- **product** — user needs · fit · feasibility · landscape · distribution · risks.
- **video / content** — audience · format · platform · production · distribution · monetization.
- **people / experts** — direct profiles (`category:people`) · own platforms · proof of work · network signals · criticism · contact path. Confidence: confirmed / likely / possible / rumored.
- **science** — foundations · SOTA · mechanisms · replications · methodology · open problems.
- **code** — official docs · reference implementations · architecture · issues/PRs · versioning · security.

---

## Output style

Start with the main point. Cite sources as markdown links. Include confidence and next steps. Separate facts from inference. Mark stale or uncertain information. Avoid: generic landscape overview without decisions, uncited claims, one-source conclusions, pretending contested evidence is settled.

Save research only when asked or when the work is large enough that losing it would be wasteful and the destination is clear. Use a consistent naming convention and YAML frontmatter (`type: research`, `mode`, `date`, `refs`). Do not create new folders.

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| One generic query | Angle-based query fan-out |
| Only search snippets | Fetch key URLs in full |
| Many links, no synthesis | Build an evidence map and cross-angle insights |
| No critic pass | Always search criticism/limitations in scan/deep |
| Treating search as exact match | Describe target pages semantically |
| No source grading | Use the evidence ledger + firewall |
| No temporal awareness | Use update mode for moving fields |
| Overbuilding every task | Quick for bounded questions, deep for strategy |
