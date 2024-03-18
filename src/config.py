# Set Global File Path variables
import os
import os.path as path


ROOT =  path.abspath(path.join(__file__ ,"../.."))

# DIRECTORY PATHS
# ROOT = ".."
REPORTS = f"{ROOT}/report"
DATA = f"{ROOT}/data"
ASSETS = f"{ROOT}/global_assets"
INFO = f"{DATA}/info"
IMAGES = f"images"

# PLOTS HOSTING READ HTML
PLOTS_ROOT = "./assets/components"

# LOGOS HOSTING READ HTML
LOGOS_ROOT = "./assets/logos"

# TILE AREA in m2
TILE_AREA = 0.173

COVER_TARGET=0.15
SURIVORSHIP_TARGET=95
RUGOSITY_TARGET=0.4

# DATE FORMAT
DATE_STR_FORMAT = "%d/%m/%Y"
# RESULTS
RESULTS = f"{DATA}/results"

# DATASETS
REEFCHECK_DATA = f"{DATA}/reefcheck"
REEFOPS_DATA = f"{DATA}/reefops"
REEFSFM_DATA = f"{DATA}/reefsfm"

CORAL_METRICS_DB=f"{REEFSFM_DATA}/reefsfm_db_coral_metrics.csv"
REEF_METRICS_DB=f"{REEFSFM_DATA}/reefsfm_db_reef_metrics.csv"

# PLOTS
COMMUNITY_WRITE_OUTPUT = f"{REPORTS}/build_v2.0/{PLOTS_ROOT}/charts/community_comparison.html"
COMMUNITY_READ_HTML = f"{PLOTS_ROOT}/charts/community_comparison.html"
INDICATOR_PROP_WRITE_OUTPUT = f"{REPORTS}/build_v2.0/{PLOTS_ROOT}/charts/indicator_proportion.html"
INDICATOR_PROP_READ_HTML = f"{PLOTS_ROOT}/charts/indicator_proportion.html"
MAP_WRITE_OUTPUT = f"{REPORTS}/build_v2.0/{PLOTS_ROOT}/maps/map.html"
MAP_READ_HTML = f"{PLOTS_ROOT}/maps/map.html"
CORAL_MAP_READ_HTML = f"{PLOTS_ROOT}/maps/coral_map.html"
CORAL_COVER_WRITE_OUTPUT = f"{REPORTS}/build_v2.0/{PLOTS_ROOT}/charts/coral_projection.html"
CORAL_COVER_READ_HTML = f"{PLOTS_ROOT}/charts/coral_projection.html"
COMPOSITION_WRITE_OUTPUT = f"{REPORTS}/build_v2.0/{PLOTS_ROOT}/charts/composition.html"
COMPOSITION_READ_HTML = f"{PLOTS_ROOT}/charts/composition.html"
SURVIVORSHIP_WRITE_OUTPUT = f"{REPORTS}/build_v2.0/{PLOTS_ROOT}/charts/survivorship.html"
SURVIVORSHIP_READ_HTML = f"{PLOTS_ROOT}/charts/survivorship.html"

# IMAGES
ICON = f"{ROOT}/report/global_assets/images/ar_logo.png"
CLIENT_LOGO = f"{LOGOS_ROOT}/ADQ_logo.svg"
ARCHIREEF_LOGO = f"{LOGOS_ROOT}/ARF_logo.svg"
ASSET_IMAGES = f"{ASSETS}/images/"

agents = dict(
    JW="Jane Wong",
    VY="Vriko Yu",
    LZ="Lamisse Zerrouki",
    MY="Mohammad Younes",
    DT="Deniz Tekerek",
    JD="Juan Diego",
    DB="David Baker",
    HW="Haykey Wong",
    OW="Olivia Wu"

)

# SET GLOBAL COLOR PALETTE
COLORS = ['#0B4B7A', "#D4D5D6", "#B6C9D7", "#FBCD6F", "#FBCD6F", "#C8E0E0", "#E5EAF4", "#E1C3B7", "#85A5BC", "#BFBFC2"]
PATTERNS = ["", "/", "", "", "/", "", "", "", "", ""]

BAR_PLOT_LAYOUT = dict(
    margin=dict(
        l=10,
        r=0,
        b=0,
        t=0,
        pad=2
    ),
    font=dict(size=20),
    font_family="Lexend",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
    hoverlabel=dict(
        font_size=16,
        font_family="Lexend"
    )

)

SPECIES = [
    {
        "species": "Chaetodontidae",
        "common_name": "Butterfly Fish",
        "type": "Fish",
        "present": False,
        "count": 0
    },
    {
        "species": "Serranidae",
        "common_name": "Grouper",
        "type": "Fish",
        "present": False,
        "count": 0
    },
    {
        "species": "Muraenidae",
        "common_name": "Moray eel",
        "type": "Fish",
        "present": False,
        "count": 0
    },
    {
        "species": "Scaridae",
        "common_name": "Parrotfish",
        "type": "Fish",
        "present": False,
        "count": 0
    },
    {
        "species": "Lutjanidae",
        "common_name": "Snapper",
        "type": "Fish",
        "present": False,
        "count": 0
    },
    {
        "species": "Haemulidae",
        "common_name": "Sweetlips",
        "type": "Fish",
        "present": False,
        "count": 0
    },
    {
        "species": "Stenopus hispidus",
        "common_name": "Banded coral shrimp",
        "type": "Invert",
        "present": False,
        "count": 0
    },
    {
        "species": "Malacostraca",
        "common_name": "Lobster",
        "type": "Invert",
        "present": False,
        "count": 0
    },
    {
        "species": "Diadema spp.",
        "common_name": "Long-spined black sea urchins",
        "type": "Invert",
        "present": True,
        "count": 67
    },
    {
        "species": "Tripneustes spp.",
        "common_name": "Collector Urchin",
        "type": "Invert",
        "present": False,
        "count": 0
    },
    {
        "species": "Chromileptes altivelis",
        "common_name": "Barrimundi Cod",
        "type": "Fish",
        "present": False,
        "count": 0
    },
    {
        "species": "Bolbometopon muricatum",
        "common_name": "Bumphead Parrotfish",
        "type": "Fish",
        "present": False,
        "count": 0
    },
    {
        "species": "Cheilinus undulatus",
        "common_name": "Humphead Wrasse",
        "type": "Fish",
        "present": False,
        "count": 0
    },
    {
        "species": "Acanthaster planci",
        "common_name": "Crown-of-thorns starfish",
        "type": "Invert",
        "present": False,
        "count": 0
    },
    {
        "species": "Holothuria edulis",
        "common_name": "Pinkfish",
        "type": "Invert",
        "present": False,
        "count": 0
    },
    {
        "species": "Stichopus chloronotus",
        "common_name": "Greenfish",
        "type": "Invert",
        "present": False,
        "count": 0
    },
    {
        "species": "Thelenota ananas",
        "common_name": "Prickly Redfish",
        "type": "Invert",
        "present": False,
        "count": 0
    },
    {
        "species": "Tridacna spp.",
        "common_name": "Giant clams",
        "type": "Invert",
        "present": False,
        "count": 0
    },
    {
        "species": "Heterocentrotus mammilatus",
        "common_name": "Pencil urchin ",
        "type": "Invert",
        "present": False,
        "count": 0
    },
    {
        "species": "Charonia tritonis",
        "common_name": "Triton shell",
        "type": "Invert",
        "present": False,
        "count": 0
    },
    {
        "species": "Chaetodon melapterus",
        "common_name": "Arabian butterflyfish",
        "type": "Fish",
        "present": False,
        "count": 0
    },
    {
        "species": "Chromileptes altivelis",
        "common_name": "Barrimundi cod",
        "type": "Fish",
        "present": False,
        "count": 0
    },
    {
        "species": "Plectorhinchus gaterinus",
        "common_name": "Black spotted grunt ",
        "type": "Fish",
        "present": False,
        "count": 0
    },
    {
        "species": "Chaetodon nigropunctatus",
        "common_name": "Dark butterflyfish",
        "type": "Fish",
        "present": False,
        "count": 0
    },
    {
        "species": "Plectorhinchus sordidus",
        "common_name": "Grey grunt",
        "type": "Fish",
        "present": False,
        "count": 0
    },
    {
        "species": "Heniochus acuminatus",
        "common_name": "Longfin bannerfish ",
        "type": "Fish",
        "present": False,
        "count": 0
    },
    {
        "species": "Epinephelus coioides",
        "common_name": "Orange-spotted grouper",
        "type": "Fish",
        "present": True,
        "count": 5
    },
    {
        "species": "Plectorhinchus pictus",
        "common_name": "Spotted grunt",
        "type": "Fish",
        "present": True,
        "count": 20
    },
    {
        "species": "Echinothrix diadema",
        "common_name": "Black urchin",
        "type": "Invert",
        "present": True,
        "count": 124
    },
    {
        "species": "Cypraeidae",
        "common_name": "Cowries",
        "type": "Invert",
        "present": False,
        "count": 0
    },
    {
        "species": "Acanthaster planci",
        "common_name": "Crown-of-thorns starfish",
        "type": "Invert",
        "present": False,
        "count": 0
    },
    {
        "species": "Heterocentrotus mammilatus",
        "common_name": "Pencil urchin",
        "type": "Invert",
        "present": False,
        "count": 0
    },
    {
        "species": "Holothuroidea",
        "common_name": "Sea cucumber ",
        "type": "Invert",
        "present": True,
        "count": 30
    },
    {
        "species": "Echinometra mathaei",
        "common_name": "Short spine urchin",
        "type": "Invert",
        "present": False,
        "count": 0
    }
]
