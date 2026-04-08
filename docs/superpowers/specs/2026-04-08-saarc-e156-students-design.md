# SAARC E156 Student Assignment Platform — Design Spec

**Date**: 2026-04-08
**Author**: Mahmood Ahmad / Claude
**Status**: APPROVED
**Location**: `C:\saarc-e156-students\`
**GitHub**: `mahmood726-cyber/saarc-e156-students`
**Pages**: `mahmood789.github.io/saarc-e156-students/`
**Target audience**: Ziauddin Medical University (Karachi, Pakistan)

---

## 1. Scope

190 E156 micro-papers analyzing clinical trial equity across 8 SAARC nations (India, Pakistan, Bangladesh, Sri Lanka, Nepal, Afghanistan, Bhutan, Maldives), with special emphasis on Pakistan. Each paper follows the E156 format: exactly 7 sentences, at most 156 words, single paragraph.

Dual purpose:
- **Research output**: Publication-grade E156 papers + interactive dashboards
- **Student assignments**: Ziauddin students rewrite AI-drafted papers for Synthesis Medicine Journal

## 2. Data Source

ClinicalTrials.gov API v2 — public registry, no API key required. Query interventional trials by country location filter for all 8 SAARC nations.

## 3. Group Structure (5 groups, 190 papers)

| Group | Directory | Theme | Papers |
|-------|-----------|-------|--------|
| 1 | `geographic-equity/` | Geographic Equity & Spatial Justice | 35 |
| 2 | `health-disease/` | Health & Disease Burden | 35 |
| 3 | `governance-justice/` | Governance, Justice & Sovereignty | 35 |
| 4 | `methods-systems/` | Methods, Design & Research Systems | 35 |
| 5 | `pakistan-deep-dive/` | Pakistan Deep-Dive | 50 |

### Group 5 Sub-themes

| Sub-theme | Papers | Focus |
|-----------|--------|-------|
| Provincial Inequity | 10 | Punjab/Sindh/KPK/Balochistan/ICT trial density, urban-rural, per-capita gaps |
| Institutional Concentration | 8 | Aga Khan, Ziauddin, CMH/MH, Shaukat Khanum, public hospitals |
| Disease-Specific Gaps | 12 | CVD, diabetes, hep B/C, TB, polio, maternal, thalassemia, dengue |
| Sponsor & Sovereignty | 8 | Foreign vs domestic, pharma vs academic, DRAP, data ownership |
| Workforce & Methods | 7 | PI demographics, completion rates, registration quality, phases |
| Karachi Lens | 5 | Karachi-specific analyses — Ziauddin students' home city |

## 4. Paper Topics

### Group 1 — Geographic Equity & Spatial Justice (35 papers)

1. SAARC Trial Density Map — trials per million population across 8 nations
2. India Dominance Index — India's share of all SAARC trials vs population share
3. Pakistan Per-Capita Deficit — Pakistan trials/capita vs regional average
4. Bangladesh Growth Trajectory — trial registration trends 2005-2025
5. Sri Lanka Punch-Above-Weight — small nation, disproportionate trial output
6. Nepal Mountain Access Barrier — geographic barriers to trial site distribution
7. Afghanistan Conflict Zone Trials — trials conducted amid active conflict
8. Bhutan Micro-State Research — smallest SAARC nation's trial landscape
9. Maldives Island Isolation — archipelago challenges for multi-site trials
10. Capital City Monopoly Index — % trials in capital vs rest of country
11. Cross-Border Trial Networks — multi-SAARC-country trial collaborations
12. Urban-Rural Site Distribution — urban concentration across all 8 nations
13. Spatial Gini Coefficient — inequality index of trial site distribution
14. Herfindahl Site Concentration — HHI of trial sites within each country
15. Regional Clustering Patterns — trial hotspot identification (Moran's I)
16. Coastal vs Interior Disparity — maritime cities vs inland regions
17. Population-Weighted Trial Gap — trials weighted by district population
18. Border Region Research Deserts — trial activity near international borders
19. Megacity Trial Absorption — Mumbai/Delhi/Karachi/Dhaka concentration
20. Second-Tier City Emergence — trial growth in non-capital urban centers
21. Rural Reach Coefficient — distance from nearest trial site for rural populations
22. Site Fragmentation Index — geographic spread of multi-site trials
23. Landlocked Penalty (Nepal/Bhutan) — logistics cost proxy for landlocked nations
24. Monsoon Belt Trial Seasonality — enrollment timing vs monsoon season
25. Economic Corridor Alignment — trial sites along CPEC/trade routes
26. Conflict-Stability Trial Gradient — trial density by peace index
27. Diaspora Return Research — trials at diaspora-linked institutions
28. SEZ & Medical Tourism Sites — trials at special economic / medical tourism zones
29. Regional Health Expenditure Match — trial density vs provincial health spending
30. Altitude & Access Barriers — high-altitude regions (Nepal, KPK, Kashmir)
31. Delta & Floodplain Populations — Bangladesh delta, Indus basin trial access
32. Spatial Entropy Index — evenness of trial distribution
33. Distance-to-Trial Burden — mean population distance to nearest site
34. Intra-SAARC Disparity Ratio — ratio of most to least trial-dense nation
35. Geographic Equity Trend — is distribution becoming more or less equitable over time?

### Group 2 — Health & Disease Burden (35 papers)

1. Cardiovascular Trial Gap — CVD is #1 killer, are trials proportional?
2. Diabetes Epidemic Mismatch — diabetes prevalence vs trial volume
3. TB Trial Landscape — tuberculosis trials across SAARC (high-burden region)
4. Hepatitis B/C Hotspot — Pakistan/India hep burden vs trial response
5. Maternal Mortality Crisis — maternal health trials vs MMR
6. Dengue & Vector-Borne — dengue, chikungunya, Zika trial activity
7. Polio Last-Mile Trials — Pakistan/Afghanistan, last 2 polio-endemic nations
8. Thalassemia & Haemoglobinopathies — genetic disease burden vs research effort
9. Mental Health Desert — depression, suicide, substance use trial scarcity
10. Childhood Pneumonia & Diarrhoea — top child killers, trial representation
11. Cancer Trial Disparity — oncology trials vs cancer mortality
12. Rheumatic Heart Disease — neglected in rich countries, deadly in South Asia
13. Chronic Kidney Disease — CKDu epidemic (Sri Lanka), general CKD burden
14. Neonatal Mortality Focus — neonatal trials vs neonatal death rate
15. Malnutrition & Stunting — nutrition intervention trials
16. Antimicrobial Resistance — AMR trials in a region with high antibiotic misuse
17. Snakebite Neglected Crisis — South Asia = global snakebite capital
18. Leishmaniasis (Kala-azar) — Nepal/Bangladesh/India visceral leishmaniasis belt
19. Air Pollution & Respiratory — COPD, asthma trials vs pollution burden
20. Hypertension Awareness Gap — hypertension prevalence vs detection/treatment trials
21. HIV Low-Prevalence Paradox — low prevalence but concentrated epidemics
22. Surgical Trial Scarcity — Lancet Commission surgical gaps
23. Eye Health & Blindness — cataract, trachoma trials in South Asia
24. Oral Health Neglect — dental/oral disease trials
25. Reproductive Health & Contraception — family planning intervention trials
26. NCD vs Communicable Balance — NCD transition, are trials keeping pace?
27. Rare Disease Orphan Gap — rare disease trials in low-resource settings
28. Traditional Medicine Trials — Ayurveda, Unani, Siddha evidence base
29. Vaccine Trial Pipeline — COVID, typhoid, cholera vaccine trials
30. Palliative Care Evidence — end-of-life trials in South Asia
31. Adolescent Health Gap — youth-specific trials (10-19 age group)
32. Geriatric Trial Exclusion — elderly population trials as demographics shift
33. Occupational Health — textile, mining, agriculture worker trials
34. Burn & Trauma Trials — high burn burden, acid attacks, road injuries
35. Disease Burden Concordance Index — overall: what's studied vs what kills (composite)

### Group 3 — Governance, Justice & Sovereignty (35 papers)

1. Foreign Sponsor Dominance — % trials sponsored by non-SAARC entities
2. Pharma vs Academic Split — industry vs investigator-initiated ratio
3. Data Sovereignty Gap — who owns South Asian trial data?
4. Post-Trial Access Commitments — continued drug access after trial ends
5. Informed Consent Language — trials conducted in local vs colonial languages
6. Ethics Committee Capacity — number/quality of IRBs across SAARC
7. Participant Compensation Equity — payment standards across the region
8. Gender in PI Leadership — female principal investigators, rates & trends
9. Regulatory Harmonization — DRAP (Pakistan), CDSCO (India), DGDA (Bangladesh) comparison
10. Results Reporting Compliance — % trials posting results on CT.gov
11. Publication Bias Signal — published vs unpublished trial results
12. CRO Outsourcing Patterns — contract research organization involvement
13. Colonial Research Legacy — historical sponsor-country patterns
14. South-South Collaboration — intra-SAARC research partnerships
15. WHO Essential Medicines Trials — trials for WHO EML drugs
16. Intellectual Property Barriers — patent landscape vs generic access
17. Community Engagement Models — participatory vs extractive trial designs
18. Vulnerable Population Protections — prisoner, refugee, pediatric safeguards
19. Trial Registration Timeliness — prospective vs retrospective registration
20. Funding Transparency — declared vs undeclared funding sources
21. Benefit-Sharing Agreements — post-trial benefit commitments
22. DRAP Approval Efficiency — Pakistan regulatory timeline analysis
23. Multi-National Power Asymmetry — decision-making in multi-country trials
24. Local Capacity Building — training/infrastructure legacy of trials
25. Paediatric Trial Ethics — child enrollment practices and safeguards
26. Placebo Use Appropriateness — active comparator vs placebo when treatment exists
27. Trial Waste Index — trials never completed, never published
28. Open Access Results Sharing — accessibility of trial findings
29. Refugee & Displaced Population Trials — Afghan refugees in Pakistan, Rohingya in Bangladesh
30. Religious & Cultural Consent Factors — faith-sensitive trial design
31. Government-Funded vs External — domestic research council investment
32. Academic Medical Center Gatekeeping — elite institution monopoly on trials
33. Whistleblower & Misconduct Reports — retraction/fraud signals in region
34. LMIC Authorship Position — first/last author from SAARC vs foreign
35. Sovereignty Composite Score — overall research independence index

### Group 4 — Methods, Design & Research Systems (35 papers)

1. Phase Distribution Analysis — phase I/II/III/IV balance across SAARC
2. Randomization Quality Audit — blinding & allocation concealment reporting
3. Sample Size Adequacy — powered vs underpowered trials
4. Primary Endpoint Selection — hard vs surrogate endpoints
5. Completion Rate Analysis — started vs completed trials by country
6. Time-to-Completion Trends — trial duration patterns
7. Adaptive Design Adoption — basket, platform, MAMS trial uptake
8. Pragmatic vs Explanatory — real-world vs tightly controlled designs
9. Biostatistical Method Quality — analysis plans and statistical rigor
10. Protocol Amendment Frequency — mid-trial protocol changes
11. Recruitment Rate Analysis — enrollment velocity across sites
12. Dropout & Attrition Patterns — loss-to-follow-up rates
13. Multi-Arm Trial Efficiency — 2-arm vs multi-arm designs
14. Non-Inferiority Trial Usage — NI margin appropriateness
15. Cluster RCT Patterns — community-level randomization
16. Interim Analysis Reporting — DSMB usage and stopping rules
17. Composite Endpoint Prevalence — single vs composite primary outcomes
18. Patient-Reported Outcome Use — PRO inclusion rates
19. Biomarker-Driven Trial Design — precision medicine approach
20. Bayesian Design Adoption — Bayesian vs frequentist frameworks
21. Registry Data Quality — missing fields, inconsistencies
22. Cross-Over Design Usage — when and how crossover trials are used
23. Equivalence Trial Standards — bioequivalence and generic drug trials
24. Outcome Reporting Bias — primary vs secondary outcome switching
25. Subgroup Analysis Practices — pre-specified vs post-hoc subgroups
26. Follow-Up Duration Adequacy — short vs long-term outcome measurement
27. Real-World Evidence Integration — observational + RCT hybrid designs
28. Digital Health Trial Methods — mHealth, telemedicine, app-based interventions
29. Pilot & Feasibility Studies — proportion of trials that are pilot/feasibility
30. Systematic Review Coverage — how many SAARC trials feed into Cochrane reviews
31. Benford's Law Enrollment Audit — first-digit distribution of enrollment numbers
32. PCA of Trial Characteristics — principal drivers of trial variation
33. Network Analysis of Investigators — PI collaboration networks
34. Machine-Readable Protocol Quality — structured data completeness
35. Methodological Rigor Composite — unified quality score across all dimensions

### Group 5 — Pakistan Deep-Dive (50 papers)

**Provincial Inequity (10)**

1. Punjab Trial Dominance — Lahore concentration
2. Sindh & Karachi Landscape — urban megacity vs rural Sindh
3. KPK & Tribal Areas — conflict-affected research capacity
4. Balochistan Research Desert — lowest trial density province
5. Islamabad Capital Advantage — federal institutions concentration
6. Gilgit-Baltistan & AJK — remote territory trial access
7. Provincial Per-Capita Trial Inequality — population-adjusted comparison
8. Provincial Health Budget vs Trial Density — spending correlation
9. Urban-Rural Punjab Disparity — Lahore/Faisalabad vs rural Punjab
10. Inter-Provincial Trend Analysis — convergence or divergence over time

**Institutional Concentration (8)**

11. Aga Khan University Hospital — premier research institution profile
12. Ziauddin University — home institution trial portfolio
13. Military Hospital Network — CMH/MH/AFIRI trial landscape
14. Shaukat Khanum Cancer Network — oncology trial concentration
15. Public Sector Teaching Hospitals — Jinnah, Mayo, Services, PIMS
16. Private vs Public Trial Divide — institutional capacity gap
17. Medical College Research Output — which colleges run trials?
18. Institutional Collaboration Networks — who works with whom?

**Disease-Specific Gaps (12)**

19. Cardiovascular Disease — Pakistan's #1 killer, trial response
20. Diabetes Tsunami — 33M+ diabetics, trial proportionality
21. Hepatitis C Epidemic — world's 2nd-highest prevalence, trial efforts
22. Hepatitis B Burden — vaccination gaps, treatment trials
23. Tuberculosis — MDR-TB hotspot, trial pipeline
24. Polio Eradication Last Mile — one of 2 endemic countries
25. Thalassemia Major — carrier rate 5-8%, treatment trial landscape
26. Dengue Outbreaks — Lahore/Karachi epidemics, prevention trials
27. Maternal & Neonatal Health — MMR and NMR crisis, intervention trials
28. Mental Health Chasm — <500 psychiatrists for 220M, trial scarcity
29. Childhood Pneumonia & Diarrhoea — top paediatric killers
30. Oral Cancer & Naswar/Gutka — uniquely high oral cancer burden

**Sponsor & Sovereignty (8)**

31. Foreign Sponsor Map — who funds Pakistan's trials?
32. DRAP Regulatory Timeline — approval speed analysis
33. Pharma Industry Presence — multinational vs local pharma
34. Academic vs Industry Ratio — investigator-initiated research capacity
35. Data Repatriation — does data stay in Pakistan?
36. Post-Trial Drug Access — continued access commitments
37. Generic Drug Trial Pipeline — bioequivalence study landscape
38. HEC Research Funding — Higher Education Commission investment

**Workforce & Methods (7)**

39. PI Gender Distribution — female investigators in Pakistan
40. Trial Completion Rate — Pakistan vs SAARC average
41. Registration Quality Audit — data completeness on CT.gov
42. Phase Distribution — Pakistan's phase I/II/III/IV balance
43. Endpoint Appropriateness — hard vs surrogate outcomes
44. Sample Size Trends — are trials getting better powered?
45. Statistical Methods Reporting — analysis plan transparency

**Karachi Lens (5)**

46. Karachi Trial Density Map — site distribution across the city
47. Karachi Disease Burden Match — trials vs city health priorities
48. Ziauddin vs Aga Khan vs Dow — Karachi institutional comparison
49. Karachi's Global Trial Share — megacity benchmarking
50. Karachi Recruitment Velocity — enrollment speed analysis

## 5. Repository Structure

```
C:\saarc-e156-students\
├── index.html                              # Landing page — 5 group cards
├── build.py                                # Master orchestrator
├── generate_dashboards.py                  # Dashboard HTML/SVG generation
├── rewrite_all_papers.py                   # E156 body generator
├── analysis/
│   ├── fetch_saarc_rcts_by_country.py      # Country-level aggregation (8 nations)
│   ├── statistical_deep_dive.py            # 10+ methods across all data
│   ├── saarc_rct_country_dashboard.html    # Comparative overview dashboard
│   └── *.json                              # Cached API results
├── geographic-equity/                      # Group 1 (35 papers)
│   ├── index.html
│   ├── dashboards/                         # 35 HTML dashboards
│   └── code/                               # 35 Python analysis scripts
├── health-disease/                         # Group 2 (35 papers)
│   ├── index.html
│   ├── dashboards/
│   └── code/
├── governance-justice/                     # Group 3 (35 papers)
│   ├── index.html
│   ├── dashboards/
│   └── code/
├── methods-systems/                        # Group 4 (35 papers)
│   ├── index.html
│   ├── dashboards/
│   └── code/
├── pakistan-deep-dive/                      # Group 5 (50 papers)
│   ├── index.html
│   ├── dashboards/
│   └── code/
├── lib/                                    # Shared libraries
│   ├── data_fetcher.py                     # CT.gov API wrapper + JSON caching
│   ├── dashboard_generator.py              # HTML/SVG template engine
│   ├── chart_library.py                    # 15+ SVG chart types
│   ├── code_generator.py                   # Python script templating
│   ├── body_generator.py                   # E156 text generation
│   ├── stats_library.py                    # 31+ statistical methods
│   ├── index_updater.py                    # Group index maintenance
│   └── paper_manifest.py                   # All 190 topic definitions
├── data_cache/                             # JSON caches (minimize API calls)
├── docs/
│   └── superpowers/
│       └── specs/
│           └── 2026-04-08-saarc-e156-students-design.md
└── E156-PROTOCOL.md                        # Timestamped E156 protocol
```

## 6. Technical Architecture

### Dashboard Design
- Single self-contained HTML per paper, NYT editorial style (Georgia serif)
- 8 unique SVG charts per dashboard (no duplicates across dashboards)
- Hero metrics card, key findings, sentence-by-sentence color-coded breakdown
- Sentence color coding: S1 blue, S2 green, S3 purple, S4 red, S5 orange, S6 teal, S7 gray
- Responsive, mobile-friendly, fully offline (no CDN dependencies)
- Open Graph meta tags for link previews

### Regional Maps
- **SAARC map**: SVG map of South Asia with 8 nations color-coded (choropleth)
- **Pakistan map**: Provincial-level SVG choropleth (Punjab, Sindh, KPK, Balochistan, ICT, GB, AJK) for Group 5 papers

### Statistical Library (31+ methods)
- Lorenz curve, Gini coefficient, HHI, Moran's I
- Bootstrap CI, permutation tests
- Bayesian rate estimation
- Time-series decomposition
- Network analysis (centrality, modularity)
- Poisson regression, logistic regression
- Theil index, Atkinson index
- Survival/hazard analysis
- PCA, Benford's law
- Disease burden concordance metrics
- All implemented in pure Python (no external stats libraries)

### Data Pipeline
1. **Fetch**: CT.gov API v2, query `query.locn=<country>` per SAARC nation
2. **Cache**: JSON in `data_cache/` — minimize API calls
3. **Analyze**: Per-paper Python script (5+ statistical methods each)
4. **Generate**: E156 body + HTML dashboard + downloadable .py
5. **Determinism**: `seed = hash(slug)` for reproducible sampling (xoshiro128**)

### Build Pipeline
```
python build.py --all
  ├── Fetches/caches CT.gov data for all 8 SAARC countries
  ├── Generates 190 E156 bodies via body_generator
  ├── Generates 190 HTML dashboards via dashboard_generator
  ├── Generates 190 Python scripts via code_generator
  ├── Builds 5 group index.html pages
  └── Builds landing index.html
```

### Chart Types Available (15+)
Choropleth maps (SAARC + Pakistan provincial), Lorenz curves, forest plots, violin plots, heatmaps, network graphs, time series, waterfall, Sankey flows, radar, bubble charts, slope graphs, ridge plots, funnel plots, Kaplan-Meier curves.

## 7. Student Workflow (Ziauddin Medical University)

### 7-Step Process

1. **Read** AI-drafted E156 paper
2. **Study** interactive HTML dashboard (8 SVG charts)
3. **Download** Python analysis code
4. **Rewrite** in own voice (AI draft is starting point, not final)
5. **Add 2-3 references** (PubMed, WHO, ClinicalTrials.gov)
6. **Include Outside Note Block** with dashboard link, code link, estimand, certainty
7. **Submit** to Synthesis Medicine Journal

### Outside Note Block Template

```
Type: [pairwise | methods | prevalence]
Primary estimand: [as per paper]
App: https://mahmood789.github.io/saarc-e156-students/{group}/dashboards/{slug}.html
Data: ClinicalTrials.gov API v2 (public)
Code: https://github.com/mahmood726-cyber/saarc-e156-students/tree/main/{group}/code/{slug}.py
Version: 1.0
Date: 2026-04-08
Certainty: [LOW | MODERATE]
```

### Warnings for Students
- Papers are AI-generated drafts requiring originality
- Reviewers will check for plagiarism
- Add own South Asian / Pakistani perspective
- Clearly label AI-assisted content

## 8. Deployment

- **GitHub repo**: `mahmood726-cyber/saarc-e156-students`
- **GitHub Pages**: `mahmood789.github.io/saarc-e156-students/`
- **Landing page**: 5 group cards with paper counts, Ziauddin branding
- **Group pages**: Instruction panel + paper cards with 3 buttons each (View Dashboard, Download Code, Download Paper)
- **Fully offline**: No external CDN dependencies
- **Open Graph meta tags** for link previews

## 9. Success Criteria

- [ ] All 190 E156 bodies generated (7 sentences, <=156 words each)
- [ ] All 190 HTML dashboards render correctly with 8 SVG charts each
- [ ] All 190 Python scripts run independently with `requests` only
- [ ] All 5 group index pages functional
- [ ] Landing page displays all 5 groups
- [ ] GitHub Pages deployed and all URLs accessible
- [ ] Mobile-responsive design
- [ ] Fully offline-capable (no CDN)
- [ ] Pakistan provincial map renders in Group 5 dashboards
- [ ] SAARC regional map renders in Groups 1-4 dashboards

## 10. Differences from Africa Project

| Aspect | Africa | SAARC |
|--------|--------|-------|
| Countries | 54 | 8 |
| Groups | 4 | 5 (added Pakistan Deep-Dive) |
| Papers | 190 | 190 |
| Distribution | 40/60/45/45 | 35/35/35/35/50 |
| Focal country | None (pan-African) | Pakistan |
| University | University of Uganda | Ziauddin Medical University |
| Regional map | Africa choropleth | South Asia choropleth |
| Sub-national map | None | Pakistan provincial choropleth |
| Unique themes | Conflict zones, landlocked, colonial legacy | CPEC, polio endgame, DRAP, provincial inequity, naswar/gutka |
