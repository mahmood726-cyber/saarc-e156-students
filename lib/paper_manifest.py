"""
Paper manifest for 190 SAARC clinical trial equity papers.
Each paper: slug, title, group, paper_num, query params, assigned stats, assigned charts, context, references.
"""

# ═══════════════════════════════════════════════════════════
#  SAARC CONSTANTS
# ═══════════════════════════════════════════════════════════

SAARC_COUNTRIES = [
    "India", "Pakistan", "Bangladesh", "Sri Lanka",
    "Nepal", "Afghanistan", "Bhutan", "Maldives"
]

PAKISTAN_PROVINCES = [
    "Punjab", "Sindh", "Khyber Pakhtunkhwa", "Balochistan",
    "Islamabad Capital Territory", "Gilgit-Baltistan", "Azad Jammu and Kashmir"
]

PAKISTAN_CITIES = {
    "Karachi": "Sindh",
    "Lahore": "Punjab",
    "Islamabad": "Islamabad Capital Territory",
    "Rawalpindi": "Punjab",
    "Faisalabad": "Punjab",
    "Peshawar": "Khyber Pakhtunkhwa",
    "Quetta": "Balochistan",
    "Multan": "Punjab",
    "Hyderabad": "Sindh",
    "Sialkot": "Punjab",
    "Abbottabad": "Khyber Pakhtunkhwa",
    "Bahawalpur": "Punjab",
    "Sukkur": "Sindh",
    "Gilgit": "Gilgit-Baltistan",
    "Muzaffarabad": "Azad Jammu and Kashmir",
}

PAKISTAN_INSTITUTIONS = [
    "Aga Khan University Hospital",
    "Ziauddin University",
    "Dow University of Health Sciences",
    "Shaukat Khanum Memorial Cancer Hospital",
    "Armed Forces Institute of Pathology",
    "Combined Military Hospital Rawalpindi",
    "National Institute of Cardiovascular Diseases",
    "Jinnah Postgraduate Medical Centre",
    "King Edward Medical University",
    "Allama Iqbal Medical College",
    "Services Hospital Lahore",
    "Pakistan Institute of Medical Sciences",
    "Shifa International Hospital",
    "Indus Hospital & Health Network",
    "Lady Reading Hospital Peshawar",
]

LANDLOCKED_SAARC = ["Nepal", "Bhutan", "Afghanistan"]
ISLAND_SAARC = ["Maldives", "Sri Lanka"]
CONFLICT_SAARC = ["Afghanistan", "Pakistan", "Sri Lanka"]

CHART_TYPES = [
    "choropleth", "lorenz", "forest", "violin", "heatmap",
    "network", "timeseries", "waterfall", "sankey", "radar",
    "bubble", "slope", "ridge", "funnel", "kaplan_meier",
    "choropleth_pakistan"
]

# Sentence role colors for dashboards
ROLE_COLORS = ["#1b4f72", "#0e6251", "#4a235a", "#922b21", "#7e5109", "#0b5345", "#566573"]

# ═══════════════════════════════════════════════════════════
#  GROUP DEFINITIONS
# ═══════════════════════════════════════════════════════════

GROUPS = {
    "geographic-equity": {
        "name": "Geographic Equity & Spatial Justice",
        "description": "Spatial distribution, access barriers, and geographic concentration of clinical trials across SAARC nations.",
        "paper_count": 35,
    },
    "health-disease": {
        "name": "Health & Disease Burden",
        "description": "Alignment between disease burden and clinical trial investment across SAARC's epidemiological landscape.",
        "paper_count": 35,
    },
    "governance-justice": {
        "name": "Governance, Justice & Sovereignty",
        "description": "Ethical oversight, sponsor dynamics, regulatory capacity, and research sovereignty in South Asia.",
        "paper_count": 35,
    },
    "methods-systems": {
        "name": "Methods, Design & Research Systems",
        "description": "Trial design quality, methodological rigor, and research infrastructure across SAARC.",
        "paper_count": 35,
    },
    "pakistan-deep-dive": {
        "name": "Pakistan Deep-Dive",
        "description": "Provincial inequity, institutional concentration, disease-specific gaps, and workforce analysis within Pakistan.",
        "paper_count": 50,
    },
}

# ═══════════════════════════════════════════════════════════
#  STANDARD REFERENCES
# ═══════════════════════════════════════════════════════════

REF_CTGOV = 'ClinicalTrials.gov API v2 Documentation. U.S. National Library of Medicine. https://clinicaltrials.gov/data-api/about-api'
REF_WHO = 'World Health Organization. "WHO South-East Asia Region: Health Topics." https://www.who.int/southeastasia'
REF_GBD = 'GBD 2021 Collaborators. "Global burden of disease study 2021." Lancet. 2024.'
REF_DRAIN = 'Drain PK, et al. "Global migration of clinical trials." Nat Rev Drug Discov. 2018;17:765-766.'
REF_LANG = 'Lang T, Siribaddana S. "Clinical trials have gone global: is this a good thing?" PLoS Med. 2012;9:e1001228.'
REF_CHAN = 'Chan AW, et al. "SPIRIT 2013 statement." Ann Intern Med. 2013;158:200-207.'
REF_HEDT = 'Hedt-Gauthier BL, et al. "Stuck in the middle: authorship in collaborative health research." BMJ Glob Health. 2019;4:e001853.'
REF_SINGH = 'Singh JA. "India, Sri Lanka and clinical trials." Indian J Med Ethics. 2018;3:221-228.'
REF_DRAP = 'Drug Regulatory Authority of Pakistan. "DRAP Annual Report." Islamabad, 2024.'
REF_HEC = 'Higher Education Commission Pakistan. "R&D Statistics." Islamabad, 2024.'


def _charts(indices):
    """Select 8 chart types by index from CHART_TYPES."""
    return [CHART_TYPES[i % len(CHART_TYPES)] for i in indices]


# ═══════════════════════════════════════════════════════════
#  GROUP 1: GEOGRAPHIC EQUITY & SPATIAL JUSTICE (35 papers)
# ═══════════════════════════════════════════════════════════
GEO_PAPERS = [
    {
        "slug": "saarc-trial-density-map", "title": "SAARC Trial Density Map",
        "group": "geographic-equity", "paper_num": 1,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["gini_coefficient", "bootstrap_ci", "poisson_rate", "shannon_entropy", "theil_index"],
        "charts": _charts([0, 1, 3, 4, 6, 7, 9, 10]),
        "context": "SAARC nations collectively host over 1.9 billion people but clinical trial density varies by orders of magnitude, from India's thousands to Bhutan's near-zero registrations.",
        "refs": [REF_CTGOV, REF_WHO, REF_DRAIN]
    },
    {
        "slug": "india-dominance-index", "title": "India Dominance Index",
        "group": "geographic-equity", "paper_num": 2,
        "query": {"condition": None, "countries": ["India"]},
        "stats": ["hhi_index", "gini_coefficient", "bootstrap_ci", "concentration_index", "lorenz_area"],
        "charts": _charts([0, 1, 2, 7, 6, 9, 3, 11]),
        "context": "India hosts over 90% of SAARC clinical trials, creating a regional research monoculture where evidence generated in Indian populations is extrapolated to seven other nations with distinct genetic, dietary, and environmental profiles.",
        "refs": [REF_CTGOV, REF_SINGH, REF_DRAIN]
    },
    {
        "slug": "pakistan-per-capita-deficit", "title": "Pakistan Per-Capita Deficit",
        "group": "geographic-equity", "paper_num": 3,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["rate_ratio", "bootstrap_ci", "poisson_rate", "bayesian_rate", "concentration_index"],
        "charts": _charts([0, 2, 3, 6, 7, 9, 11, 13]),
        "context": "Pakistan's 230 million people make it the fifth most populous nation, yet its per-capita clinical trial rate is a fraction of India's, reflecting chronic underinvestment in research infrastructure.",
        "refs": [REF_CTGOV, REF_DRAP, REF_DRAIN]
    },
    {
        "slug": "bangladesh-growth-trajectory", "title": "Bangladesh Growth Trajectory",
        "group": "geographic-equity", "paper_num": 4,
        "query": {"condition": None, "countries": ["Bangladesh"]},
        "stats": ["linear_regression", "bootstrap_ci", "poisson_rate", "bayesian_rate", "spearman_correlation"],
        "charts": _charts([6, 0, 2, 10, 7, 9, 3, 11]),
        "context": "Bangladesh's clinical trial portfolio has grown steadily, driven by icddr,b and BRAC health networks, but the trajectory remains insufficient relative to its 170 million population and disease burden.",
        "refs": [REF_CTGOV, REF_WHO, REF_DRAIN]
    },
    {
        "slug": "sri-lanka-punch-above-weight", "title": "Sri Lanka Punch-Above-Weight",
        "group": "geographic-equity", "paper_num": 5,
        "query": {"condition": None, "countries": ["Sri Lanka"]},
        "stats": ["rate_ratio", "bootstrap_ci", "poisson_rate", "bayesian_rate", "permutation_test"],
        "charts": _charts([0, 2, 6, 3, 7, 9, 10, 14]),
        "context": "Sri Lanka's universal healthcare system and high literacy rate create a research-ready population that punches above its demographic weight in clinical trial participation.",
        "refs": [REF_CTGOV, REF_SINGH, REF_LANG]
    },
    {
        "slug": "nepal-mountain-access-barrier", "title": "Nepal Mountain Access Barrier",
        "group": "geographic-equity", "paper_num": 6,
        "query": {"condition": None, "countries": ["Nepal"]},
        "stats": ["morans_i", "bootstrap_ci", "poisson_rate", "gini_coefficient", "lorenz_area"],
        "charts": _charts([0, 1, 3, 6, 7, 9, 12, 14]),
        "context": "Nepal's Himalayan geography creates vertical health disparities where trial sites concentrate in the Kathmandu Valley while highland communities remain entirely excluded from clinical research.",
        "refs": [REF_CTGOV, REF_WHO, REF_GBD]
    },
    {
        "slug": "afghanistan-conflict-zone-trials", "title": "Afghanistan Conflict Zone Trials",
        "group": "geographic-equity", "paper_num": 7,
        "query": {"condition": None, "countries": ["Afghanistan"]},
        "stats": ["poisson_rate", "bootstrap_ci", "bayesian_rate", "rate_ratio", "permutation_test"],
        "charts": _charts([0, 2, 6, 7, 3, 9, 14, 13]),
        "context": "Decades of conflict have devastated Afghanistan's research infrastructure, leaving a nation of 40 million with fewer clinical trials than many individual hospitals in India.",
        "refs": [REF_CTGOV, REF_WHO, REF_GBD]
    },
    {
        "slug": "bhutan-micro-state-research", "title": "Bhutan Micro-State Research",
        "group": "geographic-equity", "paper_num": 8,
        "query": {"condition": None, "countries": ["Bhutan"]},
        "stats": ["poisson_rate", "bayesian_rate", "bootstrap_ci", "rate_ratio", "shannon_entropy"],
        "charts": _charts([0, 2, 3, 6, 7, 9, 10, 14]),
        "context": "Bhutan's population of 780,000 makes conventional clinical trial design challenging, but its universal healthcare system and centralized health data present unique opportunities for pragmatic research.",
        "refs": [REF_CTGOV, REF_WHO]
    },
    {
        "slug": "maldives-island-isolation", "title": "Maldives Island Isolation",
        "group": "geographic-equity", "paper_num": 9,
        "query": {"condition": None, "countries": ["Maldives"]},
        "stats": ["poisson_rate", "bayesian_rate", "bootstrap_ci", "permutation_test", "rate_ratio"],
        "charts": _charts([0, 2, 6, 3, 7, 9, 14, 10]),
        "context": "The Maldives' 1,200 islands spread across 90,000 square kilometers of ocean create logistical impossibilities for multi-site trials, making it the most geographically fragmented SAARC nation.",
        "refs": [REF_CTGOV, REF_WHO]
    },
    {
        "slug": "capital-city-monopoly-index", "title": "Capital City Monopoly Index",
        "group": "geographic-equity", "paper_num": 10,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["hhi_index", "gini_coefficient", "atkinson_index", "bootstrap_ci", "lorenz_area"],
        "charts": _charts([0, 1, 7, 3, 9, 4, 11, 6]),
        "context": "Capital cities monopolize SAARC clinical trial infrastructure because they host major teaching hospitals, have reliable electricity and internet, and offer transport links that sponsors require for monitoring.",
        "refs": [REF_CTGOV, REF_DRAIN]
    },
    {
        "slug": "cross-border-trial-networks", "title": "Cross-Border Trial Networks",
        "group": "geographic-equity", "paper_num": 11,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["network_centrality", "bootstrap_ci", "shannon_entropy", "hhi_index", "spearman_correlation"],
        "charts": _charts([5, 0, 4, 8, 6, 9, 7, 3]),
        "context": "Cross-border trial networks in SAARC are rare despite shared languages, diseases, and genetic backgrounds, reflecting political tensions that fragment what should be a collaborative research space.",
        "refs": [REF_DRAIN, REF_LANG, REF_CTGOV]
    },
    {
        "slug": "urban-rural-site-distribution", "title": "Urban-Rural Site Distribution",
        "group": "geographic-equity", "paper_num": 12,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["gini_coefficient", "lorenz_area", "bootstrap_ci", "chi_squared", "rate_ratio"],
        "charts": _charts([0, 1, 3, 7, 6, 9, 12, 10]),
        "context": "Over 65% of South Asians live in rural areas, yet trial sites cluster exclusively in urban centers, creating an evidence base derived from populations that differ systematically from the rural majority.",
        "refs": [REF_CTGOV, REF_WHO, REF_GBD]
    },
    {
        "slug": "spatial-gini-coefficient", "title": "Spatial Gini Coefficient",
        "group": "geographic-equity", "paper_num": 13,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["gini_coefficient", "bootstrap_ci", "lorenz_area", "theil_index", "atkinson_index"],
        "charts": _charts([1, 0, 3, 7, 4, 9, 6, 11]),
        "context": "The spatial Gini coefficient for SAARC trial distribution exceeds 0.9, indicating near-total concentration — a level of inequality that would be considered extreme in any economic context.",
        "refs": [REF_CTGOV, REF_DRAIN]
    },
    {
        "slug": "herfindahl-site-concentration", "title": "Herfindahl Site Concentration",
        "group": "geographic-equity", "paper_num": 14,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["hhi_index", "bootstrap_ci", "gini_coefficient", "concentration_index", "shannon_entropy"],
        "charts": _charts([4, 0, 1, 7, 9, 3, 6, 11]),
        "context": "The Herfindahl-Hirschman Index for trial site concentration across SAARC reveals monopolistic patterns that would trigger antitrust scrutiny in commercial markets.",
        "refs": [REF_CTGOV, REF_DRAIN]
    },
    {
        "slug": "regional-clustering-patterns", "title": "Regional Clustering Patterns",
        "group": "geographic-equity", "paper_num": 15,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["morans_i", "bootstrap_ci", "network_centrality", "hhi_index", "shannon_entropy"],
        "charts": _charts([0, 5, 4, 7, 6, 9, 3, 10]),
        "context": "Spatial clustering analysis reveals that SAARC trials form distinct geographic clusters around major medical centers, with vast intervening territories that are research deserts.",
        "refs": [REF_CTGOV, REF_WHO]
    },
    {
        "slug": "coastal-vs-interior-disparity", "title": "Coastal vs Interior Disparity",
        "group": "geographic-equity", "paper_num": 16,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["chi_squared", "rate_ratio", "bootstrap_ci", "odds_ratio", "permutation_test"],
        "charts": _charts([0, 2, 3, 7, 6, 9, 11, 10]),
        "context": "Coastal cities like Mumbai, Karachi, and Colombo dominate trial infrastructure due to port logistics, international connectivity, and colonial-era investment patterns that persist today.",
        "refs": [REF_CTGOV, REF_DRAIN]
    },
    {
        "slug": "population-weighted-trial-gap", "title": "Population-Weighted Trial Gap",
        "group": "geographic-equity", "paper_num": 17,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["rate_ratio", "bootstrap_ci", "poisson_rate", "spearman_correlation", "linear_regression"],
        "charts": _charts([10, 0, 1, 6, 7, 9, 3, 11]),
        "context": "When trials are weighted by population, Pakistan's 230 million people face the largest absolute research deficit in SAARC, followed by Bangladesh's 170 million.",
        "refs": [REF_CTGOV, REF_WHO, REF_GBD]
    },
    {
        "slug": "border-region-research-deserts", "title": "Border Region Research Deserts",
        "group": "geographic-equity", "paper_num": 18,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["morans_i", "poisson_rate", "bootstrap_ci", "bayesian_rate", "gini_coefficient"],
        "charts": _charts([0, 3, 4, 6, 7, 9, 12, 14]),
        "context": "Border regions between SAARC nations are doubly disadvantaged — too remote for national research networks and politically sensitive for cross-border collaboration — creating some of the world's largest research deserts.",
        "refs": [REF_CTGOV, REF_WHO]
    },
    {
        "slug": "megacity-trial-absorption", "title": "Megacity Trial Absorption",
        "group": "geographic-equity", "paper_num": 19,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["hhi_index", "concentration_index", "bootstrap_ci", "gini_coefficient", "poisson_rate"],
        "charts": _charts([0, 1, 7, 3, 4, 9, 6, 10]),
        "context": "Megacities like Delhi, Mumbai, Dhaka, and Karachi absorb the vast majority of their nation's trials, creating urban research enclaves that bear little resemblance to the populations they claim to serve.",
        "refs": [REF_CTGOV, REF_DRAIN]
    },
    {
        "slug": "second-tier-city-emergence", "title": "Second-Tier City Emergence",
        "group": "geographic-equity", "paper_num": 20,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["linear_regression", "bootstrap_ci", "poisson_rate", "bayesian_rate", "spearman_correlation"],
        "charts": _charts([6, 0, 7, 11, 3, 9, 10, 2]),
        "context": "Second-tier cities like Pune, Chandigarh, Faisalabad, and Chittagong are beginning to emerge as trial sites, driven by growing university hospital capacity and CRO expansion beyond capital cities.",
        "refs": [REF_CTGOV, REF_DRAIN]
    },
    {
        "slug": "rural-reach-coefficient", "title": "Rural Reach Coefficient",
        "group": "geographic-equity", "paper_num": 21,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["gini_coefficient", "lorenz_area", "bootstrap_ci", "rate_ratio", "poisson_rate"],
        "charts": _charts([1, 0, 3, 7, 6, 9, 12, 10]),
        "context": "The rural reach coefficient measures the fraction of trials conducted outside major urban centers, revealing that less than 5% of SAARC trials reach the rural communities where the majority of people live.",
        "refs": [REF_CTGOV, REF_WHO]
    },
    {
        "slug": "site-fragmentation-index", "title": "Site Fragmentation Index",
        "group": "geographic-equity", "paper_num": 22,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["shannon_entropy", "hhi_index", "bootstrap_ci", "gini_coefficient", "theil_index"],
        "charts": _charts([4, 0, 1, 7, 3, 9, 6, 12]),
        "context": "Trial site fragmentation across SAARC reveals a paradox: India has many sites but they cluster in a few cities, while smaller nations have too few sites to even measure fragmentation.",
        "refs": [REF_CTGOV, REF_DRAIN]
    },
    {
        "slug": "landlocked-penalty-nepal-bhutan", "title": "Landlocked Penalty (Nepal/Bhutan)",
        "group": "geographic-equity", "paper_num": 23,
        "query": {"condition": None, "countries": LANDLOCKED_SAARC},
        "stats": ["rate_ratio", "bootstrap_ci", "poisson_rate", "permutation_test", "bayesian_rate"],
        "charts": _charts([0, 2, 3, 6, 7, 9, 11, 14]),
        "context": "Landlocked SAARC nations face compounded research access barriers — no port infrastructure for temperature-sensitive biologics, higher import costs for trial supplies, and limited international connectivity.",
        "refs": [REF_CTGOV, REF_DRAIN, REF_WHO]
    },
    {
        "slug": "monsoon-belt-trial-seasonality", "title": "Monsoon Belt Trial Seasonality",
        "group": "geographic-equity", "paper_num": 24,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["chi_squared", "permutation_test", "bootstrap_ci", "poisson_rate", "spearman_correlation"],
        "charts": _charts([6, 0, 3, 12, 7, 9, 4, 10]),
        "context": "The South Asian monsoon disrupts trial operations for 3-4 months annually through flooding, transport paralysis, and vector-borne disease surges that confound endpoint assessment.",
        "refs": [REF_CTGOV, REF_WHO]
    },
    {
        "slug": "economic-corridor-alignment", "title": "Economic Corridor Alignment",
        "group": "geographic-equity", "paper_num": 25,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["spearman_correlation", "linear_regression", "bootstrap_ci", "rate_ratio", "gini_coefficient"],
        "charts": _charts([0, 10, 1, 6, 7, 9, 3, 8]),
        "context": "CPEC, the Golden Quadrilateral, and other economic corridors shape trial site geography by determining where infrastructure, hospitals, and transport networks concentrate.",
        "refs": [REF_CTGOV, REF_DRAIN]
    },
    {
        "slug": "conflict-stability-trial-gradient", "title": "Conflict-Stability Trial Gradient",
        "group": "geographic-equity", "paper_num": 26,
        "query": {"condition": None, "countries": CONFLICT_SAARC},
        "stats": ["linear_regression", "bootstrap_ci", "poisson_rate", "rate_ratio", "bayesian_rate"],
        "charts": _charts([0, 6, 2, 7, 3, 9, 14, 11]),
        "context": "A clear gradient exists from stable SAARC nations (Sri Lanka, Bhutan) to conflict-affected ones (Afghanistan), with trial density tracking security conditions rather than health need.",
        "refs": [REF_CTGOV, REF_GBD, REF_WHO]
    },
    {
        "slug": "diaspora-return-research", "title": "Diaspora Return Research",
        "group": "geographic-equity", "paper_num": 27,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["network_centrality", "bootstrap_ci", "rate_ratio", "spearman_correlation", "poisson_rate"],
        "charts": _charts([5, 0, 6, 7, 3, 9, 8, 10]),
        "context": "South Asian diaspora researchers in the US, UK, and Gulf states increasingly serve as bridge figures connecting SAARC trial sites with global networks, but their role can perpetuate dependency.",
        "refs": [REF_DRAIN, REF_HEDT, REF_CTGOV]
    },
    {
        "slug": "sez-medical-tourism-sites", "title": "SEZ & Medical Tourism Sites",
        "group": "geographic-equity", "paper_num": 28,
        "query": {"condition": None, "countries": ["India", "Sri Lanka"]},
        "stats": ["rate_ratio", "bootstrap_ci", "chi_squared", "poisson_rate", "odds_ratio"],
        "charts": _charts([0, 2, 7, 6, 3, 9, 10, 11]),
        "context": "Special economic zones and medical tourism hubs in India and Sri Lanka attract clinical trials through tax incentives and world-class hospital infrastructure, further concentrating research in privileged enclaves.",
        "refs": [REF_CTGOV, REF_SINGH]
    },
    {
        "slug": "regional-health-expenditure-match", "title": "Regional Health Expenditure Match",
        "group": "geographic-equity", "paper_num": 29,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["spearman_correlation", "linear_regression", "bootstrap_ci", "rate_ratio", "gini_coefficient"],
        "charts": _charts([10, 0, 1, 6, 7, 9, 3, 11]),
        "context": "Health expenditure per capita ranges from $12 in Afghanistan to $200+ in Maldives, and trial density tracks spending rather than disease burden, creating a wealth-research feedback loop.",
        "refs": [REF_CTGOV, REF_WHO, REF_GBD]
    },
    {
        "slug": "altitude-access-barriers", "title": "Altitude & Access Barriers",
        "group": "geographic-equity", "paper_num": 30,
        "query": {"condition": None, "countries": ["Nepal", "Bhutan", "Pakistan"]},
        "stats": ["morans_i", "bootstrap_ci", "poisson_rate", "rate_ratio", "gini_coefficient"],
        "charts": _charts([0, 3, 4, 6, 7, 9, 12, 14]),
        "context": "High-altitude populations across the Himalayas, Karakoram, and Hindu Kush have unique health profiles — altitude sickness, UV exposure, cold-related illness — yet are entirely absent from clinical trial enrollment.",
        "refs": [REF_CTGOV, REF_WHO]
    },
    {
        "slug": "delta-floodplain-populations", "title": "Delta & Floodplain Populations",
        "group": "geographic-equity", "paper_num": 31,
        "query": {"condition": None, "countries": ["Bangladesh", "India"]},
        "stats": ["poisson_rate", "bootstrap_ci", "rate_ratio", "bayesian_rate", "chi_squared"],
        "charts": _charts([0, 2, 3, 6, 7, 9, 12, 10]),
        "context": "The Ganges-Brahmaputra-Meghna delta hosts 150 million people facing unique health challenges from flooding, arsenic contamination, and climate displacement, yet has minimal trial presence.",
        "refs": [REF_CTGOV, REF_WHO, REF_GBD]
    },
    {
        "slug": "spatial-entropy-index", "title": "Spatial Entropy Index",
        "group": "geographic-equity", "paper_num": 32,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["shannon_entropy", "bootstrap_ci", "kl_divergence", "theil_index", "gini_coefficient"],
        "charts": _charts([4, 0, 1, 7, 3, 9, 6, 12]),
        "context": "Shannon entropy applied to trial site distribution reveals extremely low spatial randomness — trial placement is driven by institutional convenience rather than population health need.",
        "refs": [REF_CTGOV, REF_DRAIN]
    },
    {
        "slug": "distance-to-trial-burden", "title": "Distance-to-Trial Burden",
        "group": "geographic-equity", "paper_num": 33,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["gini_coefficient", "linear_regression", "bootstrap_ci", "lorenz_area", "spearman_correlation"],
        "charts": _charts([0, 1, 10, 6, 9, 3, 7, 12]),
        "context": "For the average rural South Asian, the nearest clinical trial site may be hundreds of kilometers away — a distance measured not in hours but in days of travel across congested roads and seasonal floodwaters.",
        "refs": [REF_CTGOV, REF_WHO, REF_GBD]
    },
    {
        "slug": "intra-saarc-disparity-ratio", "title": "Intra-SAARC Disparity Ratio",
        "group": "geographic-equity", "paper_num": 34,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["theil_index", "atkinson_index", "bootstrap_ci", "gini_coefficient", "rate_ratio"],
        "charts": _charts([7, 0, 1, 4, 6, 9, 3, 11]),
        "context": "The ratio of India's per-capita trial rate to Afghanistan's exceeds 100:1, making intra-SAARC disparity among the highest of any regional bloc and rivalling intercontinental inequalities.",
        "refs": [REF_CTGOV, REF_DRAIN, REF_GBD]
    },
    {
        "slug": "geographic-equity-trend", "title": "Geographic Equity Trend",
        "group": "geographic-equity", "paper_num": 35,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["linear_regression", "bootstrap_ci", "spearman_correlation", "gini_coefficient", "theil_index"],
        "charts": _charts([6, 0, 1, 11, 7, 9, 3, 10]),
        "context": "Longitudinal analysis of geographic equity across SAARC reveals whether the trial distribution is becoming more equitable over time or whether concentration in India continues to intensify.",
        "refs": [REF_CTGOV, REF_WHO, REF_DRAIN]
    },
]

# ═══════════════════════════════════════════════════════════
#  GROUP 2: HEALTH & DISEASE BURDEN (35 papers)
# ═══════════════════════════════════════════════════════════
HEALTH_PAPERS = [
    {
        "slug": "cardiovascular-trial-gap", "title": "Cardiovascular Trial Gap",
        "group": "health-disease", "paper_num": 1,
        "query": {"condition": "Cardiovascular Diseases", "countries": SAARC_COUNTRIES},
        "stats": ["rate_ratio", "bootstrap_ci", "poisson_rate", "lorenz_area", "gini_coefficient"],
        "charts": _charts([0, 1, 2, 6, 7, 9, 3, 11]),
        "context": "South Asia has the world's highest cardiovascular mortality rate, with events occurring a decade earlier than in Europe, yet CV trial investment is a fraction of what the epidemic demands.",
        "refs": [REF_GBD, REF_CTGOV, REF_WHO]
    },
    {
        "slug": "diabetes-epidemic-mismatch", "title": "Diabetes Epidemic Mismatch",
        "group": "health-disease", "paper_num": 2,
        "query": {"condition": "Diabetes", "countries": SAARC_COUNTRIES},
        "stats": ["linear_regression", "bootstrap_ci", "poisson_rate", "rate_ratio", "spearman_correlation"],
        "charts": _charts([10, 1, 0, 6, 7, 9, 3, 2]),
        "context": "South Asians develop diabetes at lower BMIs and younger ages than Europeans, yet the evidence base for treatment is derived from Western populations with fundamentally different metabolic profiles.",
        "refs": [REF_GBD, REF_CTGOV, REF_WHO]
    },
    {
        "slug": "tb-trial-landscape", "title": "TB Trial Landscape",
        "group": "health-disease", "paper_num": 3,
        "query": {"condition": "Tuberculosis", "countries": SAARC_COUNTRIES},
        "stats": ["bayesian_rate", "rate_ratio", "bootstrap_ci", "chi_squared", "poisson_rate"],
        "charts": _charts([2, 0, 3, 6, 7, 9, 4, 14]),
        "context": "SAARC nations carry one-third of the global TB burden, with India, Pakistan, and Bangladesh among the top 8 high-burden countries, yet the drug-resistant TB pipeline remains critically thin.",
        "refs": [REF_GBD, REF_CTGOV, REF_WHO]
    },
    {
        "slug": "hepatitis-bc-hotspot", "title": "Hepatitis B/C Hotspot",
        "group": "health-disease", "paper_num": 4,
        "query": {"condition": "Hepatitis B OR Hepatitis C", "countries": SAARC_COUNTRIES},
        "stats": ["rate_ratio", "bootstrap_ci", "poisson_rate", "lorenz_area", "bayesian_rate"],
        "charts": _charts([0, 1, 2, 6, 7, 9, 3, 14]),
        "context": "Pakistan alone has 12 million hepatitis C patients — the second highest prevalence globally — yet hepatitis trial investment in SAARC is dwarfed by efforts in Egypt and East Asia.",
        "refs": [REF_GBD, REF_CTGOV, REF_DRAP]
    },
    {
        "slug": "maternal-mortality-crisis", "title": "Maternal Mortality Crisis",
        "group": "health-disease", "paper_num": 5,
        "query": {"condition": "Maternal Health OR Preeclampsia OR Postpartum Hemorrhage", "countries": SAARC_COUNTRIES},
        "stats": ["rate_ratio", "lorenz_area", "bootstrap_ci", "poisson_rate", "gini_coefficient"],
        "charts": _charts([0, 1, 2, 6, 7, 9, 3, 14]),
        "context": "South Asia accounts for one-third of global maternal deaths, with Afghanistan's maternal mortality ratio exceeding 600 per 100,000 — yet obstetric trial infrastructure barely exists outside India.",
        "refs": [REF_GBD, REF_WHO, REF_CTGOV]
    },
    {
        "slug": "dengue-vector-borne", "title": "Dengue & Vector-Borne",
        "group": "health-disease", "paper_num": 6,
        "query": {"condition": "Dengue OR Chikungunya OR Malaria", "countries": SAARC_COUNTRIES},
        "stats": ["poisson_rate", "bootstrap_ci", "rate_ratio", "bayesian_rate", "spearman_correlation"],
        "charts": _charts([0, 6, 2, 7, 3, 9, 10, 14]),
        "context": "Dengue epidemics sweep SAARC nations annually with increasing severity, yet vaccine and therapeutic trial investment focuses on Southeast Asia and Latin America rather than South Asia.",
        "refs": [REF_GBD, REF_CTGOV, REF_WHO]
    },
    {
        "slug": "polio-last-mile-trials", "title": "Polio Last-Mile Trials",
        "group": "health-disease", "paper_num": 7,
        "query": {"condition": "Polio OR Poliomyelitis", "countries": ["Pakistan", "Afghanistan"]},
        "stats": ["kaplan_meier_survival", "bootstrap_ci", "rate_ratio", "poisson_rate", "bayesian_rate"],
        "charts": _charts([14, 0, 6, 2, 7, 9, 3, 11]),
        "context": "Pakistan and Afghanistan are the world's last two polio-endemic countries, making SAARC the epicenter of the eradication endgame where operational research trials are existentially important.",
        "refs": [REF_WHO, REF_CTGOV, REF_GBD]
    },
    {
        "slug": "thalassemia-haemoglobinopathies", "title": "Thalassemia & Haemoglobinopathies",
        "group": "health-disease", "paper_num": 8,
        "query": {"condition": "Thalassemia OR Hemoglobinopathy", "countries": SAARC_COUNTRIES},
        "stats": ["rate_ratio", "bootstrap_ci", "poisson_rate", "theil_index", "lorenz_area"],
        "charts": _charts([0, 1, 2, 7, 3, 6, 9, 11]),
        "context": "The thalassemia belt runs through South Asia, with Pakistan alone having 100,000 transfusion-dependent patients, yet gene therapy trials concentrate in Europe and the US where patients are fewer.",
        "refs": [REF_GBD, REF_CTGOV]
    },
    {
        "slug": "mental-health-desert", "title": "Mental Health Desert",
        "group": "health-disease", "paper_num": 9,
        "query": {"condition": "Depression OR Anxiety OR Schizophrenia OR Mental Health", "countries": SAARC_COUNTRIES},
        "stats": ["shannon_entropy", "rate_ratio", "bootstrap_ci", "lorenz_area", "chi_squared"],
        "charts": _charts([1, 0, 3, 4, 6, 9, 7, 12]),
        "context": "South Asia has 0.3 psychiatrists per 100,000 people versus 15 in Europe, and mental health trial investment is among the lowest of any disease category, reflecting deep stigma and policy neglect.",
        "refs": [REF_GBD, REF_WHO, REF_CTGOV]
    },
    {
        "slug": "childhood-pneumonia-diarrhoea", "title": "Childhood Pneumonia & Diarrhoea",
        "group": "health-disease", "paper_num": 10,
        "query": {"condition": "Pneumonia OR Diarrhea OR Rotavirus", "countries": SAARC_COUNTRIES},
        "stats": ["poisson_rate", "rate_ratio", "bootstrap_ci", "bayesian_rate", "morans_i"],
        "charts": _charts([0, 2, 6, 7, 3, 9, 14, 11]),
        "context": "Pneumonia and diarrhea together kill more SAARC children than any other causes, yet the trial pipeline for improved oral rehydration, zinc, and pneumococcal vaccines in South Asian populations is thin.",
        "refs": [REF_GBD, REF_CTGOV, REF_WHO]
    },
    {
        "slug": "cancer-trial-disparity", "title": "Cancer Trial Disparity",
        "group": "health-disease", "paper_num": 11,
        "query": {"condition": "Cancer", "countries": SAARC_COUNTRIES},
        "stats": ["hhi_index", "chi_squared", "bootstrap_ci", "theil_index", "lorenz_area"],
        "charts": _charts([4, 0, 1, 7, 6, 9, 3, 12]),
        "context": "Cancer incidence in South Asia is rising rapidly with the epidemiological transition, yet trial investment concentrates on cancers prevalent in Western populations rather than oral, cervical, and gastric cancers dominant in SAARC.",
        "refs": [REF_GBD, REF_CTGOV]
    },
    {
        "slug": "rheumatic-heart-disease", "title": "Rheumatic Heart Disease",
        "group": "health-disease", "paper_num": 12,
        "query": {"condition": "Rheumatic Heart Disease OR Rheumatic Fever", "countries": SAARC_COUNTRIES},
        "stats": ["rate_ratio", "bootstrap_ci", "poisson_rate", "bayesian_rate", "lorenz_area"],
        "charts": _charts([0, 1, 2, 6, 7, 9, 3, 14]),
        "context": "Rheumatic heart disease kills more young South Asians than any other cardiac condition and is entirely preventable with penicillin prophylaxis, yet delivery strategy trials are almost nonexistent.",
        "refs": [REF_GBD, REF_CTGOV, REF_WHO]
    },
    {
        "slug": "chronic-kidney-disease", "title": "Chronic Kidney Disease",
        "group": "health-disease", "paper_num": 13,
        "query": {"condition": "Chronic Kidney Disease OR Nephrology", "countries": SAARC_COUNTRIES},
        "stats": ["rate_ratio", "bootstrap_ci", "kaplan_meier_survival", "poisson_rate", "bayesian_rate"],
        "charts": _charts([14, 0, 2, 6, 7, 9, 3, 11]),
        "context": "CKD prevalence in South Asia is 15-17%, driven by diabetes and hypertension epidemics, yet renal trial investment is negligible and dialysis access in Pakistan and Bangladesh is under 10%.",
        "refs": [REF_GBD, REF_CTGOV]
    },
    {
        "slug": "neonatal-mortality-focus", "title": "Neonatal Mortality Focus",
        "group": "health-disease", "paper_num": 14,
        "query": {"condition": "Neonatal OR Newborn", "countries": SAARC_COUNTRIES},
        "stats": ["rate_ratio", "lorenz_area", "bootstrap_ci", "poisson_rate", "gini_coefficient"],
        "charts": _charts([1, 0, 2, 6, 7, 9, 3, 14]),
        "context": "South Asia accounts for 40% of global neonatal deaths, yet the trial pipeline for context-appropriate low-resource neonatal interventions — kangaroo care, chlorhexidine, simplified antibiotic regimens — remains insufficient.",
        "refs": [REF_GBD, REF_WHO, REF_CTGOV]
    },
    {
        "slug": "malnutrition-stunting", "title": "Malnutrition & Stunting",
        "group": "health-disease", "paper_num": 15,
        "query": {"condition": "Malnutrition OR Stunting OR Wasting", "countries": SAARC_COUNTRIES},
        "stats": ["linear_regression", "bootstrap_ci", "rate_ratio", "poisson_rate", "spearman_correlation"],
        "charts": _charts([6, 0, 10, 2, 7, 9, 3, 11]),
        "context": "South Asia has the world's highest stunting prevalence — 35% of children under five — yet nutrition intervention trials rarely account for the region's unique dietary patterns and micronutrient profiles.",
        "refs": [REF_GBD, REF_WHO, REF_CTGOV]
    },
    {
        "slug": "antimicrobial-resistance", "title": "Antimicrobial Resistance",
        "group": "health-disease", "paper_num": 16,
        "query": {"condition": "Antimicrobial Resistance OR Antibiotic Resistance", "countries": SAARC_COUNTRIES},
        "stats": ["poisson_rate", "bootstrap_ci", "rate_ratio", "bayesian_rate", "linear_regression"],
        "charts": _charts([6, 0, 2, 7, 10, 9, 3, 14]),
        "context": "South Asia is a global AMR hotspot, with over-the-counter antibiotic access, unregulated veterinary use, and pharmaceutical effluent creating resistance genes that spread globally.",
        "refs": [REF_GBD, REF_CTGOV, REF_WHO]
    },
    {
        "slug": "snakebite-neglected-crisis", "title": "Snakebite Neglected Crisis",
        "group": "health-disease", "paper_num": 17,
        "query": {"condition": "Snakebite OR Snake Envenomation", "countries": SAARC_COUNTRIES},
        "stats": ["poisson_rate", "rate_ratio", "bootstrap_ci", "permutation_test", "bayesian_rate"],
        "charts": _charts([0, 2, 7, 6, 3, 9, 14, 11]),
        "context": "India alone accounts for nearly half of global snakebite deaths, yet antivenom trial investment is near zero and the subcontinent relies on antivenoms with limited cross-species efficacy.",
        "refs": [REF_GBD, REF_CTGOV]
    },
    {
        "slug": "leishmaniasis-kala-azar", "title": "Leishmaniasis (Kala-azar)",
        "group": "health-disease", "paper_num": 18,
        "query": {"condition": "Leishmaniasis OR Kala-azar", "countries": SAARC_COUNTRIES},
        "stats": ["rate_ratio", "bootstrap_ci", "poisson_rate", "bayesian_rate", "kaplan_meier_survival"],
        "charts": _charts([0, 14, 2, 6, 7, 9, 3, 10]),
        "context": "The India-Nepal-Bangladesh triangle is the world's largest visceral leishmaniasis endemic zone, and elimination efforts depend on a trial pipeline for short-course, oral treatments.",
        "refs": [REF_GBD, REF_WHO, REF_CTGOV]
    },
    {
        "slug": "air-pollution-respiratory", "title": "Air Pollution & Respiratory",
        "group": "health-disease", "paper_num": 19,
        "query": {"condition": "Air Pollution OR COPD OR Asthma", "countries": SAARC_COUNTRIES},
        "stats": ["spearman_correlation", "bootstrap_ci", "rate_ratio", "linear_regression", "poisson_rate"],
        "charts": _charts([10, 0, 2, 6, 7, 9, 3, 12]),
        "context": "South Asia has 14 of the world's 20 most polluted cities, yet respiratory trial investment barely acknowledges the unique phenotype of pollution-driven COPD in never-smokers.",
        "refs": [REF_GBD, REF_WHO, REF_CTGOV]
    },
    {
        "slug": "hypertension-awareness-gap", "title": "Hypertension Awareness Gap",
        "group": "health-disease", "paper_num": 20,
        "query": {"condition": "Hypertension", "countries": SAARC_COUNTRIES},
        "stats": ["poisson_rate", "rate_ratio", "bootstrap_ci", "lorenz_area", "gini_coefficient"],
        "charts": _charts([0, 1, 2, 6, 7, 9, 3, 11]),
        "context": "With 30-40% prevalence and under 25% awareness, hypertension is South Asia's silent killer — yet community-based screening and treatment trial designs remain rare.",
        "refs": [REF_GBD, REF_CTGOV, REF_WHO]
    },
    {
        "slug": "hiv-low-prevalence-paradox", "title": "HIV Low-Prevalence Paradox",
        "group": "health-disease", "paper_num": 21,
        "query": {"condition": "HIV", "countries": SAARC_COUNTRIES},
        "stats": ["rate_ratio", "bootstrap_ci", "bayesian_rate", "poisson_rate", "chi_squared"],
        "charts": _charts([0, 2, 3, 6, 7, 9, 14, 11]),
        "context": "South Asia's low overall HIV prevalence masks concentrated epidemics among key populations — MSM, PWID, sex workers — whose trials face profound ethical and recruitment challenges in conservative societies.",
        "refs": [REF_GBD, REF_WHO, REF_CTGOV]
    },
    {
        "slug": "surgical-trial-scarcity", "title": "Surgical Trial Scarcity",
        "group": "health-disease", "paper_num": 22,
        "query": {"condition": "Surgery OR Surgical", "countries": SAARC_COUNTRIES},
        "stats": ["rate_ratio", "bootstrap_ci", "chi_squared", "poisson_rate", "odds_ratio"],
        "charts": _charts([0, 2, 7, 3, 6, 9, 11, 4]),
        "context": "South Asia faces a surgical workforce crisis with 0.7 surgeons per 100,000 versus 50 in Europe, yet surgical trial investment is among the lowest of all specialties in the region.",
        "refs": [REF_GBD, REF_CTGOV]
    },
    {
        "slug": "eye-health-blindness", "title": "Eye Health & Blindness",
        "group": "health-disease", "paper_num": 23,
        "query": {"condition": "Cataract OR Glaucoma OR Blindness OR Ophthalmology", "countries": SAARC_COUNTRIES},
        "stats": ["rate_ratio", "bootstrap_ci", "poisson_rate", "bayesian_rate", "lorenz_area"],
        "charts": _charts([0, 1, 2, 6, 7, 9, 3, 14]),
        "context": "South Asia carries the world's largest burden of avoidable blindness, yet ophthalmic trial investment focuses on age-related macular degeneration — a condition of aging Western populations — rather than cataract and trachoma.",
        "refs": [REF_GBD, REF_CTGOV, REF_WHO]
    },
    {
        "slug": "oral-health-neglect", "title": "Oral Health Neglect",
        "group": "health-disease", "paper_num": 24,
        "query": {"condition": "Oral Cancer OR Dental OR Oral Health", "countries": SAARC_COUNTRIES},
        "stats": ["poisson_rate", "bootstrap_ci", "rate_ratio", "bayesian_rate", "chi_squared"],
        "charts": _charts([0, 2, 3, 6, 7, 9, 13, 11]),
        "context": "Oral cancer rates in South Asia are among the world's highest due to betel nut, paan, and gutka use, yet oral health trial investment is nearly nonexistent.",
        "refs": [REF_GBD, REF_CTGOV]
    },
    {
        "slug": "reproductive-health-contraception", "title": "Reproductive Health & Contraception",
        "group": "health-disease", "paper_num": 25,
        "query": {"condition": "Contraception OR Family Planning OR Reproductive Health", "countries": SAARC_COUNTRIES},
        "stats": ["theil_index", "bootstrap_ci", "rate_ratio", "lorenz_area", "poisson_rate"],
        "charts": _charts([1, 0, 2, 6, 7, 9, 3, 11]),
        "context": "Unmet need for family planning affects 80 million South Asian women, yet contraception trial investment focuses on new methods rather than delivery strategies for existing ones in conservative settings.",
        "refs": [REF_GBD, REF_WHO, REF_CTGOV]
    },
    {
        "slug": "ncd-communicable-balance", "title": "NCD vs Communicable Balance",
        "group": "health-disease", "paper_num": 26,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["chi_squared", "bootstrap_ci", "rate_ratio", "kl_divergence", "shannon_entropy"],
        "charts": _charts([9, 0, 4, 7, 3, 6, 1, 11]),
        "context": "South Asia faces a dual burden — communicable diseases that haven't been conquered and NCDs that are arriving early — yet the trial portfolio tilts heavily toward infectious disease, leaving the NCD epidemic under-researched.",
        "refs": [REF_GBD, REF_WHO, REF_CTGOV]
    },
    {
        "slug": "rare-disease-orphan-gap", "title": "Rare Disease Orphan Gap",
        "group": "health-disease", "paper_num": 27,
        "query": {"condition": "Rare Disease OR Orphan Drug", "countries": SAARC_COUNTRIES},
        "stats": ["poisson_rate", "bootstrap_ci", "bayesian_rate", "rate_ratio", "shannon_entropy"],
        "charts": _charts([0, 2, 3, 6, 7, 9, 14, 12]),
        "context": "South Asia's consanguinity rates produce a high burden of rare genetic diseases, yet orphan drug development and rare disease trial infrastructure is effectively nonexistent in the region.",
        "refs": [REF_GBD, REF_CTGOV]
    },
    {
        "slug": "traditional-medicine-trials", "title": "Traditional Medicine Trials",
        "group": "health-disease", "paper_num": 28,
        "query": {"condition": "Ayurveda OR Unani OR Traditional Medicine", "countries": SAARC_COUNTRIES},
        "stats": ["chi_squared", "bootstrap_ci", "shannon_entropy", "network_centrality", "rate_ratio"],
        "charts": _charts([5, 0, 4, 7, 3, 9, 6, 12]),
        "context": "Ayurveda, Unani, and Siddha systems serve hundreds of millions of South Asians, yet rigorous clinical trials of traditional remedies remain rare despite government initiatives like India's AYUSH ministry.",
        "refs": [REF_CTGOV, REF_SINGH]
    },
    {
        "slug": "vaccine-trial-pipeline", "title": "Vaccine Trial Pipeline",
        "group": "health-disease", "paper_num": 29,
        "query": {"condition": "Vaccine", "countries": SAARC_COUNTRIES},
        "stats": ["hhi_index", "bootstrap_ci", "rate_ratio", "theil_index", "linear_regression"],
        "charts": _charts([4, 0, 6, 7, 1, 9, 3, 11]),
        "context": "India's Serum Institute produces more vaccine doses than any manufacturer globally, yet vaccine trial design in SAARC rarely addresses the unique immunological profiles of South Asian populations.",
        "refs": [REF_CTGOV, REF_WHO]
    },
    {
        "slug": "palliative-care-evidence", "title": "Palliative Care Evidence",
        "group": "health-disease", "paper_num": 30,
        "query": {"condition": "Palliative Care OR Hospice", "countries": SAARC_COUNTRIES},
        "stats": ["poisson_rate", "bootstrap_ci", "rate_ratio", "bayesian_rate", "permutation_test"],
        "charts": _charts([0, 6, 2, 7, 3, 9, 14, 11]),
        "context": "Morphine availability in South Asia is among the world's lowest due to restrictive narcotics policies, and the trial pipeline for affordable pain management in the region is nearly empty.",
        "refs": [REF_GBD, REF_CTGOV]
    },
    {
        "slug": "adolescent-health-gap", "title": "Adolescent Health Gap",
        "group": "health-disease", "paper_num": 31,
        "query": {"condition": "Adolescent Health OR Youth", "countries": SAARC_COUNTRIES},
        "stats": ["rate_ratio", "bootstrap_ci", "poisson_rate", "linear_regression", "bayesian_rate"],
        "charts": _charts([6, 0, 2, 10, 7, 9, 3, 14]),
        "context": "South Asia has 350 million adolescents whose health needs — mental health, sexual health, nutrition — are poorly addressed by trial designs that treat them as either small adults or large children.",
        "refs": [REF_GBD, REF_WHO, REF_CTGOV]
    },
    {
        "slug": "geriatric-trial-exclusion", "title": "Geriatric Trial Exclusion",
        "group": "health-disease", "paper_num": 32,
        "query": {"condition": "Elderly OR Geriatric", "countries": SAARC_COUNTRIES},
        "stats": ["rate_ratio", "bootstrap_ci", "poisson_rate", "chi_squared", "odds_ratio"],
        "charts": _charts([0, 2, 3, 6, 7, 9, 11, 14]),
        "context": "South Asia's over-60 population will reach 300 million by 2050, yet geriatric medicine trials are almost nonexistent — the region is ageing into an evidence vacuum with no adapted treatment protocols.",
        "refs": [REF_GBD, REF_CTGOV]
    },
    {
        "slug": "occupational-health", "title": "Occupational Health",
        "group": "health-disease", "paper_num": 33,
        "query": {"condition": "Occupational Health OR Occupational Disease", "countries": SAARC_COUNTRIES},
        "stats": ["rate_ratio", "bootstrap_ci", "poisson_rate", "spearman_correlation", "chi_squared"],
        "charts": _charts([0, 2, 10, 6, 7, 9, 3, 4]),
        "context": "Textile workers in Bangladesh, brick kiln laborers in Pakistan, and pesticide-exposed farmers across SAARC face occupational hazards with virtually no trial evidence for prevention or treatment.",
        "refs": [REF_GBD, REF_CTGOV, REF_WHO]
    },
    {
        "slug": "burn-trauma-trials", "title": "Burn & Trauma Trials",
        "group": "health-disease", "paper_num": 34,
        "query": {"condition": "Burns OR Trauma OR Emergency Medicine", "countries": SAARC_COUNTRIES},
        "stats": ["poisson_rate", "bootstrap_ci", "rate_ratio", "bayesian_rate", "chi_squared"],
        "charts": _charts([0, 6, 2, 7, 3, 9, 14, 11]),
        "context": "Burns affect 300,000 South Asians annually — many from domestic cooking fires and acid attacks — yet burn care trial investment is negligible despite high mortality and disability burden.",
        "refs": [REF_GBD, REF_CTGOV]
    },
    {
        "slug": "disease-burden-concordance-index", "title": "Disease Burden Concordance Index",
        "group": "health-disease", "paper_num": 35,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["spearman_correlation", "kl_divergence", "bootstrap_ci", "shannon_entropy", "gini_coefficient"],
        "charts": _charts([9, 0, 4, 10, 1, 6, 7, 11]),
        "context": "The concordance between disease burden (DALYs) and trial investment across SAARC reveals systematic misalignment — conditions causing the most suffering receive disproportionately little research attention.",
        "refs": [REF_GBD, REF_CTGOV, REF_WHO]
    },
]

# ═══════════════════════════════════════════════════════════
#  GROUP 3: GOVERNANCE, JUSTICE & SOVEREIGNTY (35 papers)
# ═══════════════════════════════════════════════════════════
GOV_PAPERS = [
    {
        "slug": "foreign-sponsor-dominance", "title": "Foreign Sponsor Dominance",
        "group": "governance-justice", "paper_num": 1,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["hhi_index", "gini_coefficient", "bootstrap_ci", "theil_index", "concentration_index"],
        "charts": _charts([8, 0, 1, 7, 4, 9, 6, 3]),
        "context": "Foreign pharmaceutical companies sponsor the majority of SAARC trials, using South Asian populations to generate evidence for global markets while contributing minimally to local research capacity.",
        "refs": [REF_DRAIN, REF_LANG, REF_CTGOV]
    },
    {
        "slug": "pharma-vs-academic-split", "title": "Pharma vs Academic Split",
        "group": "governance-justice", "paper_num": 2,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["chi_squared", "rate_ratio", "bootstrap_ci", "odds_ratio", "gini_coefficient"],
        "charts": _charts([7, 0, 2, 3, 6, 9, 11, 4]),
        "context": "The pharma-academic split in SAARC trials reveals that industry funds the majority, setting research agendas around commercial products rather than public health priorities.",
        "refs": [REF_CTGOV, REF_DRAIN, REF_LANG]
    },
    {
        "slug": "data-sovereignty-gap", "title": "Data Sovereignty Gap",
        "group": "governance-justice", "paper_num": 3,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["chi_squared", "bootstrap_ci", "rate_ratio", "network_centrality", "shannon_entropy"],
        "charts": _charts([5, 0, 8, 7, 3, 9, 6, 4]),
        "context": "Clinical trial data generated from SAARC populations frequently leaves the region for analysis in Northern institutions, creating a data sovereignty deficit where South Asian researchers cannot access their own populations' data.",
        "refs": [REF_HEDT, REF_LANG, REF_CTGOV]
    },
    {
        "slug": "post-trial-access-commitments", "title": "Post-Trial Access Commitments",
        "group": "governance-justice", "paper_num": 4,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["kaplan_meier_survival", "bootstrap_ci", "rate_ratio", "chi_squared", "bayesian_rate"],
        "charts": _charts([14, 0, 2, 6, 7, 9, 3, 11]),
        "context": "Post-trial access — the obligation to provide beneficial treatments after a trial ends — is poorly enforced in SAARC, leaving participants who helped prove a drug's efficacy unable to access it.",
        "refs": [REF_LANG, REF_SINGH, REF_CTGOV]
    },
    {
        "slug": "informed-consent-language", "title": "Informed Consent Language",
        "group": "governance-justice", "paper_num": 5,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["shannon_entropy", "chi_squared", "bootstrap_ci", "theil_index", "rate_ratio"],
        "charts": _charts([4, 0, 9, 7, 3, 6, 1, 12]),
        "context": "SAARC nations speak hundreds of languages, yet trial consent documents are typically in English or a single national language, excluding populations whose mother tongue is neither.",
        "refs": [REF_LANG, REF_CTGOV]
    },
    {
        "slug": "ethics-committee-capacity", "title": "Ethics Committee Capacity",
        "group": "governance-justice", "paper_num": 6,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["poisson_rate", "bootstrap_ci", "rate_ratio", "bayesian_rate", "linear_regression"],
        "charts": _charts([7, 0, 6, 3, 9, 2, 14, 11]),
        "context": "Many SAARC nations have fewer than 10 accredited ethics committees reviewing hundreds of protocols, creating bottlenecks that delay research and may compromise review quality.",
        "refs": [REF_LANG, REF_SINGH, REF_CTGOV]
    },
    {
        "slug": "participant-compensation-equity", "title": "Participant Compensation Equity",
        "group": "governance-justice", "paper_num": 7,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["gini_coefficient", "bootstrap_ci", "rate_ratio", "permutation_test", "lorenz_area"],
        "charts": _charts([1, 0, 3, 7, 11, 9, 6, 2]),
        "context": "Trial participant compensation in South Asia raises unique ethical tensions — $5/day may be a family's weekly income, creating undue inducement, while withholding it exploits poverty.",
        "refs": [REF_LANG, REF_CTGOV]
    },
    {
        "slug": "gender-pi-leadership", "title": "Gender in PI Leadership",
        "group": "governance-justice", "paper_num": 8,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["odds_ratio", "bootstrap_ci", "chi_squared", "rate_ratio", "linear_regression"],
        "charts": _charts([2, 0, 6, 11, 7, 9, 3, 4]),
        "context": "Female principal investigators lead a small minority of SAARC trials despite women comprising 70% of healthcare workers in countries like Bangladesh, reflecting deeply embedded patriarchal academic structures.",
        "refs": [REF_HEDT, REF_CTGOV]
    },
    {
        "slug": "regulatory-harmonization", "title": "Regulatory Harmonization",
        "group": "governance-justice", "paper_num": 9,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["network_centrality", "chi_squared", "bootstrap_ci", "shannon_entropy", "rate_ratio"],
        "charts": _charts([5, 0, 9, 8, 7, 6, 3, 4]),
        "context": "Each SAARC nation maintains separate regulatory frameworks with no mutual recognition, meaning a trial approved in India must repeat the entire approval process in Pakistan — a barrier that fragments the regional research space.",
        "refs": [REF_DRAP, REF_SINGH, REF_CTGOV]
    },
    {
        "slug": "results-reporting-compliance", "title": "Results Reporting Compliance",
        "group": "governance-justice", "paper_num": 10,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["chi_squared", "bootstrap_ci", "rate_ratio", "odds_ratio", "poisson_rate"],
        "charts": _charts([7, 0, 2, 6, 3, 9, 13, 11]),
        "context": "Only a fraction of SAARC trials report results on ClinicalTrials.gov or in peer-reviewed publications, wasting research investment and hiding potentially important safety signals.",
        "refs": [REF_CHAN, REF_CTGOV]
    },
    {
        "slug": "publication-bias-signal", "title": "Publication Bias Signal",
        "group": "governance-justice", "paper_num": 11,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["rate_ratio", "bootstrap_ci", "chi_squared", "bayesian_rate", "poisson_rate"],
        "charts": _charts([13, 0, 2, 6, 7, 9, 3, 11]),
        "context": "Publication bias in SAARC trials is compounded by language barriers, limited journal access, and the pressure to publish positive results — creating an evidence base that systematically overstates treatment effects.",
        "refs": [REF_CHAN, REF_HEDT, REF_CTGOV]
    },
    {
        "slug": "cro-outsourcing-patterns", "title": "CRO Outsourcing Patterns",
        "group": "governance-justice", "paper_num": 12,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["hhi_index", "network_centrality", "bootstrap_ci", "gini_coefficient", "concentration_index"],
        "charts": _charts([5, 8, 0, 4, 7, 9, 6, 3]),
        "context": "India is the world's largest CRO outsourcing destination, but this positions South Asian populations as low-cost research subjects for multinational sponsors rather than sovereign research actors.",
        "refs": [REF_DRAIN, REF_CTGOV]
    },
    {
        "slug": "colonial-research-legacy", "title": "Colonial Research Legacy",
        "group": "governance-justice", "paper_num": 13,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["network_centrality", "chi_squared", "bootstrap_ci", "spearman_correlation", "hhi_index"],
        "charts": _charts([5, 8, 0, 4, 7, 9, 6, 3]),
        "context": "The British colonial research infrastructure — AIIMS, CMC Vellore, Aga Khan — continues to anchor SAARC's trial geography, demonstrating how colonial patterns persist in postcolonial research.",
        "refs": [REF_LANG, REF_DRAIN, REF_CTGOV]
    },
    {
        "slug": "south-south-collaboration", "title": "South-South Collaboration",
        "group": "governance-justice", "paper_num": 14,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["network_centrality", "bootstrap_ci", "rate_ratio", "shannon_entropy", "poisson_rate"],
        "charts": _charts([5, 0, 6, 8, 7, 9, 10, 3]),
        "context": "South-South collaboration between SAARC and African or Latin American nations could create alternative research partnerships, but such networks remain embryonic compared to North-South collaborations.",
        "refs": [REF_DRAIN, REF_CTGOV]
    },
    {
        "slug": "who-essential-medicines-trials", "title": "WHO Essential Medicines Trials",
        "group": "governance-justice", "paper_num": 15,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["chi_squared", "bootstrap_ci", "rate_ratio", "kl_divergence", "shannon_entropy"],
        "charts": _charts([9, 0, 4, 7, 3, 6, 1, 11]),
        "context": "The WHO Essential Medicines List defines treatments for priority diseases, yet SAARC trial investment only partially aligns with these globally endorsed priorities.",
        "refs": [REF_WHO, REF_CTGOV]
    },
    {
        "slug": "intellectual-property-barriers", "title": "Intellectual Property Barriers",
        "group": "governance-justice", "paper_num": 16,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["chi_squared", "rate_ratio", "bootstrap_ci", "odds_ratio", "bayesian_rate"],
        "charts": _charts([7, 0, 2, 6, 3, 9, 11, 8]),
        "context": "TRIPS compliance and patent regimes create barriers to generic drug trials in SAARC, paradoxically restricting the region that produces the world's most affordable medicines.",
        "refs": [REF_LANG, REF_CTGOV]
    },
    {
        "slug": "community-engagement-models", "title": "Community Engagement Models",
        "group": "governance-justice", "paper_num": 17,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["rate_ratio", "bootstrap_ci", "chi_squared", "poisson_rate", "bayesian_rate"],
        "charts": _charts([6, 0, 7, 3, 9, 2, 11, 4]),
        "context": "Community engagement in SAARC trials ranges from tokenistic CABs to deep participatory models like BRAC's community health worker networks, but formal documentation of engagement methods remains rare.",
        "refs": [REF_LANG, REF_CTGOV]
    },
    {
        "slug": "vulnerable-population-protections", "title": "Vulnerable Population Protections",
        "group": "governance-justice", "paper_num": 18,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["odds_ratio", "permutation_test", "bootstrap_ci", "chi_squared", "rate_ratio"],
        "charts": _charts([2, 0, 3, 7, 9, 6, 11, 4]),
        "context": "Refugees, migrant workers, Rohingya populations, and other vulnerable groups in SAARC face either blanket exclusion from trials or inadequate safeguards when included.",
        "refs": [REF_LANG, REF_WHO, REF_CTGOV]
    },
    {
        "slug": "trial-registration-timeliness", "title": "Trial Registration Timeliness",
        "group": "governance-justice", "paper_num": 19,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["chi_squared", "bootstrap_ci", "rate_ratio", "poisson_rate", "bayesian_rate"],
        "charts": _charts([6, 0, 7, 9, 3, 11, 2, 4]),
        "context": "Prospective trial registration before enrollment is an ICMJE requirement that many SAARC trials fail to meet, with retrospective registration rates exceeding 40% in some countries.",
        "refs": [REF_CHAN, REF_CTGOV]
    },
    {
        "slug": "funding-transparency", "title": "Funding Transparency",
        "group": "governance-justice", "paper_num": 20,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["hhi_index", "theil_index", "bootstrap_ci", "lorenz_area", "gini_coefficient"],
        "charts": _charts([8, 0, 1, 7, 4, 9, 6, 3]),
        "context": "Funding source disclosure in SAARC trials is inconsistent, making it impossible to trace the flow of research money or identify potential conflicts of interest.",
        "refs": [REF_LANG, REF_CTGOV]
    },
    {
        "slug": "benefit-sharing-agreements", "title": "Benefit-Sharing Agreements",
        "group": "governance-justice", "paper_num": 21,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["chi_squared", "bootstrap_ci", "rate_ratio", "bayesian_rate", "poisson_rate"],
        "charts": _charts([7, 0, 6, 3, 9, 2, 11, 4]),
        "context": "Benefit-sharing agreements ensuring that SAARC communities hosting trials receive tangible benefits beyond the research itself are rarely documented in trial protocols.",
        "refs": [REF_LANG, REF_CTGOV]
    },
    {
        "slug": "drap-approval-efficiency", "title": "DRAP Approval Efficiency",
        "group": "governance-justice", "paper_num": 22,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["kaplan_meier_survival", "bootstrap_ci", "rate_ratio", "poisson_rate", "linear_regression"],
        "charts": _charts([14, 0, 6, 7, 3, 9, 2, 11]),
        "context": "DRAP's trial approval timeline has improved but still averages 6-12 months, compared to 30-60 days for India's CDSCO, creating a regulatory speed disadvantage that diverts trials from Pakistan.",
        "refs": [REF_DRAP, REF_CTGOV]
    },
    {
        "slug": "multi-national-power-asymmetry", "title": "Multi-National Power Asymmetry",
        "group": "governance-justice", "paper_num": 23,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["network_centrality", "bootstrap_ci", "hhi_index", "theil_index", "gini_coefficient"],
        "charts": _charts([5, 8, 0, 7, 4, 9, 6, 1]),
        "context": "Multi-national trials in SAARC typically assign Southern sites as enrollment arms while Northern sites retain protocol design, data analysis, and publication — a structural power asymmetry.",
        "refs": [REF_HEDT, REF_DRAIN, REF_CTGOV]
    },
    {
        "slug": "local-capacity-building", "title": "Local Capacity Building",
        "group": "governance-justice", "paper_num": 24,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["linear_regression", "bootstrap_ci", "rate_ratio", "poisson_rate", "spearman_correlation"],
        "charts": _charts([6, 0, 10, 7, 3, 9, 11, 2]),
        "context": "Capacity building claims in trial protocols rarely translate into sustained local infrastructure — once the trial ends, equipment, training, and institutional knowledge frequently dissipate.",
        "refs": [REF_LANG, REF_HEDT, REF_CTGOV]
    },
    {
        "slug": "paediatric-trial-ethics", "title": "Paediatric Trial Ethics",
        "group": "governance-justice", "paper_num": 25,
        "query": {"condition": "Pediatric OR Child", "countries": SAARC_COUNTRIES},
        "stats": ["chi_squared", "bootstrap_ci", "rate_ratio", "bayesian_rate", "odds_ratio"],
        "charts": _charts([9, 0, 2, 7, 3, 6, 11, 4]),
        "context": "Pediatric trials in SAARC face unique consent challenges: child marriage, child labor, extended family decision-making, and varying age-of-assent norms across countries complicate ethical oversight.",
        "refs": [REF_LANG, REF_CTGOV]
    },
    {
        "slug": "placebo-use-appropriateness", "title": "Placebo Use Appropriateness",
        "group": "governance-justice", "paper_num": 26,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["odds_ratio", "chi_squared", "bootstrap_ci", "rate_ratio", "bayesian_rate"],
        "charts": _charts([2, 0, 3, 7, 6, 9, 11, 13]),
        "context": "Placebo-controlled trials in SAARC nations raise ethical concerns when proven treatments exist but are unavailable locally, creating a lower standard of care that enables placebo use impermissible in wealthy countries.",
        "refs": [REF_LANG, REF_SINGH, REF_CTGOV]
    },
    {
        "slug": "trial-waste-index", "title": "Trial Waste Index",
        "group": "governance-justice", "paper_num": 27,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["gini_coefficient", "lorenz_area", "bootstrap_ci", "rate_ratio", "linear_regression"],
        "charts": _charts([1, 0, 7, 6, 3, 9, 2, 11]),
        "context": "Avoidable research waste from poor design, incomplete reporting, and non-publication is estimated at 85% globally but may be even higher in SAARC where resource constraints amplify the cost of waste.",
        "refs": [REF_CHAN, REF_CTGOV]
    },
    {
        "slug": "open-access-results-sharing", "title": "Open Access Results Sharing",
        "group": "governance-justice", "paper_num": 28,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["chi_squared", "rate_ratio", "bootstrap_ci", "lorenz_area", "odds_ratio"],
        "charts": _charts([11, 0, 1, 2, 7, 9, 6, 3]),
        "context": "SAARC researchers face a double bind: publish in high-impact paywalled journals for career advancement, or choose open access with article processing charges that consume their entire research budget.",
        "refs": [REF_HEDT, REF_CTGOV]
    },
    {
        "slug": "refugee-displaced-population-trials", "title": "Refugee & Displaced Population Trials",
        "group": "governance-justice", "paper_num": 29,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["poisson_rate", "bootstrap_ci", "rate_ratio", "bayesian_rate", "permutation_test"],
        "charts": _charts([0, 2, 6, 7, 3, 9, 14, 12]),
        "context": "SAARC hosts millions of displaced people — Afghan refugees in Pakistan, Rohingya in Bangladesh, Tamil IDPs in Sri Lanka — whose health needs are largely absent from the clinical trial evidence base.",
        "refs": [REF_WHO, REF_LANG, REF_CTGOV]
    },
    {
        "slug": "religious-cultural-consent-factors", "title": "Religious & Cultural Consent Factors",
        "group": "governance-justice", "paper_num": 30,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["chi_squared", "bootstrap_ci", "shannon_entropy", "rate_ratio", "odds_ratio"],
        "charts": _charts([4, 0, 9, 7, 3, 6, 12, 11]),
        "context": "Religious beliefs about bodily integrity, blood donation, and intervention during fasting periods create consent complexities that Western ethical frameworks inadequately address in SAARC contexts.",
        "refs": [REF_LANG, REF_CTGOV]
    },
    {
        "slug": "government-funded-vs-external", "title": "Government-Funded vs External",
        "group": "governance-justice", "paper_num": 31,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["chi_squared", "rate_ratio", "bootstrap_ci", "gini_coefficient", "theil_index"],
        "charts": _charts([7, 0, 2, 6, 1, 9, 3, 11]),
        "context": "Government-funded trials in SAARC represent a small fraction of the total, meaning research agendas are largely set by foreign sponsors whose priorities may not align with national health needs.",
        "refs": [REF_CTGOV, REF_LANG]
    },
    {
        "slug": "academic-medical-center-gatekeeping", "title": "Academic Medical Center Gatekeeping",
        "group": "governance-justice", "paper_num": 32,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["hhi_index", "network_centrality", "bootstrap_ci", "gini_coefficient", "concentration_index"],
        "charts": _charts([5, 0, 4, 7, 1, 9, 6, 8]),
        "context": "A handful of elite academic medical centers — AIIMS, Aga Khan, CMC Vellore — gatekeep trial access, concentrating research capacity and blocking the emergence of new sites.",
        "refs": [REF_DRAIN, REF_CTGOV]
    },
    {
        "slug": "whistleblower-misconduct-reports", "title": "Whistleblower & Misconduct Reports",
        "group": "governance-justice", "paper_num": 33,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["poisson_rate", "bootstrap_ci", "rate_ratio", "chi_squared", "bayesian_rate"],
        "charts": _charts([13, 0, 7, 3, 6, 9, 2, 4]),
        "context": "Research misconduct reporting in SAARC is hampered by weak whistleblower protections, hierarchical academic cultures, and institutional incentives to suppress negative findings.",
        "refs": [REF_LANG, REF_CTGOV]
    },
    {
        "slug": "lmic-authorship-position", "title": "LMIC Authorship Position",
        "group": "governance-justice", "paper_num": 34,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["odds_ratio", "bootstrap_ci", "chi_squared", "rate_ratio", "network_centrality"],
        "charts": _charts([2, 0, 5, 11, 7, 9, 6, 3]),
        "context": "South Asian investigators frequently occupy middle-author positions on papers from their own trials, while Northern collaborators claim first and last authorship — the positions that drive career advancement.",
        "refs": [REF_HEDT, REF_CTGOV]
    },
    {
        "slug": "sovereignty-composite-score", "title": "Sovereignty Composite Score",
        "group": "governance-justice", "paper_num": 35,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["gini_coefficient", "shannon_entropy", "bootstrap_ci", "theil_index", "atkinson_index"],
        "charts": _charts([9, 0, 1, 4, 7, 6, 8, 3]),
        "context": "A composite sovereignty score combining data ownership, authorship equity, regulatory control, and funding independence reveals that most SAARC nations have low research sovereignty despite hosting thousands of trials.",
        "refs": [REF_HEDT, REF_LANG, REF_CTGOV]
    },
]

# ═══════════════════════════════════════════════════════════
#  GROUP 4: METHODS, DESIGN & RESEARCH SYSTEMS (35 papers)
# ═══════════════════════════════════════════════════════════
METHODS_PAPERS = [
    {
        "slug": "phase-distribution-analysis", "title": "Phase Distribution Analysis",
        "group": "methods-systems", "paper_num": 1,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["chi_squared", "bootstrap_ci", "rate_ratio", "kl_divergence", "shannon_entropy"],
        "charts": _charts([7, 0, 2, 3, 6, 9, 4, 11]),
        "context": "SAARC's trial portfolio is heavily skewed toward Phase III — late-stage confirmation — with minimal Phase I/II early discovery, reflecting the region's role as a testing ground rather than an innovation hub.",
        "refs": [REF_CHAN, REF_CTGOV]
    },
    {
        "slug": "randomization-quality-audit", "title": "Randomization Quality Audit",
        "group": "methods-systems", "paper_num": 2,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["chi_squared", "bootstrap_ci", "rate_ratio", "odds_ratio", "permutation_test"],
        "charts": _charts([2, 0, 9, 3, 7, 6, 11, 4]),
        "context": "Proper randomization — allocation concealment and sequence generation — is the gold standard for bias prevention, but reporting of randomization methods in SAARC trials is often incomplete or absent.",
        "refs": [REF_CHAN, REF_CTGOV]
    },
    {
        "slug": "sample-size-adequacy", "title": "Sample Size Adequacy",
        "group": "methods-systems", "paper_num": 3,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["rate_ratio", "bootstrap_ci", "linear_regression", "poisson_rate", "chi_squared"],
        "charts": _charts([10, 0, 2, 13, 7, 9, 3, 6]),
        "context": "Underpowered trials waste resources and participants' altruism by producing inconclusive results, yet a substantial fraction of SAARC trials fail to achieve their planned enrollment targets.",
        "refs": [REF_CHAN, REF_CTGOV]
    },
    {
        "slug": "primary-endpoint-selection", "title": "Primary Endpoint Selection",
        "group": "methods-systems", "paper_num": 4,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["shannon_entropy", "hhi_index", "bootstrap_ci", "chi_squared", "rate_ratio"],
        "charts": _charts([4, 0, 9, 7, 3, 6, 2, 12]),
        "context": "Primary endpoint selection in SAARC trials reveals a reliance on surrogate markers rather than patient-important outcomes, reflecting sponsors' desire for regulatory efficiency over clinical relevance.",
        "refs": [REF_CHAN, REF_CTGOV]
    },
    {
        "slug": "completion-rate-analysis", "title": "Completion Rate Analysis",
        "group": "methods-systems", "paper_num": 5,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["kaplan_meier_survival", "bootstrap_ci", "rate_ratio", "linear_regression", "bayesian_rate"],
        "charts": _charts([14, 0, 6, 7, 3, 9, 2, 11]),
        "context": "Trial completion rates in SAARC vary dramatically by country and sponsor type, with early termination rates exceeding 30% in some settings — representing wasted investment and participant burden.",
        "refs": [REF_CHAN, REF_CTGOV]
    },
    {
        "slug": "time-to-completion-trends", "title": "Time-to-Completion Trends",
        "group": "methods-systems", "paper_num": 6,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["linear_regression", "bootstrap_ci", "kaplan_meier_survival", "spearman_correlation", "bayesian_rate"],
        "charts": _charts([6, 14, 0, 10, 7, 9, 3, 11]),
        "context": "Time-to-completion for SAARC trials has been increasing despite global trends toward faster trials, suggesting worsening recruitment challenges and operational inefficiencies.",
        "refs": [REF_CHAN, REF_CTGOV]
    },
    {
        "slug": "adaptive-design-adoption", "title": "Adaptive Design Adoption",
        "group": "methods-systems", "paper_num": 7,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["linear_regression", "bootstrap_ci", "rate_ratio", "poisson_rate", "bayesian_rate"],
        "charts": _charts([6, 0, 10, 7, 3, 9, 2, 11]),
        "context": "Adaptive trial designs could benefit SAARC most — allowing mid-trial modifications based on emerging data — yet adoption lags years behind high-income countries.",
        "refs": [REF_CHAN, REF_CTGOV]
    },
    {
        "slug": "pragmatic-vs-explanatory", "title": "Pragmatic vs Explanatory",
        "group": "methods-systems", "paper_num": 8,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["shannon_entropy", "bootstrap_ci", "chi_squared", "rate_ratio", "kl_divergence"],
        "charts": _charts([9, 0, 3, 4, 7, 6, 12, 2]),
        "context": "South Asia needs pragmatic trials that test interventions under real-world conditions with overburdened health systems, yet most SAARC trials use explanatory designs imported from well-resourced settings.",
        "refs": [REF_CHAN, REF_CTGOV]
    },
    {
        "slug": "biostatistical-method-quality", "title": "Biostatistical Method Quality",
        "group": "methods-systems", "paper_num": 9,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["chi_squared", "bootstrap_ci", "rate_ratio", "shannon_entropy", "bayesian_rate"],
        "charts": _charts([4, 0, 9, 7, 3, 6, 2, 11]),
        "context": "Biostatistical capacity in SAARC is critically limited — South Asia has fewer trained biostatisticians than a single US academic medical center, leading to methodological errors in trial design and analysis.",
        "refs": [REF_CHAN, REF_CTGOV]
    },
    {
        "slug": "protocol-amendment-frequency", "title": "Protocol Amendment Frequency",
        "group": "methods-systems", "paper_num": 10,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["poisson_rate", "bootstrap_ci", "rate_ratio", "linear_regression", "chi_squared"],
        "charts": _charts([7, 0, 6, 3, 9, 2, 10, 11]),
        "context": "Frequent protocol amendments signal poor initial planning and can introduce bias, yet SAARC trials show higher amendment rates than global averages, partly due to unrealistic enrollment projections.",
        "refs": [REF_CHAN, REF_CTGOV]
    },
    {
        "slug": "recruitment-rate-analysis", "title": "Recruitment Rate Analysis",
        "group": "methods-systems", "paper_num": 11,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["linear_regression", "bootstrap_ci", "rate_ratio", "poisson_rate", "spearman_correlation"],
        "charts": _charts([6, 0, 10, 2, 7, 9, 3, 11]),
        "context": "SAARC's large populations make it attractive for rapid recruitment, but actual enrollment rates vary enormously by disease, site, and country — with some trials enrolling in days and others failing entirely.",
        "refs": [REF_CTGOV, REF_DRAIN]
    },
    {
        "slug": "dropout-attrition-patterns", "title": "Dropout & Attrition Patterns",
        "group": "methods-systems", "paper_num": 12,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["kaplan_meier_survival", "bootstrap_ci", "rate_ratio", "chi_squared", "linear_regression"],
        "charts": _charts([14, 0, 6, 7, 3, 9, 2, 11]),
        "context": "High attrition rates in SAARC trials — driven by migration, economic pressures, and transport barriers — threaten internal validity and waste the investment of participants who completed only partial follow-up.",
        "refs": [REF_CHAN, REF_CTGOV]
    },
    {
        "slug": "multi-arm-trial-efficiency", "title": "Multi-Arm Trial Efficiency",
        "group": "methods-systems", "paper_num": 13,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["rate_ratio", "bootstrap_ci", "poisson_rate", "chi_squared", "bayesian_rate"],
        "charts": _charts([7, 0, 6, 2, 3, 9, 11, 14]),
        "context": "Multi-arm trials share a common control group, increasing efficiency — a property especially valuable in South Asia where every enrolled participant represents a scarce resource in a resource-limited system.",
        "refs": [REF_CHAN, REF_CTGOV]
    },
    {
        "slug": "non-inferiority-trial-usage", "title": "Non-Inferiority Trial Usage",
        "group": "methods-systems", "paper_num": 14,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["rate_ratio", "bootstrap_ci", "chi_squared", "poisson_rate", "bayesian_rate"],
        "charts": _charts([2, 0, 7, 3, 9, 6, 11, 14]),
        "context": "Non-inferiority trials are critical for testing cheaper or simpler alternatives — exactly what SAARC needs — but NI margin justification is often inadequately reported in South Asian trials.",
        "refs": [REF_CHAN, REF_CTGOV]
    },
    {
        "slug": "cluster-rct-patterns", "title": "Cluster RCT Patterns",
        "group": "methods-systems", "paper_num": 15,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["linear_regression", "bootstrap_ci", "rate_ratio", "poisson_rate", "cohens_d"],
        "charts": _charts([10, 0, 2, 7, 3, 9, 6, 13]),
        "context": "Cluster-RCTs are ideal for community-level interventions in SAARC's village-based healthcare delivery systems, but many fail to report ICC values and design effect calculations.",
        "refs": [REF_CHAN, REF_CTGOV]
    },
    {
        "slug": "interim-analysis-reporting", "title": "Interim Analysis Reporting",
        "group": "methods-systems", "paper_num": 16,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["rate_ratio", "bootstrap_ci", "chi_squared", "poisson_rate", "bayesian_rate"],
        "charts": _charts([6, 0, 2, 7, 9, 3, 14, 11]),
        "context": "Data Safety Monitoring Boards provide independent oversight, but DSMB formation and interim analysis planning in SAARC trials is often ad hoc rather than protocol-mandated.",
        "refs": [REF_CHAN, REF_CTGOV]
    },
    {
        "slug": "composite-endpoint-prevalence", "title": "Composite Endpoint Prevalence",
        "group": "methods-systems", "paper_num": 17,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["shannon_entropy", "hhi_index", "bootstrap_ci", "rate_ratio", "chi_squared"],
        "charts": _charts([4, 0, 9, 7, 3, 6, 2, 12]),
        "context": "Composite endpoints increase statistical power but can mask clinically important differences between components — a risk when endpoints validated in Western populations may not apply in South Asian contexts.",
        "refs": [REF_CHAN, REF_CTGOV]
    },
    {
        "slug": "patient-reported-outcome-use", "title": "Patient-Reported Outcome Use",
        "group": "methods-systems", "paper_num": 18,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["rate_ratio", "bootstrap_ci", "poisson_rate", "chi_squared", "spearman_correlation"],
        "charts": _charts([6, 0, 2, 7, 3, 9, 11, 4]),
        "context": "Patient-reported outcomes capture what matters to patients, but most PRO instruments are developed in English-speaking Western populations and may lack cultural validity for South Asian patients.",
        "refs": [REF_CHAN, REF_CTGOV]
    },
    {
        "slug": "biomarker-driven-trial-design", "title": "Biomarker-Driven Trial Design",
        "group": "methods-systems", "paper_num": 19,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["rate_ratio", "bootstrap_ci", "chi_squared", "spearman_correlation", "linear_regression"],
        "charts": _charts([10, 0, 2, 7, 3, 9, 6, 4]),
        "context": "Biomarker-driven trials enable precision medicine, but SAARC's limited laboratory infrastructure and biobanking capacity constrain biomarker endpoint adoption across the region.",
        "refs": [REF_CHAN, REF_CTGOV]
    },
    {
        "slug": "bayesian-design-adoption", "title": "Bayesian Design Adoption",
        "group": "methods-systems", "paper_num": 20,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["bayesian_rate", "bootstrap_ci", "rate_ratio", "poisson_rate", "linear_regression"],
        "charts": _charts([6, 0, 2, 7, 9, 3, 14, 11]),
        "context": "Bayesian methods are ideally suited for South Asia's small-sample reality — incorporating prior knowledge to strengthen inference — yet Bayesian trial designs remain extremely rare in the region.",
        "refs": [REF_CHAN, REF_CTGOV]
    },
    {
        "slug": "registry-data-quality", "title": "Registry Data Quality",
        "group": "methods-systems", "paper_num": 21,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["chi_squared", "bootstrap_ci", "shannon_entropy", "rate_ratio", "poisson_rate"],
        "charts": _charts([4, 0, 7, 9, 3, 6, 13, 11]),
        "context": "Data completeness on ClinicalTrials.gov and CTRI for SAARC trials is often poor, with missing primary outcomes, enrollment figures, and results — undermining the registry's transparency function.",
        "refs": [REF_CHAN, REF_CTGOV]
    },
    {
        "slug": "cross-over-design-usage", "title": "Cross-Over Design Usage",
        "group": "methods-systems", "paper_num": 22,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["rate_ratio", "bootstrap_ci", "chi_squared", "poisson_rate", "cohens_d"],
        "charts": _charts([2, 0, 3, 7, 6, 9, 11, 4]),
        "context": "Cross-over designs halve the required sample size, making them efficient for resource-limited settings, yet their use in SAARC is limited by high dropout rates and carryover effect concerns.",
        "refs": [REF_CHAN, REF_CTGOV]
    },
    {
        "slug": "equivalence-trial-standards", "title": "Equivalence Trial Standards",
        "group": "methods-systems", "paper_num": 23,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["rate_ratio", "bootstrap_ci", "chi_squared", "odds_ratio", "cohens_d"],
        "charts": _charts([2, 0, 7, 3, 13, 9, 6, 11]),
        "context": "Equivalence trials testing generic vs branded drugs are critical for SAARC's pharmaceutical economies, yet equivalence margin selection and statistical analysis often fall below international standards.",
        "refs": [REF_CHAN, REF_CTGOV]
    },
    {
        "slug": "outcome-reporting-bias", "title": "Outcome Reporting Bias",
        "group": "methods-systems", "paper_num": 24,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["chi_squared", "bootstrap_ci", "odds_ratio", "rate_ratio", "bayesian_rate"],
        "charts": _charts([13, 0, 2, 7, 6, 9, 3, 4]),
        "context": "Selective outcome reporting — publishing positive endpoints while suppressing negative ones — is a pervasive threat to evidence integrity that may be amplified in SAARC by weak enforcement of registration requirements.",
        "refs": [REF_CHAN, REF_CTGOV]
    },
    {
        "slug": "subgroup-analysis-practices", "title": "Subgroup Analysis Practices",
        "group": "methods-systems", "paper_num": 25,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["chi_squared", "bootstrap_ci", "rate_ratio", "odds_ratio", "permutation_test"],
        "charts": _charts([2, 0, 9, 3, 7, 6, 11, 4]),
        "context": "Post-hoc subgroup analyses in SAARC trials are frequently overstated as confirmatory findings, particularly when trials are underpowered for the primary endpoint and investigators seek publishable results.",
        "refs": [REF_CHAN, REF_CTGOV]
    },
    {
        "slug": "follow-up-duration-adequacy", "title": "Follow-Up Duration Adequacy",
        "group": "methods-systems", "paper_num": 26,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["kaplan_meier_survival", "bootstrap_ci", "rate_ratio", "linear_regression", "bayesian_rate"],
        "charts": _charts([14, 0, 6, 7, 3, 9, 2, 11]),
        "context": "Long-term follow-up is essential for safety monitoring and durability assessment, but mobile populations and limited tracing systems in SAARC make sustained follow-up exceptionally challenging.",
        "refs": [REF_CHAN, REF_CTGOV]
    },
    {
        "slug": "real-world-evidence-integration", "title": "Real-World Evidence Integration",
        "group": "methods-systems", "paper_num": 27,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["rate_ratio", "bootstrap_ci", "poisson_rate", "linear_regression", "spearman_correlation"],
        "charts": _charts([6, 0, 10, 7, 3, 9, 2, 14]),
        "context": "Real-world evidence from electronic health records and insurance databases is transforming research in high-income countries, but SAARC's fragmented, paper-based health systems cannot yet generate RWE at scale.",
        "refs": [REF_CHAN, REF_CTGOV]
    },
    {
        "slug": "digital-health-trial-methods", "title": "Digital Health Trial Methods",
        "group": "methods-systems", "paper_num": 28,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["linear_regression", "bootstrap_ci", "rate_ratio", "poisson_rate", "bayesian_rate"],
        "charts": _charts([6, 0, 10, 7, 3, 9, 2, 11]),
        "context": "South Asia's mobile phone penetration exceeding 70% creates unique opportunities for mHealth trials that could leapfrog traditional clinical infrastructure in the region.",
        "refs": [REF_CTGOV, REF_WHO]
    },
    {
        "slug": "pilot-feasibility-studies", "title": "Pilot & Feasibility Studies",
        "group": "methods-systems", "paper_num": 29,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["poisson_rate", "bootstrap_ci", "rate_ratio", "bayesian_rate", "chi_squared"],
        "charts": _charts([0, 2, 6, 7, 3, 9, 10, 11]),
        "context": "Pilot studies are essential for testing trial feasibility in new settings, yet SAARC trials often skip this step, launching full-scale trials that then fail due to predictable operational challenges.",
        "refs": [REF_CHAN, REF_CTGOV]
    },
    {
        "slug": "systematic-review-coverage", "title": "Systematic Review Coverage",
        "group": "methods-systems", "paper_num": 30,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["rate_ratio", "bootstrap_ci", "chi_squared", "shannon_entropy", "poisson_rate"],
        "charts": _charts([9, 0, 4, 7, 3, 6, 2, 11]),
        "context": "SAARC trials are frequently excluded from Cochrane and other systematic reviews due to perceived quality concerns, creating a vicious cycle where South Asian evidence never influences global guidelines.",
        "refs": [REF_CHAN, REF_CTGOV]
    },
    {
        "slug": "benford-law-enrollment-audit", "title": "Benford's Law Enrollment Audit",
        "group": "methods-systems", "paper_num": 31,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["chi_squared", "bootstrap_ci", "kl_divergence", "rate_ratio", "permutation_test"],
        "charts": _charts([13, 0, 3, 7, 6, 9, 4, 2]),
        "context": "Benford's Law analysis of enrollment numbers can detect fabricated data — a forensic tool that reveals whether reported sample sizes follow the expected digit distribution of naturally occurring numbers.",
        "refs": [REF_CHAN, REF_CTGOV]
    },
    {
        "slug": "pca-trial-characteristics", "title": "PCA of Trial Characteristics",
        "group": "methods-systems", "paper_num": 32,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["spearman_correlation", "bootstrap_ci", "shannon_entropy", "linear_regression", "gini_coefficient"],
        "charts": _charts([10, 0, 4, 3, 7, 9, 6, 12]),
        "context": "Principal component analysis of SAARC trial characteristics reveals latent dimensions — a pharma-commercial axis and an academic-public-health axis — that explain the majority of variation in trial design.",
        "refs": [REF_CTGOV, REF_CHAN]
    },
    {
        "slug": "network-analysis-investigators", "title": "Network Analysis of Investigators",
        "group": "methods-systems", "paper_num": 33,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["network_centrality", "bootstrap_ci", "hhi_index", "shannon_entropy", "gini_coefficient"],
        "charts": _charts([5, 0, 4, 8, 7, 9, 6, 3]),
        "context": "Investigator network analysis reveals a small-world topology where a handful of well-connected PIs bridge most SAARC trial collaborations, creating fragility if these hub investigators retire or relocate.",
        "refs": [REF_CTGOV, REF_DRAIN]
    },
    {
        "slug": "machine-readable-protocol-quality", "title": "Machine-Readable Protocol Quality",
        "group": "methods-systems", "paper_num": 34,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["chi_squared", "bootstrap_ci", "rate_ratio", "shannon_entropy", "poisson_rate"],
        "charts": _charts([4, 0, 7, 9, 3, 6, 13, 11]),
        "context": "Machine-readable protocol fields on ClinicalTrials.gov enable automated quality assessment, but SAARC trials have higher rates of missing, inconsistent, or free-text entries that resist automated analysis.",
        "refs": [REF_CHAN, REF_CTGOV]
    },
    {
        "slug": "methodological-rigor-composite", "title": "Methodological Rigor Composite",
        "group": "methods-systems", "paper_num": 35,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["gini_coefficient", "shannon_entropy", "bootstrap_ci", "theil_index", "atkinson_index"],
        "charts": _charts([9, 0, 1, 4, 7, 6, 3, 11]),
        "context": "A composite methodological rigor score combining randomization quality, blinding, ITT compliance, and registration timeliness reveals wide variation across SAARC nations and sponsor types.",
        "refs": [REF_CHAN, REF_CTGOV]
    },
]

# ═══════════════════════════════════════════════════════════
#  GROUP 5: PAKISTAN DEEP-DIVE (50 papers)
# ═══════════════════════════════════════════════════════════

# --- Provincial Inequity (papers 1-10) ---
PAK_PROVINCIAL = [
    {
        "slug": "punjab-trial-dominance", "title": "Punjab Trial Dominance",
        "group": "pakistan-deep-dive", "paper_num": 1,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["hhi_index", "gini_coefficient", "bootstrap_ci", "concentration_index", "lorenz_area"],
        "charts": _charts([15, 0, 1, 7, 6, 9, 3, 11]),
        "context": "Punjab province hosts over 60% of Pakistan's clinical trials, with Lahore alone accounting for a disproportionate share, reflecting the province's medical infrastructure advantage and 110 million population.",
        "refs": [REF_DRAP, REF_CTGOV, REF_HEC]
    },
    {
        "slug": "sindh-karachi-landscape", "title": "Sindh & Karachi Landscape",
        "group": "pakistan-deep-dive", "paper_num": 2,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["hhi_index", "bootstrap_ci", "gini_coefficient", "poisson_rate", "rate_ratio"],
        "charts": _charts([15, 0, 1, 3, 6, 9, 7, 10]),
        "context": "Sindh's trial landscape is dominated by Karachi's private medical universities, creating an urban enclave of research excellence surrounded by a province where 70% of the population has no trial access.",
        "refs": [REF_DRAP, REF_CTGOV]
    },
    {
        "slug": "kpk-tribal-areas", "title": "KPK & Tribal Areas",
        "group": "pakistan-deep-dive", "paper_num": 3,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["poisson_rate", "bootstrap_ci", "rate_ratio", "bayesian_rate", "permutation_test"],
        "charts": _charts([15, 0, 2, 6, 7, 9, 3, 14]),
        "context": "Khyber Pakhtunkhwa's trial infrastructure is concentrated in Peshawar, while the former tribal areas — recently merged into the province — remain among the most research-deprived regions on earth.",
        "refs": [REF_DRAP, REF_CTGOV, REF_GBD]
    },
    {
        "slug": "balochistan-research-desert", "title": "Balochistan Research Desert",
        "group": "pakistan-deep-dive", "paper_num": 4,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["poisson_rate", "bayesian_rate", "bootstrap_ci", "rate_ratio", "permutation_test"],
        "charts": _charts([15, 0, 2, 7, 3, 9, 14, 6]),
        "context": "Balochistan is Pakistan's largest province by area but smallest by trial count — its 14 million people have fewer clinical trials than a single hospital in Lahore, reflecting extreme infrastructure deprivation.",
        "refs": [REF_DRAP, REF_CTGOV]
    },
    {
        "slug": "islamabad-capital-advantage", "title": "Islamabad Capital Advantage",
        "group": "pakistan-deep-dive", "paper_num": 5,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["rate_ratio", "bootstrap_ci", "poisson_rate", "hhi_index", "concentration_index"],
        "charts": _charts([15, 0, 2, 7, 6, 9, 3, 11]),
        "context": "Islamabad's status as federal capital concentrates PIMS, NIH, and DRAP headquarters, giving it a trial density per capita that vastly exceeds any other region of Pakistan.",
        "refs": [REF_DRAP, REF_CTGOV]
    },
    {
        "slug": "gilgit-baltistan-ajk", "title": "Gilgit-Baltistan & AJK",
        "group": "pakistan-deep-dive", "paper_num": 6,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["poisson_rate", "bayesian_rate", "bootstrap_ci", "rate_ratio", "shannon_entropy"],
        "charts": _charts([15, 0, 2, 3, 7, 9, 14, 6]),
        "context": "Gilgit-Baltistan and Azad Jammu & Kashmir have combined populations exceeding 5 million but near-zero trial registrations, reflecting their disputed political status and extreme geographic isolation.",
        "refs": [REF_DRAP, REF_CTGOV]
    },
    {
        "slug": "provincial-per-capita-trial-inequality", "title": "Provincial Per-Capita Trial Inequality",
        "group": "pakistan-deep-dive", "paper_num": 7,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["gini_coefficient", "theil_index", "bootstrap_ci", "atkinson_index", "lorenz_area"],
        "charts": _charts([15, 1, 0, 7, 4, 9, 3, 11]),
        "context": "Per-capita trial rates across Pakistan's provinces reveal inequality ratios exceeding 50:1 between Islamabad and Balochistan, a disparity that mirrors and reinforces broader development gaps.",
        "refs": [REF_DRAP, REF_CTGOV, REF_GBD]
    },
    {
        "slug": "provincial-health-budget-vs-trial-density", "title": "Provincial Health Budget vs Trial Density",
        "group": "pakistan-deep-dive", "paper_num": 8,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["spearman_correlation", "linear_regression", "bootstrap_ci", "rate_ratio", "gini_coefficient"],
        "charts": _charts([15, 10, 0, 6, 7, 9, 3, 1]),
        "context": "Provincial health budget allocation correlates with trial density, but the relationship is sublinear — doubling health spending does not double trial output, suggesting structural barriers beyond funding.",
        "refs": [REF_DRAP, REF_HEC, REF_CTGOV]
    },
    {
        "slug": "urban-rural-punjab-disparity", "title": "Urban-Rural Punjab Disparity",
        "group": "pakistan-deep-dive", "paper_num": 9,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["gini_coefficient", "lorenz_area", "bootstrap_ci", "chi_squared", "rate_ratio"],
        "charts": _charts([15, 1, 0, 3, 7, 9, 12, 6]),
        "context": "Even within Punjab — Pakistan's most trial-rich province — research concentrates in Lahore while the agricultural heartland of southern Punjab with 50 million people is a research desert.",
        "refs": [REF_DRAP, REF_CTGOV]
    },
    {
        "slug": "inter-provincial-trend-analysis", "title": "Inter-Provincial Trend Analysis",
        "group": "pakistan-deep-dive", "paper_num": 10,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["linear_regression", "bootstrap_ci", "spearman_correlation", "gini_coefficient", "theil_index"],
        "charts": _charts([15, 6, 0, 11, 7, 9, 1, 3]),
        "context": "Longitudinal analysis of inter-provincial trial trends reveals whether devolution of health to provinces after the 18th Amendment has increased or decreased geographic equity in research.",
        "refs": [REF_DRAP, REF_CTGOV, REF_HEC]
    },
]

# --- Institutional Concentration (papers 11-18) ---
PAK_INSTITUTIONAL = [
    {
        "slug": "aga-khan-university-hospital", "title": "Aga Khan University Hospital",
        "group": "pakistan-deep-dive", "paper_num": 11,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["hhi_index", "bootstrap_ci", "rate_ratio", "poisson_rate", "concentration_index"],
        "charts": _charts([15, 0, 2, 7, 6, 9, 5, 3]),
        "context": "AKUH anchors Pakistan's clinical trial infrastructure with international accreditation and research networks, but its private status means trial access is limited to patients who can afford its fees.",
        "refs": [REF_DRAP, REF_CTGOV]
    },
    {
        "slug": "ziauddin-university", "title": "Ziauddin University",
        "group": "pakistan-deep-dive", "paper_num": 12,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["rate_ratio", "bootstrap_ci", "poisson_rate", "network_centrality", "linear_regression"],
        "charts": _charts([15, 0, 5, 6, 7, 9, 3, 10]),
        "context": "Ziauddin University has emerged as Karachi's second major trial hub, but its research output remains a fraction of AKUH's, reflecting the challenge of building research culture in newer private institutions.",
        "refs": [REF_DRAP, REF_CTGOV]
    },
    {
        "slug": "military-hospital-network", "title": "Military Hospital Network",
        "group": "pakistan-deep-dive", "paper_num": 13,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["network_centrality", "bootstrap_ci", "hhi_index", "rate_ratio", "poisson_rate"],
        "charts": _charts([15, 5, 0, 7, 6, 9, 3, 4]),
        "context": "Pakistan's military hospital network — CMH, AFIP, AMC — controls significant clinical research infrastructure but operates with limited transparency and restricted population access.",
        "refs": [REF_DRAP, REF_CTGOV]
    },
    {
        "slug": "shaukat-khanum-cancer-network", "title": "Shaukat Khanum Cancer Network",
        "group": "pakistan-deep-dive", "paper_num": 14,
        "query": {"condition": "Cancer", "countries": ["Pakistan"]},
        "stats": ["rate_ratio", "bootstrap_ci", "poisson_rate", "hhi_index", "kaplan_meier_survival"],
        "charts": _charts([15, 14, 0, 2, 7, 9, 6, 3]),
        "context": "Shaukat Khanum Memorial Cancer Hospital dominates Pakistan's oncology trial landscape, but with only two campuses (Lahore, Peshawar), cancer trial access remains geographically restricted.",
        "refs": [REF_DRAP, REF_CTGOV]
    },
    {
        "slug": "public-sector-teaching-hospitals", "title": "Public Sector Teaching Hospitals",
        "group": "pakistan-deep-dive", "paper_num": 15,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["rate_ratio", "bootstrap_ci", "poisson_rate", "gini_coefficient", "chi_squared"],
        "charts": _charts([15, 0, 2, 7, 3, 9, 6, 4]),
        "context": "Public sector teaching hospitals like Mayo, JPMC, and Lady Reading serve the majority of Pakistan's population but host a minority of clinical trials due to infrastructure and bureaucratic barriers.",
        "refs": [REF_DRAP, REF_CTGOV, REF_HEC]
    },
    {
        "slug": "private-vs-public-trial-divide", "title": "Private vs Public Trial Divide",
        "group": "pakistan-deep-dive", "paper_num": 16,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["chi_squared", "odds_ratio", "bootstrap_ci", "rate_ratio", "gini_coefficient"],
        "charts": _charts([15, 7, 0, 2, 3, 9, 6, 11]),
        "context": "Private hospitals host the majority of Pakistan's industry-sponsored trials while public hospitals conduct most academic research, creating two parallel trial ecosystems with different quality standards.",
        "refs": [REF_DRAP, REF_CTGOV]
    },
    {
        "slug": "medical-college-research-output", "title": "Medical College Research Output",
        "group": "pakistan-deep-dive", "paper_num": 17,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["hhi_index", "gini_coefficient", "bootstrap_ci", "poisson_rate", "concentration_index"],
        "charts": _charts([15, 0, 1, 4, 7, 9, 6, 3]),
        "context": "Pakistan's 170+ medical colleges produce vastly unequal research output — the top 5 institutions generate more trials than the bottom 150 combined, reflecting resource concentration in elite institutions.",
        "refs": [REF_HEC, REF_CTGOV]
    },
    {
        "slug": "institutional-collaboration-networks", "title": "Institutional Collaboration Networks",
        "group": "pakistan-deep-dive", "paper_num": 18,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["network_centrality", "bootstrap_ci", "hhi_index", "shannon_entropy", "gini_coefficient"],
        "charts": _charts([5, 15, 0, 8, 4, 9, 7, 3]),
        "context": "Network analysis of institutional collaborations reveals a hub-and-spoke model centered on AKUH and KEMU, with most institutions operating as isolated research nodes rather than collaborative partners.",
        "refs": [REF_DRAP, REF_CTGOV, REF_HEC]
    },
]

# --- Disease-Specific Gaps (papers 19-30) ---
PAK_DISEASE = [
    {
        "slug": "pak-cardiovascular-disease", "title": "Cardiovascular Disease",
        "group": "pakistan-deep-dive", "paper_num": 19,
        "query": {"condition": "Cardiovascular Diseases", "countries": ["Pakistan"]},
        "stats": ["rate_ratio", "bootstrap_ci", "poisson_rate", "lorenz_area", "gini_coefficient"],
        "charts": _charts([15, 0, 1, 2, 6, 9, 3, 14]),
        "context": "Pakistan has one of the world's highest rates of premature cardiovascular death, yet CV trial investment is dwarfed by India's, and most Pakistani patients rely on evidence generated from Western populations.",
        "refs": [REF_GBD, REF_CTGOV, REF_DRAP]
    },
    {
        "slug": "pak-diabetes-tsunami", "title": "Diabetes Tsunami",
        "group": "pakistan-deep-dive", "paper_num": 20,
        "query": {"condition": "Diabetes", "countries": ["Pakistan"]},
        "stats": ["linear_regression", "bootstrap_ci", "rate_ratio", "poisson_rate", "spearman_correlation"],
        "charts": _charts([15, 6, 0, 10, 7, 9, 3, 2]),
        "context": "Pakistan has 33 million diabetes patients — the third highest globally — yet diabetes trial investment per patient is less than 1% of what European nations invest per diabetic person.",
        "refs": [REF_GBD, REF_DRAP, REF_CTGOV]
    },
    {
        "slug": "pak-hepatitis-c-epidemic", "title": "Hepatitis C Epidemic",
        "group": "pakistan-deep-dive", "paper_num": 21,
        "query": {"condition": "Hepatitis C", "countries": ["Pakistan"]},
        "stats": ["poisson_rate", "bootstrap_ci", "rate_ratio", "bayesian_rate", "kaplan_meier_survival"],
        "charts": _charts([15, 14, 0, 6, 7, 9, 2, 3]),
        "context": "Pakistan's hepatitis C prevalence of 5-8% is among the world's highest, driven by unsafe injection practices, yet the country is reliant on generic DAA trials designed elsewhere.",
        "refs": [REF_GBD, REF_DRAP, REF_CTGOV]
    },
    {
        "slug": "pak-hepatitis-b-burden", "title": "Hepatitis B Burden",
        "group": "pakistan-deep-dive", "paper_num": 22,
        "query": {"condition": "Hepatitis B", "countries": ["Pakistan"]},
        "stats": ["rate_ratio", "bootstrap_ci", "poisson_rate", "bayesian_rate", "lorenz_area"],
        "charts": _charts([15, 0, 1, 2, 6, 9, 7, 14]),
        "context": "Pakistan's hepatitis B burden of 7-9 million carriers is compounded by low vaccination coverage in rural areas, yet HBV cure trial infrastructure is virtually nonexistent in the country.",
        "refs": [REF_GBD, REF_DRAP, REF_CTGOV]
    },
    {
        "slug": "pak-tuberculosis", "title": "Tuberculosis",
        "group": "pakistan-deep-dive", "paper_num": 23,
        "query": {"condition": "Tuberculosis", "countries": ["Pakistan"]},
        "stats": ["bayesian_rate", "bootstrap_ci", "rate_ratio", "poisson_rate", "chi_squared"],
        "charts": _charts([15, 0, 2, 6, 7, 9, 4, 3]),
        "context": "Pakistan ranks fifth globally for TB burden with 600,000 new cases annually, yet MDR-TB trials are concentrated in India and South Africa, leaving Pakistan dependent on extrapolated evidence.",
        "refs": [REF_GBD, REF_CTGOV, REF_WHO]
    },
    {
        "slug": "pak-polio-eradication-last-mile", "title": "Polio Eradication Last Mile",
        "group": "pakistan-deep-dive", "paper_num": 24,
        "query": {"condition": "Polio", "countries": ["Pakistan"]},
        "stats": ["kaplan_meier_survival", "bootstrap_ci", "rate_ratio", "poisson_rate", "bayesian_rate"],
        "charts": _charts([15, 14, 0, 6, 7, 9, 2, 3]),
        "context": "Pakistan remains one of two polio-endemic countries, with transmission persisting in southern KPK and Balochistan — areas where operational research trials face security and access challenges.",
        "refs": [REF_WHO, REF_CTGOV, REF_DRAP]
    },
    {
        "slug": "pak-thalassemia-major", "title": "Thalassemia Major",
        "group": "pakistan-deep-dive", "paper_num": 25,
        "query": {"condition": "Thalassemia", "countries": ["Pakistan"]},
        "stats": ["rate_ratio", "bootstrap_ci", "poisson_rate", "bayesian_rate", "theil_index"],
        "charts": _charts([15, 0, 2, 7, 6, 9, 3, 1]),
        "context": "Pakistan has an estimated 100,000 transfusion-dependent thalassemia patients — the world's largest burden — yet gene therapy and novel chelation trials are concentrated in Europe and the US.",
        "refs": [REF_GBD, REF_DRAP, REF_CTGOV]
    },
    {
        "slug": "pak-dengue-outbreaks", "title": "Dengue Outbreaks",
        "group": "pakistan-deep-dive", "paper_num": 26,
        "query": {"condition": "Dengue", "countries": ["Pakistan"]},
        "stats": ["poisson_rate", "bootstrap_ci", "rate_ratio", "bayesian_rate", "spearman_correlation"],
        "charts": _charts([15, 6, 0, 2, 7, 9, 10, 3]),
        "context": "Pakistan's dengue outbreaks have intensified — Lahore 2011, Karachi 2022 — yet the country lacks sovereign dengue vaccine and therapeutic trial infrastructure.",
        "refs": [REF_GBD, REF_CTGOV, REF_DRAP]
    },
    {
        "slug": "pak-maternal-neonatal-health", "title": "Maternal & Neonatal Health",
        "group": "pakistan-deep-dive", "paper_num": 27,
        "query": {"condition": "Maternal Health OR Neonatal", "countries": ["Pakistan"]},
        "stats": ["rate_ratio", "lorenz_area", "bootstrap_ci", "poisson_rate", "gini_coefficient"],
        "charts": _charts([15, 1, 0, 2, 6, 9, 7, 14]),
        "context": "Pakistan's maternal mortality ratio of 186/100,000 and neonatal mortality of 42/1,000 are among SAARC's highest, yet obstetric and neonatal trial investment remains critically low.",
        "refs": [REF_GBD, REF_WHO, REF_CTGOV]
    },
    {
        "slug": "pak-mental-health-chasm", "title": "Mental Health Chasm",
        "group": "pakistan-deep-dive", "paper_num": 28,
        "query": {"condition": "Depression OR Mental Health", "countries": ["Pakistan"]},
        "stats": ["shannon_entropy", "rate_ratio", "bootstrap_ci", "lorenz_area", "chi_squared"],
        "charts": _charts([15, 1, 0, 3, 4, 9, 6, 12]),
        "context": "Pakistan has 0.19 psychiatrists per 100,000 people — one of the lowest ratios globally — and mental health trial investment reflects this systematic neglect of psychological wellbeing.",
        "refs": [REF_GBD, REF_CTGOV, REF_WHO]
    },
    {
        "slug": "pak-childhood-pneumonia-diarrhoea", "title": "Childhood Pneumonia & Diarrhoea",
        "group": "pakistan-deep-dive", "paper_num": 29,
        "query": {"condition": "Pneumonia OR Diarrhea", "countries": ["Pakistan"]},
        "stats": ["poisson_rate", "rate_ratio", "bootstrap_ci", "bayesian_rate", "morans_i"],
        "charts": _charts([15, 0, 2, 6, 7, 9, 14, 3]),
        "context": "Pneumonia and diarrhea together kill over 150,000 Pakistani children annually, yet the trial pipeline for community-based IMNCI interventions adapted to Pakistan's health system is insufficient.",
        "refs": [REF_GBD, REF_CTGOV, REF_WHO]
    },
    {
        "slug": "pak-oral-cancer-naswar-gutka", "title": "Oral Cancer & Naswar/Gutka",
        "group": "pakistan-deep-dive", "paper_num": 30,
        "query": {"condition": "Oral Cancer", "countries": ["Pakistan"]},
        "stats": ["rate_ratio", "bootstrap_ci", "odds_ratio", "poisson_rate", "chi_squared"],
        "charts": _charts([15, 0, 2, 7, 3, 9, 6, 13]),
        "context": "Pakistan has among the world's highest oral cancer rates, driven by naswar and gutka use, yet prevention and treatment trials for smokeless tobacco-related cancers are virtually nonexistent.",
        "refs": [REF_GBD, REF_DRAP, REF_CTGOV]
    },
]

# --- Sponsor & Sovereignty (papers 31-38) ---
PAK_SPONSOR = [
    {
        "slug": "pak-foreign-sponsor-map", "title": "Foreign Sponsor Map",
        "group": "pakistan-deep-dive", "paper_num": 31,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["hhi_index", "network_centrality", "bootstrap_ci", "gini_coefficient", "theil_index"],
        "charts": _charts([15, 5, 8, 0, 7, 9, 6, 4]),
        "context": "Foreign pharmaceutical companies from the US, EU, and China dominate Pakistan's trial sponsorship landscape, using the country's large treatment-naive populations for pivotal Phase III trials.",
        "refs": [REF_DRAIN, REF_DRAP, REF_CTGOV]
    },
    {
        "slug": "pak-drap-regulatory-timeline", "title": "DRAP Regulatory Timeline",
        "group": "pakistan-deep-dive", "paper_num": 32,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["kaplan_meier_survival", "bootstrap_ci", "linear_regression", "rate_ratio", "poisson_rate"],
        "charts": _charts([15, 14, 6, 0, 7, 9, 3, 2]),
        "context": "DRAP's clinical trial approval process has evolved since the agency's 2012 establishment, but regulatory timelines remain longer than competitors like India's CDSCO, affecting Pakistan's attractiveness to sponsors.",
        "refs": [REF_DRAP, REF_CTGOV]
    },
    {
        "slug": "pak-pharma-industry-presence", "title": "Pharma Industry Presence",
        "group": "pakistan-deep-dive", "paper_num": 33,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["hhi_index", "bootstrap_ci", "network_centrality", "gini_coefficient", "concentration_index"],
        "charts": _charts([15, 5, 0, 4, 7, 9, 8, 3]),
        "context": "Pakistan's pharmaceutical industry — 700+ companies — is the largest in SAARC after India, yet local pharma sponsors fewer than 15% of clinical trials, preferring manufacturing over innovation.",
        "refs": [REF_DRAP, REF_CTGOV]
    },
    {
        "slug": "pak-academic-vs-industry-ratio", "title": "Academic vs Industry Ratio",
        "group": "pakistan-deep-dive", "paper_num": 34,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["chi_squared", "rate_ratio", "bootstrap_ci", "odds_ratio", "gini_coefficient"],
        "charts": _charts([15, 7, 0, 2, 3, 9, 6, 11]),
        "context": "The academic-to-industry trial ratio in Pakistan reveals a research ecosystem where industry sets the agenda, leaving gaps in public health research that academic institutions cannot fill alone.",
        "refs": [REF_DRAP, REF_HEC, REF_CTGOV]
    },
    {
        "slug": "pak-data-repatriation", "title": "Data Repatriation",
        "group": "pakistan-deep-dive", "paper_num": 35,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["chi_squared", "bootstrap_ci", "rate_ratio", "network_centrality", "shannon_entropy"],
        "charts": _charts([15, 5, 0, 8, 7, 9, 6, 4]),
        "context": "Clinical trial data generated from Pakistani populations frequently flows to sponsor headquarters abroad without local data retention, creating a data sovereignty deficit with long-term capacity implications.",
        "refs": [REF_HEDT, REF_DRAP, REF_CTGOV]
    },
    {
        "slug": "pak-post-trial-drug-access", "title": "Post-Trial Drug Access",
        "group": "pakistan-deep-dive", "paper_num": 36,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["kaplan_meier_survival", "bootstrap_ci", "rate_ratio", "chi_squared", "bayesian_rate"],
        "charts": _charts([15, 14, 0, 2, 6, 9, 7, 3]),
        "context": "Post-trial drug access provisions in Pakistan are weakly enforced, leaving participants who contributed to proving a drug's efficacy without access to the approved treatment they helped develop.",
        "refs": [REF_DRAP, REF_LANG, REF_CTGOV]
    },
    {
        "slug": "pak-generic-drug-trial-pipeline", "title": "Generic Drug Trial Pipeline",
        "group": "pakistan-deep-dive", "paper_num": 37,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["rate_ratio", "bootstrap_ci", "poisson_rate", "linear_regression", "bayesian_rate"],
        "charts": _charts([15, 6, 0, 2, 7, 9, 3, 10]),
        "context": "Pakistan's generic pharmaceutical industry could serve as a trial platform for affordable medicine development, but bioequivalence study quality varies and international recognition remains limited.",
        "refs": [REF_DRAP, REF_CTGOV]
    },
    {
        "slug": "pak-hec-research-funding", "title": "HEC Research Funding",
        "group": "pakistan-deep-dive", "paper_num": 38,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["linear_regression", "bootstrap_ci", "spearman_correlation", "rate_ratio", "gini_coefficient"],
        "charts": _charts([15, 6, 10, 0, 7, 9, 1, 3]),
        "context": "HEC's research funding for clinical trials has fluctuated with political changes, and the total budget for health research is a fraction of what peer nations like Turkey and Iran invest.",
        "refs": [REF_HEC, REF_CTGOV]
    },
]

# --- Workforce & Methods (papers 39-45) ---
PAK_WORKFORCE = [
    {
        "slug": "pak-pi-gender-distribution", "title": "PI Gender Distribution",
        "group": "pakistan-deep-dive", "paper_num": 39,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["odds_ratio", "bootstrap_ci", "chi_squared", "rate_ratio", "linear_regression"],
        "charts": _charts([15, 2, 0, 6, 11, 9, 3, 7]),
        "context": "Female medical graduates now outnumber males in Pakistan, yet female PI leadership in clinical trials remains under 15%, reflecting structural barriers in career progression and institutional culture.",
        "refs": [REF_HEDT, REF_DRAP, REF_CTGOV]
    },
    {
        "slug": "pak-trial-completion-rate", "title": "Trial Completion Rate",
        "group": "pakistan-deep-dive", "paper_num": 40,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["kaplan_meier_survival", "bootstrap_ci", "rate_ratio", "linear_regression", "bayesian_rate"],
        "charts": _charts([15, 14, 0, 6, 7, 9, 3, 2]),
        "context": "Pakistan's trial completion rate trails the global average, with early termination driven by recruitment failures, funding gaps, and political instability affecting site operations.",
        "refs": [REF_DRAP, REF_CTGOV]
    },
    {
        "slug": "pak-registration-quality-audit", "title": "Registration Quality Audit",
        "group": "pakistan-deep-dive", "paper_num": 41,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["chi_squared", "bootstrap_ci", "rate_ratio", "shannon_entropy", "poisson_rate"],
        "charts": _charts([15, 4, 0, 7, 9, 6, 13, 3]),
        "context": "Trial registration quality on ClinicalTrials.gov for Pakistan-based trials reveals high rates of missing primary outcomes, inconsistent enrollment data, and delayed results posting.",
        "refs": [REF_CHAN, REF_CTGOV]
    },
    {
        "slug": "pak-phase-distribution", "title": "Phase Distribution",
        "group": "pakistan-deep-dive", "paper_num": 42,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["chi_squared", "bootstrap_ci", "rate_ratio", "kl_divergence", "shannon_entropy"],
        "charts": _charts([15, 7, 0, 2, 3, 9, 6, 4]),
        "context": "Pakistan's trial portfolio is dominated by Phase III and IV studies, with minimal Phase I/II early discovery — reflecting its role as a late-stage testing market rather than an innovation center.",
        "refs": [REF_DRAP, REF_CTGOV]
    },
    {
        "slug": "pak-endpoint-appropriateness", "title": "Endpoint Appropriateness",
        "group": "pakistan-deep-dive", "paper_num": 43,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["shannon_entropy", "hhi_index", "bootstrap_ci", "chi_squared", "rate_ratio"],
        "charts": _charts([15, 4, 0, 9, 7, 6, 3, 12]),
        "context": "Endpoint selection in Pakistan trials often imports Western-validated measures without cultural adaptation, raising questions about whether outcomes measured are meaningful to Pakistani patients.",
        "refs": [REF_CHAN, REF_DRAP, REF_CTGOV]
    },
    {
        "slug": "pak-sample-size-trends", "title": "Sample Size Trends",
        "group": "pakistan-deep-dive", "paper_num": 44,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["linear_regression", "bootstrap_ci", "rate_ratio", "poisson_rate", "spearman_correlation"],
        "charts": _charts([15, 6, 0, 10, 7, 9, 3, 13]),
        "context": "Sample size trends in Pakistani trials reveal a bimodal distribution — large multinational Phase III trials alongside underpowered academic studies — with few trials in the optimal middle range.",
        "refs": [REF_CHAN, REF_CTGOV]
    },
    {
        "slug": "pak-statistical-methods-reporting", "title": "Statistical Methods Reporting",
        "group": "pakistan-deep-dive", "paper_num": 45,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["chi_squared", "bootstrap_ci", "rate_ratio", "shannon_entropy", "bayesian_rate"],
        "charts": _charts([15, 4, 0, 9, 7, 6, 3, 11]),
        "context": "Statistical methods reporting in Pakistani trials frequently lacks detail on sample size justification, multiplicity adjustment, and missing data handling — deficiencies that undermine reproducibility.",
        "refs": [REF_CHAN, REF_DRAP, REF_CTGOV]
    },
]

# --- Karachi Lens (papers 46-50) ---
PAK_KARACHI = [
    {
        "slug": "karachi-trial-density-map", "title": "Karachi Trial Density Map",
        "group": "pakistan-deep-dive", "paper_num": 46,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["hhi_index", "gini_coefficient", "bootstrap_ci", "morans_i", "concentration_index"],
        "charts": _charts([15, 0, 1, 4, 7, 9, 3, 10]),
        "context": "Karachi — Pakistan's largest city with 16 million people — concentrates the majority of Sindh's trials in a handful of neighborhoods near major hospitals, creating micro-level geographic inequity.",
        "refs": [REF_DRAP, REF_CTGOV]
    },
    {
        "slug": "karachi-disease-burden-match", "title": "Karachi Disease Burden Match",
        "group": "pakistan-deep-dive", "paper_num": 47,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["spearman_correlation", "kl_divergence", "bootstrap_ci", "shannon_entropy", "gini_coefficient"],
        "charts": _charts([15, 9, 0, 4, 10, 6, 1, 7]),
        "context": "Karachi's trial portfolio reflects sponsor interests more than the city's disease burden — with overrepresentation of diabetes and CV trials for export markets and underrepresentation of dengue and TB.",
        "refs": [REF_GBD, REF_DRAP, REF_CTGOV]
    },
    {
        "slug": "ziauddin-vs-aga-khan-vs-dow", "title": "Ziauddin vs Aga Khan vs Dow",
        "group": "pakistan-deep-dive", "paper_num": 48,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["chi_squared", "rate_ratio", "bootstrap_ci", "hhi_index", "network_centrality"],
        "charts": _charts([15, 5, 0, 2, 7, 9, 4, 3]),
        "context": "The three-way comparison between Ziauddin, Aga Khan, and Dow universities reveals distinct research profiles — AKUH leads in international trials, Dow in public health research, Ziauddin in pharmaceutical partnerships.",
        "refs": [REF_DRAP, REF_CTGOV]
    },
    {
        "slug": "karachi-global-trial-share", "title": "Karachi's Global Trial Share",
        "group": "pakistan-deep-dive", "paper_num": 49,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["rate_ratio", "bootstrap_ci", "poisson_rate", "concentration_index", "linear_regression"],
        "charts": _charts([15, 0, 10, 6, 7, 9, 3, 11]),
        "context": "Karachi's global trial share relative to its population reveals a city that punches below its demographic weight, hosting fewer trials per capita than Mumbai, Bangkok, or Cairo despite comparable size.",
        "refs": [REF_DRAIN, REF_CTGOV]
    },
    {
        "slug": "karachi-recruitment-velocity", "title": "Karachi Recruitment Velocity",
        "group": "pakistan-deep-dive", "paper_num": 50,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["linear_regression", "bootstrap_ci", "rate_ratio", "poisson_rate", "kaplan_meier_survival"],
        "charts": _charts([15, 14, 6, 0, 7, 9, 10, 3]),
        "context": "Karachi's recruitment velocity — patients per site per month — is competitive for some therapeutic areas but hampered by transport challenges, security concerns, and the city's fragmented healthcare geography.",
        "refs": [REF_DRAIN, REF_DRAP, REF_CTGOV]
    },
]

# ═══════════════════════════════════════════════════════════
#  COMBINED PAKISTAN DEEP-DIVE
# ═══════════════════════════════════════════════════════════
PAKISTAN_PAPERS = PAK_PROVINCIAL + PAK_INSTITUTIONAL + PAK_DISEASE + PAK_SPONSOR + PAK_WORKFORCE + PAK_KARACHI

# ═══════════════════════════════════════════════════════════
#  COMBINED MANIFEST
# ═══════════════════════════════════════════════════════════
MANIFEST = GEO_PAPERS + HEALTH_PAPERS + GOV_PAPERS + METHODS_PAPERS + PAKISTAN_PAPERS
PAPERS = MANIFEST  # Alias for build.py compatibility

# Validation
assert len(MANIFEST) == 190, f"Expected 190 papers, got {len(MANIFEST)}"
assert len(GEO_PAPERS) == 35, f"Expected 35 geo papers, got {len(GEO_PAPERS)}"
assert len(HEALTH_PAPERS) == 35, f"Expected 35 health papers, got {len(HEALTH_PAPERS)}"
assert len(GOV_PAPERS) == 35, f"Expected 35 gov papers, got {len(GOV_PAPERS)}"
assert len(METHODS_PAPERS) == 35, f"Expected 35 methods papers, got {len(METHODS_PAPERS)}"
assert len(PAKISTAN_PAPERS) == 50, f"Expected 50 pakistan papers, got {len(PAKISTAN_PAPERS)}"
assert len(set(p["slug"] for p in MANIFEST)) == 190, "Duplicate slugs found!"
