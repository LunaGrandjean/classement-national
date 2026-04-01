import streamlit as st
import pandas as pd
import numpy as np
import base64
from pathlib import Path

# MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(page_title="Classement FFTir", layout="wide")

LOGO_PATH = "FFTir_Logo.svg"
CSV_PATH = "data_classement.csv"

# CSS THEME + WATERMARK + TRICOLOR + PODIUM
def inject_css_with_watermark(svg_path: str):
    svg_file = Path(svg_path)
    watermark_css = ""

    if svg_file.exists():
        svg = svg_file.read_text(encoding="utf-8")
        b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
        watermark_css = f"""
        .stApp {{
          background-image:
            linear-gradient(rgba(246, 247, 251, 0.86), rgba(246, 247, 251, 0.86)),
            url("data:image/svg+xml;base64,{b64}");
          background-repeat: no-repeat, no-repeat;
          background-position: center, center 110px;
          background-size: cover, min(900px, 78vw);
          background-attachment: scroll, fixed;
        }}
        """

    st.markdown(
        f"""
        <style>
          :root {{
            --ff-blue: #0055A4;
            --ff-red: #EF4135;
            --ff-ink: #0f172a;
            --ff-muted: #64748b;
            --ff-border: rgba(15, 23, 42, 0.12);
            --ff-bg: #f6f7fb;
            --ff-blueSoft: rgba(0,85,164,0.12);
            --ff-redSoft: rgba(239,65,53,0.10);
          }}

          .stApp::after {{
            content: "";
            position: fixed;
            top: 0; left: 0;
            width: 100%;
            height: 7px;
            background: linear-gradient(90deg, var(--ff-blue), #ffffff 50%, var(--ff-red));
            z-index: 3;
          }}

          .stApp {{ background: var(--ff-bg); }}
          {watermark_css}

          .block-container {{
            padding-top: 1.1rem;
            padding-bottom: 2rem;
          }}

          section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #ffffff, rgba(0,85,164,0.04));
            border-right: 1px solid var(--ff-border);
            position: relative;
          }}
          section[data-testid="stSidebar"]::after {{
            content: "";
            position: absolute;
            left: 0; top: 0;
            width: 6px; height: 100%;
            background: linear-gradient(to bottom, var(--ff-blue), #ffffff, var(--ff-red));
          }}
          section[data-testid="stSidebar"] h2,
          section[data-testid="stSidebar"] h3 {{
            color: var(--ff-blue);
          }}

          .ff-title {{
            font-size: 38px;
            font-weight: 900;
            letter-spacing: -0.6px;
            margin: 0;
            color: var(--ff-ink);
          }}

          .ff-card {{
            background: linear-gradient(135deg, rgba(255,255,255,0.92), rgba(0,85,164,0.05));
            border: 1px solid var(--ff-border);
            border-radius: 18px;
            padding: 18px;
            box-shadow: 0 12px 32px rgba(2, 6, 23, 0.08);
            position: relative;
            overflow: hidden;
          }}
          .ff-card::before {{
            content: "";
            position: absolute;
            left: 0; top: 0;
            height: 5px; width: 100%;
            background: linear-gradient(90deg, var(--ff-blue), #ffffff, var(--ff-red));
          }}

          .podium {{
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 14px;
            margin-bottom: 8px;
          }}
          .podium-card {{
            background: linear-gradient(135deg, rgba(255,255,255,0.92), rgba(239,65,53,0.05));
            border: 1px solid var(--ff-border);
            border-radius: 18px;
            padding: 14px;
            box-shadow: 0 12px 28px rgba(2, 6, 23, 0.07);
            position: relative;
            overflow: hidden;
          }}
          .podium-card::before {{
            content: "";
            position: absolute;
            left: 0; top: 0;
            height: 5px; width: 100%;
            background: linear-gradient(90deg, var(--ff-blue), #ffffff, var(--ff-red));
          }}
          .podium-medal {{ font-size: 28px; line-height: 1; }}
          .podium-name {{ font-weight: 900; color: var(--ff-ink); margin-top: 8px; font-size: 16px; }}
          .podium-meta {{ color: var(--ff-muted); font-size: 13px; margin-top: 4px; line-height: 1.35; }}
          @media (max-width: 900px) {{ .podium {{ grid-template-columns: 1fr; }} }}

          div[data-testid="stMarkdownContainer"] h2 {{ color: var(--ff-blue); }}

          div[data-testid="stDataFrame"] {{
            background: rgba(255,255,255,0.92);
            border: 1px solid var(--ff-border);
            border-radius: 18px;
            padding: 8px;
            box-shadow: 0 12px 28px rgba(2, 6, 23, 0.07);
          }}

          .stDownloadButton button, .stButton button {{
            border-radius: 14px !important;
            padding: 0.55rem 0.95rem !important;
            border: 1px solid rgba(0,85,164,0.28) !important;
            background: linear-gradient(90deg, var(--ff-blueSoft), rgba(255,255,255,0.6), var(--ff-redSoft)) !important;
          }}

          div[data-baseweb="select"] > div {{
            border-radius: 14px !important;
            border-color: rgba(0,85,164,0.22) !important;
          }}

          input[type="radio"] {{ accent-color: var(--ff-red); }}

          .stCaption {{ color: var(--ff-muted) !important; }}
        </style>
        """,
        unsafe_allow_html=True,
    )

inject_css_with_watermark(LOGO_PATH)

# HEADER
st.markdown('<p class="ff-title">FFTir – Classements & fiches athlètes</p>', unsafe_allow_html=True)
st.markdown(
    """
    <div style="
      display:inline-block;
      margin-top:6px;
      padding:7px 12px;
      border-radius:999px;
      border:1px solid rgba(15,23,42,0.12);
      background: linear-gradient(90deg, rgba(0,85,164,0.14), rgba(255,255,255,0.50), rgba(239,65,53,0.12));
      color:#334155;
      font-size:13px;
      font-weight:600;
    ">
      Classements par épreuve • filtres • catégories d’âge • fiches détaillées par athlète
    </div>
    """,
    unsafe_allow_html=True
)
st.write("")

# LOAD DATA
@st.cache_data
def load_data():
    try:
        df = pd.read_csv(CSV_PATH, sep=";", encoding="utf-8", low_memory=False)
    except UnicodeDecodeError:
        df = pd.read_csv(CSV_PATH, sep=";", encoding="cp1252", low_memory=False)
    return df

df = load_data()

# COLONNES
DISC_COL = "Epreuve"
GENDER_COL = "Civilité"
TOTAL_COL = "Total Séries"
LIC_COL = "Licence"
NOM_COL = "Nom"
PRENOM_COL = "Prenom"
DATE_COL = "Date de début"
COMP_COL = "Compétition"
AGE_CAT_COL = "Catégorie E"
COMP_TYPE_COL = "Type compétition"

# CLEAN
df[TOTAL_COL] = df[TOTAL_COL].astype(str).str.replace(",", ".", regex=False)
df[TOTAL_COL] = pd.to_numeric(df[TOTAL_COL], errors="coerce")
df[DATE_COL] = pd.to_datetime(df[DATE_COL], dayfirst=True, errors="coerce")

df[GENDER_COL] = df[GENDER_COL].astype(str).str.strip().str.upper()
df[GENDER_COL] = df[GENDER_COL].replace({"FEMME": "F", "HOMME": "M"})

if AGE_CAT_COL in df.columns:
    df[AGE_CAT_COL] = df[AGE_CAT_COL].astype(str).str.strip().str.upper()

df = df.dropna(subset=[TOTAL_COL, DISC_COL, NOM_COL, PRENOM_COL, GENDER_COL])

# =========================================================
# TYPE DE COMPÉTITION
# =========================================================
def normalize_text(s: str) -> str:
    s = str(s).upper().strip()
    replacements = {
        "É": "E", "È": "E", "Ê": "E", "Ë": "E",
        "À": "A", "Â": "A", "Ä": "A",
        "Î": "I", "Ï": "I",
        "Ô": "O", "Ö": "O",
        "Ù": "U", "Û": "U", "Ü": "U",
        "Ç": "C",
        "Œ": "OE",
        "’": "'", "–": "-", "—": "-"
    }
    for a, b in replacements.items():
        s = s.replace(a, b)
    return s

def classify_competition_type(comp_name: str) -> str:
    s = normalize_text(comp_name)

    if (
        "CHAMPIONNAT DE FRANCE" in s
        or "CHAMPIONNATS DE FRANCE" in s
        or "CDF" in s
    ):
        return "Championnat de France"

    if "REGION" in s or "LIGUE" in s or "REGIONAL" in s:
        return "Régional"

    if "DEPART" in s or "DEPARTEMENTAL" in s or "DEPARTEMENTAUX" in s:
        return "Départemental"

    if any(x in s for x in ["CHALLENGE", "CRITERIUM", "COUPE", "OPEN", "AMICAL", "TROPHEE", "TOURNOI"]):
        return "Challenge / Open"

    return "Autre"

df[COMP_COL] = df[COMP_COL].astype(str).str.strip()
df[COMP_TYPE_COL] = df[COMP_COL].apply(classify_competition_type)

# =========================================================
# EPREUVES A GARDER + NOMS NETTOYES
# =========================================================
def normalize_epreuve(ep: str) -> str | None:
    s = str(ep).upper().strip()

    # EXCLUSION DES FINALES
    if "APRES FINALE" in s or "APRÈS FINALE" in s:
        return None

    # ex: 100-F / 104-F
    code_prefix = s.split(" - ")[0].strip()
    if code_prefix.endswith("-F"):
        return None

    # DISCIPLINES

    # Carabine 10m
    if "CARABINE 10" in s and "ECOLES DE TIR" not in s and "HP -" not in s:
        return "Carabine 10m"

    # Carabine 3 positions
    if "CARABINE 50M 3 X 20" in s or "CARABINE 3 X 20" in s or "3X20" in s or "3 X 20" in s:
        return "Carabine 3 positions"

    # Pistolet 10m
    if "PISTOLET 10" in s and "VITESSE" not in s and "STANDARD" not in s and "ECOLES DE TIR" not in s and "HP -" not in s:
        return "Pistolet 10m"

    # Pistolet 25m femme
    if "PISTOLET 25" in s and "VITESSE" not in s and "STANDARD" not in s and "PERCUSSION" not in s and "HP -" not in s:
        return "Pistolet 25m femme"

    # VO 25m
    if "PISTOLET VITESSE 25" in s:
        return "VO 25m"

    # Skeet
    if "SKEET" in s:
        return "Skeet"

    # Fosse / Trap
    if "FOSSE" in s or "TRAP" in s:
        return "Fosse"

    return None

df["epreuve_clean"] = df[DISC_COL].apply(normalize_epreuve)
df = df[df["epreuve_clean"].notna()].copy()

# On remplace la colonne d'origine par le nom nettoyé
df[DISC_COL] = df["epreuve_clean"]

# =========================================================
# CATEGORIES D'AGE
# =========================================================
U16_CODES = {"BF", "BG", "MF", "MG", "PF", "PG"}
U18_CODES = {"CF", "CG"}
U21_CODES = {"JF", "JG"}
SENIOR_CODES = {"S1", "S2", "S3", "D1", "D2", "D3"}
MASTER_CODES = {"VA S", "VA D"}

def map_age_bucket(cat_e: str) -> str:
    c = str(cat_e).upper().strip()
    if c in U16_CODES:
        return "U16"
    if c in U18_CODES:
        return "U18"
    if c in U21_CODES:
        return "U21"
    if c in MASTER_CODES:
        return "Master"
    if c in SENIOR_CODES:
        return "Senior"
    return "Autres"

if AGE_CAT_COL in df.columns:
    df["cat_age"] = df[AGE_CAT_COL].apply(map_age_bucket)
else:
    df["cat_age"] = "Autres"

def make_cat_label(row) -> str:
    sex = row[GENDER_COL]
    bucket = row["cat_age"]
    if bucket in {"U16", "U18", "U21"}:
        return f"{bucket} {'Fille' if sex == 'F' else 'Garçon'}"
    if bucket == "Senior":
        return "Dame" if sex == "F" else "Senior"
    if bucket == "Master":
        return f"Master {'Femme' if sex == 'F' else 'Homme'}"
    return bucket

df["cat_label"] = df.apply(make_cat_label, axis=1)

# NAV
page = st.sidebar.radio("Navigation", ["Classement", "Athlète"], index=0)

# FILTRES GLOBAUX
with st.sidebar:
    st.header("Filtres globaux")

    # plus de "Toutes" pour l'épreuve
    epreuves = sorted(df[DISC_COL].unique().tolist())
    default_epreuve = epreuves[0] if epreuves else None
    epreuve_choice = st.selectbox("Épreuve", epreuves, index=0 if default_epreuve is not None else None)

    sex_choice = st.selectbox("Sexe", ["Tous", "F", "M"], index=0)

    age_options = ["U16", "U18", "U21", "Senior", "Master"]
    age_choices = st.multiselect(
        "Catégorie(s) d’âge",
        options=age_options,
        default=[]
    )

    comp_type_options = sorted(df[COMP_TYPE_COL].dropna().unique().tolist())
    comp_type_choices = st.multiselect(
        "Type(s) de compétition",
        options=comp_type_options,
        default=[]
    )

    competition_options = sorted(df[COMP_COL].dropna().unique().tolist())
    competition_choices = st.multiselect(
        "Compétition(s)",
        options=competition_options,
        default=[]
    )

    st.divider()
    st.subheader("Mode de classement")
    ranking_mode = st.selectbox(
        "Calcul",
        ["Classement national (basique)", "4 meilleurs", "Pondéré"],
        index=0
    )

    st.divider()
    st.subheader("Performance")
    fast_mode = st.toggle("Mode rapide", value=True)
    top_n = st.slider("Lignes à afficher", 50, 2000, 300, step=50)

base = df.copy()

if epreuve_choice:
    base = base[base[DISC_COL] == epreuve_choice]
if sex_choice != "Tous":
    base = base[base[GENDER_COL] == sex_choice]
if age_choices:
    base = base[base["cat_age"].isin(age_choices)]
if comp_type_choices:
    base = base[base[COMP_TYPE_COL].isin(comp_type_choices)]
if competition_choices:
    base = base[base[COMP_COL].isin(competition_choices)]

if age_choices:
    if len(age_choices) == 1:
        ranking_cat_label = age_choices[0]
    else:
        ranking_cat_label = " + ".join(age_choices)
else:
    ranking_cat_label = "Toutes catégories"

base = base.copy()
base["ranking_cat"] = ranking_cat_label

st.caption(f"{len(base):,} lignes après filtres globaux")

active_filters = []

if comp_type_choices:
    active_filters.append("Type compétition : " + ", ".join(comp_type_choices))

if competition_choices:
    preview = competition_choices[:3]
    txt = ", ".join(preview)
    if len(competition_choices) > 3:
        txt += f" ... (+{len(competition_choices)-3})"
    active_filters.append("Compétitions : " + txt)

if active_filters:
    st.caption(" • ".join(active_filters))

# HELPERS
def per_discipline_table(data: pd.DataFrame) -> pd.DataFrame:
    group_cols = [DISC_COL, "ranking_cat", NOM_COL, PRENOM_COL, GENDER_COL]
    return (
        data.groupby(group_cols, as_index=False)
            .agg(
                matchs=(TOTAL_COL, "count"),
                moyenne=(TOTAL_COL, "mean"),
                meilleur=(TOTAL_COL, "max"),
            )
    )

def per_discipline_table_athlete(data: pd.DataFrame) -> pd.DataFrame:
    group_cols = [DISC_COL, "cat_label", NOM_COL, PRENOM_COL, GENDER_COL]
    return (
        data.groupby(group_cols, as_index=False)
            .agg(
                matchs=(TOTAL_COL, "count"),
                moyenne=(TOTAL_COL, "mean"),
                meilleur=(TOTAL_COL, "max"),
            )
    )

@st.cache_data
def compute_ranking(data: pd.DataFrame) -> pd.DataFrame:
    r = per_discipline_table(data)
    r["moyenne"] = r["moyenne"].round(2)
    r["meilleur"] = r["meilleur"].round(2)
    r = r.sort_values(["moyenne", "meilleur"], ascending=False).reset_index(drop=True)
    r.insert(0, "Rang", np.arange(1, len(r) + 1))
    return r

def add_weight_coef(data: pd.DataFrame, window_months: int = 12, k: float = 0.3) -> pd.DataFrame:
    d = data.copy()
    d = d.dropna(subset=[DATE_COL]).copy()

    today = pd.Timestamp.today().normalize()
    d["delta_months"] = (
        (today.year - d[DATE_COL].dt.year) * 12
        + (today.month - d[DATE_COL].dt.month)
    )

    d = d[d["delta_months"] <= window_months].copy()

    if d.empty:
        return d

    delta = np.minimum(d["delta_months"], window_months)
    d["coef"] = 1 - np.exp(k * delta) / np.exp(k * window_months) + 1 / np.exp(k * window_months)
    return d

def compute_ranking_basique(data: pd.DataFrame) -> pd.DataFrame:
    r = per_discipline_table(data)
    r["moyenne"] = r["moyenne"].round(2)
    r["meilleur"] = r["meilleur"].round(2)
    r = r.sort_values(["moyenne", "meilleur"], ascending=False).reset_index(drop=True)
    r.insert(0, "Rang", np.arange(1, len(r) + 1))
    return r

def compute_ranking_top4(data: pd.DataFrame) -> pd.DataFrame:
    group_cols = [DISC_COL, "ranking_cat", NOM_COL, PRENOM_COL, GENDER_COL]

    top4 = (
        data.sort_values(group_cols + [TOTAL_COL], ascending=[True, True, True, True, True, False])
            .groupby(group_cols, as_index=False, group_keys=False)
            .head(4)
    )

    r = (
        top4.groupby(group_cols, as_index=False)
            .agg(
                matchs=(TOTAL_COL, "count"),
                moyenne=(TOTAL_COL, "mean"),
                meilleur=(TOTAL_COL, "max"),
            )
    )

    r["moyenne"] = r["moyenne"].round(2)
    r["meilleur"] = r["meilleur"].round(2)
    r = r.sort_values(["moyenne", "meilleur"], ascending=False).reset_index(drop=True)
    r.insert(0, "Rang", np.arange(1, len(r) + 1))
    return r

def compute_ranking_pondere(data: pd.DataFrame) -> pd.DataFrame:
    d = add_weight_coef(data, window_months=12, k=0.3)

    if d.empty:
        cols = ["Rang", DISC_COL, "ranking_cat", NOM_COL, PRENOM_COL, GENDER_COL, "matchs", "moyenne", "meilleur"]
        return pd.DataFrame(columns=cols)

    group_cols = [DISC_COL, "ranking_cat", NOM_COL, PRENOM_COL, GENDER_COL]

    r = (
        d.groupby(group_cols, as_index=False)
         .apply(lambda x: pd.Series({
             "matchs": x[TOTAL_COL].count(),
             "moyenne": (x[TOTAL_COL] * x["coef"]).sum() / x["coef"].sum(),
             "meilleur": x[TOTAL_COL].max()
         }))
         .reset_index(drop=True)
    )

    r["moyenne"] = r["moyenne"].round(2)
    r["meilleur"] = r["meilleur"].round(2)
    r = r.sort_values(["moyenne", "meilleur"], ascending=False).reset_index(drop=True)
    r.insert(0, "Rang", np.arange(1, len(r) + 1))
    return r

def compute_ranking_by_mode(data: pd.DataFrame, mode: str) -> pd.DataFrame:
    if mode == "4 meilleurs":
        return compute_ranking_top4(data)
    if mode == "Pondéré":
        return compute_ranking_pondere(data)
    return compute_ranking_basique(data)

def style_top3_only(df_show: pd.DataFrame):
    def row_style(i):
        if i == 0:
            return ["background: linear-gradient(90deg, rgba(0,85,164,0.25), rgba(255,255,255,0.90), rgba(239,65,53,0.18)); font-weight:800;"] * df_show.shape[1]
        if i == 1:
            return ["background: linear-gradient(90deg, rgba(0,85,164,0.18), rgba(255,255,255,0.92), rgba(239,65,53,0.12)); font-weight:750;"] * df_show.shape[1]
        if i == 2:
            return ["background: linear-gradient(90deg, rgba(0,85,164,0.12), rgba(255,255,255,0.94), rgba(239,65,53,0.10)); font-weight:700;"] * df_show.shape[1]
        return [""] * df_show.shape[1]

    return (
        df_show.style
        .apply(lambda row: row_style(row.name), axis=1)
        .set_table_styles([
            {"selector": "th", "props": [("background", "rgba(255,255,255,0.97)"),
                                        ("color", "#0f172a"),
                                        ("font-weight", "800"),
                                        ("border-bottom", "1px solid rgba(15,23,42,0.12)")]},
            {"selector": "td", "props": [("border-bottom", "1px solid rgba(15,23,42,0.08)")]},
        ])
    )

def add_rank_within_discipline(t: pd.DataFrame) -> pd.DataFrame:
    t = t.copy()
    t["moyenne"] = t["moyenne"].round(2)
    t["meilleur"] = t["meilleur"].round(2)
    t["rang_dans_cat"] = (
        t.groupby([DISC_COL, "cat_label"])["moyenne"]
         .rank(method="dense", ascending=False)
         .astype(int)
    )
    return t

# PAGE CLASSEMENT
if page == "Classement":
    ranking = compute_ranking_by_mode(base, ranking_mode)

    st.markdown("## Podium 🏅")
    top3 = ranking.head(3).copy()
    medals = ["🥇", "🥈", "🥉"]

    if len(top3) == 0:
        st.info("Aucun résultat avec ces filtres.")
    else:
        st.markdown('<div class="podium">', unsafe_allow_html=True)
        for i in range(len(top3)):
            row = top3.iloc[i]
            epreuve = str(row.get(DISC_COL, ""))
            cat = str(row.get("ranking_cat", ""))
            nom = f"{row.get(NOM_COL,'')} {row.get(PRENOM_COL,'')}"
            sexe = str(row.get(GENDER_COL, ""))
            moyenne = row.get("moyenne", "")
            meilleur = row.get("meilleur", "")

            st.markdown(
                f"""
                <div class="podium-card">
                  <div class="podium-medal">{medals[i]}</div>
                  <div class="podium-name">{nom}</div>
                  <div class="podium-meta">
                    {sexe} • <b>{cat}</b><br/>
                    <b>Moyenne</b> : {moyenne} • <b>Meilleur</b> : {meilleur}<br/>
                    <span style="color: var(--ff-blue); font-weight:800;">{epreuve}</span>
                  </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    st.markdown('<div class="ff-card">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Lignes (après filtres)", f"{len(base):,}")
    c2.metric("Athlètes", f"{base[[NOM_COL, PRENOM_COL]].drop_duplicates().shape[0]:,}")
    c3.metric("Épreuves", f"{base[DISC_COL].nunique():,}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")

    st.subheader(f"Classement – {ranking_mode}")

    table_df = ranking.rename(columns={
        DISC_COL: "Épreuve",
        "ranking_cat": "Catégorie",
        NOM_COL: "Nom",
        PRENOM_COL: "Prénom",
        GENDER_COL: "Sexe",
        "moyenne": "Moyenne (Total Séries)",
        "meilleur": "Meilleur score",
        "matchs": "Nb matchs"
    }).copy()

    table_view = table_df.head(top_n)

    if fast_mode:
        st.dataframe(table_view, use_container_width=True, hide_index=True)
    else:
        st.dataframe(style_top3_only(table_view), use_container_width=True, hide_index=True)

    st.download_button(
        "Télécharger le classement complet (CSV)",
        data=table_df.to_csv(index=False, sep=";", encoding="utf-8").encode("utf-8"),
        file_name="classement_fftir.csv",
        mime="text/csv"
    )

# PAGE ATHLÈTE
else:
    st.subheader("Fiche athlète")

    base = base.copy()
    base["athlete_key"] = (
        base[NOM_COL].astype(str) + " " + base[PRENOM_COL].astype(str)
    )
    athletes = sorted(base["athlete_key"].unique().tolist())

    if not athletes:
        st.warning("Aucun athlète avec les filtres actuels.")
        st.stop()

    st.markdown('<div class="ff-card">', unsafe_allow_html=True)
    athlete_choice = st.selectbox("Choisir un athlète", athletes)
    st.markdown('</div>', unsafe_allow_html=True)
    st.write("")

    ath = base[base["athlete_key"] == athlete_choice].copy()

    nom = ath[NOM_COL].iloc[0]
    prenom = ath[PRENOM_COL].iloc[0]
    sexe = ath[GENDER_COL].iloc[0]

    st.markdown('<div class="ff-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.metric("Athlète", f"{nom} {prenom}")
    c2.metric("Sexe", sexe)
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")

    cats_ath = sorted(ath["cat_label"].unique().tolist())
    cat_choice = st.selectbox("Catégorie", ["Toutes"] + cats_ath)

    epreuves_ath = sorted(ath[DISC_COL].unique().tolist())
    epreuve_ath_choice = st.selectbox("Voir l’épreuve", ["Toutes"] + epreuves_ath)

    ath_view = ath.copy()
    if cat_choice != "Toutes":
        ath_view = ath_view[ath_view["cat_label"] == cat_choice]
    if epreuve_ath_choice != "Toutes":
        ath_view = ath_view[ath_view[DISC_COL] == epreuve_ath_choice]

    st.markdown("### Résumé par épreuve & catégorie (avec rang)")

    all_avg = add_rank_within_discipline(per_discipline_table_athlete(base))

    ath_summary = all_avg[
        (all_avg[NOM_COL] == nom) &
        (all_avg[PRENOM_COL] == prenom)
    ].copy()

    if cat_choice != "Toutes":
        ath_summary = ath_summary[ath_summary["cat_label"] == cat_choice]
    if epreuve_ath_choice != "Toutes":
        ath_summary = ath_summary[ath_summary[DISC_COL] == epreuve_ath_choice]

    ath_summary = ath_summary.sort_values(["moyenne", "meilleur"], ascending=False)

    st.dataframe(
        ath_summary.rename(columns={
            DISC_COL: "Épreuve",
            "cat_label": "Catégorie",
            "matchs": "Nb matchs",
            "moyenne": "Moyenne",
            "meilleur": "Meilleur",
            "rang_dans_cat": "Rang (épreuve + cat.)"
        })[["Épreuve", "Catégorie", "Nb matchs", "Moyenne", "Meilleur", "Rang (épreuve + cat.)"]],
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### Détails des matchs")
    cols_detail = ["cat_label", COMP_COL, COMP_TYPE_COL, DATE_COL, DISC_COL, TOTAL_COL, "Nombre 10", "Nombre 9", "Nombre Mouches"]
    cols_detail = [c for c in cols_detail if c in ath_view.columns]

    detail = ath_view.sort_values(DATE_COL, ascending=False).copy()
    detail[TOTAL_COL] = detail[TOTAL_COL].round(2)

    st.dataframe(
        detail[cols_detail].rename(columns={
            "cat_label": "Catégorie",
            COMP_COL: "Compétition",
            COMP_TYPE_COL: "Type compétition",
            DATE_COL: "Date",
            DISC_COL: "Épreuve",
            TOTAL_COL: "Total Séries"
        }),
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Télécharger la fiche athlète (CSV)",
        data=detail.to_csv(index=False, sep=";", encoding="utf-8").encode("utf-8"),
        file_name=f"athlete_{nom}_{prenom}.csv",
        mime="text/csv"
    )
