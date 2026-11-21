import streamlit as st
import pandas as pd
import plotly.express as px

st.markdown("<h1 style ='text-align: center;'>Átlagos napi forgalom meghatározása", unsafe_allow_html=True,)

st.markdown("""<style>div[data-testid="stMetricValue"] {font-size: 30px !important;}</style>""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Átlagos napi forgalom bekérése", "Keresztmetszeti áteresztőképesség"])

if "szemelygepjarmu" not in st.session_state:
    st.session_state["szemelygepjarmu"] = 0.0
if "teher_osszesen" not in st.session_state:
    st.session_state["teher_osszesen"] = 0.0
if "osszes_zaras_min" not in st.session_state:
    st.session_state["osszes_zaras_min"] = 0.0
if "szemely_celevre" not in st.session_state:
    st.session_state["szemely_celevre"] = 0.0
if "zarvatartas_ptc" not in st.session_state:
    st.session_state["zarvatartas_ptc"] = 0.0
if "teher_celevre" not in st.session_state:
    st.session_state["teher_celevre"] = 0.0

celev = int(st.session_state.get("celev", 2026))
p_szemely_pct = float(st.session_state.get("p_szemely_pct", 1.5))
p_teher_pct = float(st.session_state.get("p_teher_pct", 1.5))

szemelygepjarmu = float(st.session_state.get("szemelygepjarmu", 0.0))
teher_osszesen = float(st.session_state.get("teher_osszesen", 0.0))
szemely_celevre = float(st.session_state.get("szemely_celevre", 0.0))
teher_celevre = float(st.session_state.get("teher_celevre", 0.0))

evek_szama = max(0, celev - 2025)
faktor_szemely = (1 + (p_szemely_pct / 100.0)) ** evek_szama
faktor_teher = (1 + (p_teher_pct / 100.0)) ** evek_szama


def parse_szelveny(val):
    if pd.isna(val):
        return None
    try:
        val_str = str(val).strip().replace(" ", "")

        if "+" in val_str:
            parts = val_str.split("+")
            km = float(parts[0]) if parts[0] else 0.0
            m = float(parts[1]) if (len(parts) > 1 and parts[1]) else 0.0
            return km + (m / 1000.0)

        val_str = val.str.replace(",", ".")
        return float(val_str)

    except Exception:
        return None

excel_path = "2025_ANF.xlsx"
df = pd.read_excel(excel_path, sheet_name="eanf_2025_20261001", header=1)

df["Út száma"] = (df["Út száma"].astype(str).str.replace(r"\.0$", "", regex=True).str.strip())

df["eleje_km"] = df["Érv.eleje"].apply(parse_szelveny)
df["vege_km"] = df["Érv.vége"].apply(parse_szelveny)

def keres_szelveny(ut_szama, szelveny_input):
    user_km = parse_szelveny(szelveny_input)

    if user_km is None:
        print("Érvénytelen szelvényszám formátum!")
        return None

    ut_szama_clean = str(ut_szama).strip().replace('.0', '')
    feltetel_ut = df["Út száma"] == ut_szama_clean

    min_km = df[['eleje_km', 'vege_km']].min(axis=1)
    max_km = df[['eleje_km', 'vege_km']].max(axis=1)

    feltetel_szelveny = (min_km <= user_km) & (user_km <= max_km)

    talalatok = df[feltetel_ut & feltetel_szelveny]

    if talalatok.empty:
        print(f"Nem található szakasz a(z) {ut_szama} úton a(z) {szelveny_input} szelvénynél!")
        return None
    return talalatok

with tab1:
    adatforras = st.radio(
        "Válassza ki a forgalmi adatok forrását:",
        [
            "Országos közúthálózat (adatbázis)",
            "Manuális adatmegadás (helyi / önkormányzati út)"
        ],
        horizontal=True
    )

    st.divider()

    if adatforras == "Országos közúthálózat (adatbázis)":
        col_ut, col_szelv = st.columns(2)
        with col_ut:
            keresett_ut = st.text_input("Adja meg a keresett út számát: ", value="1")
        with col_szelv:
            keresett_szelveny = st.text_input(label= "Adja meg a keresett szelvény számát: ", value="79+866")

        if st.button("Átlagos napi forgalom lekérése: ", use_container_width = True):
            talalat = keres_szelveny(keresett_ut, keresett_szelveny)
            fontos_oszlopok = [
                "Út száma",
                "Megye",
                "Érv.eleje",
                "Érv.vége",
                "ÉÁNF (Ej)",
                "Személy-gépkocsi",
                "Szóló teher-gépkocsi",
                "Pótkocsis teher-gépkocsi",
                "Nyerges szerelvény",
            ]

            st.subheader("Megtalált útszakasz adatai: ")
            st.dataframe(talalat[fontos_oszlopok], use_container_width = True, hide_index= True)
            szolo = float(talalat['Szóló teher-gépkocsi'].values[0] or 0)
            potkocsis = float(talalat['Pótkocsis teher-gépkocsi'].values[0] or 0)
            nyerges = float(talalat['Nyerges szerelvény'].values[0] or 0)
            szemelygepjarmi = float(talalat['Személy-gépkocsi'].values[0] or 0)

            teher_osszesen = (szolo + potkocsis + nyerges) * 2.5
            szemelygepjarmu = szemelygepjarmi
            szemely_celevre = szemelygepjarmu * faktor_szemely
            teher_celevre = teher_osszesen * faktor_teher

            st.session_state['szemelygepjarmu'] = szemelygepjarmu
            st.session_state['teher_osszesen'] = teher_osszesen
            st.session_state['szemely_celevre'] = szemely_celevre
            st.session_state['teher_celevre'] = teher_celevre
        else:
            st.warning("A megadott keresési feltételekkel nem található útszakasz a megadott adatbázisban.")

    else:
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            manual_szemely = st.number_input("Személygépjárművek száma (jármű/nap):", min_value = 0.0, value=0.0, step = 10.0)
        with col_m2:
            manual_teher = st.number_input("Tehergépjárművek száma (jármű/nap):", min_value = 0.0, value=0.0, step = 10.0)

        if st.button("Manuális forgalom mentése", use_container_width = True):
            szemelygepjarmu = manual_szemely
            teher_osszesen = manual_teher * 2.5
            szemely_celevre = szemelygepjarmu * faktor_szemely
            teher_celevre = teher_osszesen * faktor_teher

            st.session_state['szemelygepjarmu'] = szemelygepjarmu
            st.session_state['teher_osszesen'] = teher_osszesen
            st.session_state['szemely_celevre'] = szemely_celevre
            st.session_state['teher_celevre'] = teher_celevre
        st.divider()

    c1, c2 = st.columns(2)
    with c1:
        with st.container(border = True):
            st.metric(label="Személygépjárművek száma", value=f"{szemelygepjarmu:,.0f} jármű/nap".replace(",", ""))
    with c2:
        with st.container(border = True):
            st.metric(label=f"Tehergépjárművek száma", value=f"{teher_osszesen:,.0f} Ej/nap".replace(",", ""), help="Ej = Egységjármű")
    c3, c4 = st.columns(2)
    with c3:
        with st.container(border=True):
            st.metric(label=f"Személygépjárművek száma [{celev}]" , value=f"{szemely_celevre:,.0f} jármű/nap".replace(",", ""))
    with c4:
        with st.container(border=True):
            st.metric(label=f"Tehergépjárművek száma [{celev}]", value=f"{teher_celevre:,.0f} Ej/nap".replace(",", ""),
                        help="Ej = Egységjármű")

with tab2:
    def szamol_zarvatartas(lezaras_lista, vizsgalt_idoszak_sec=3600):
        db = len(lezaras_lista)
        osszes_sec = sum(lezaras_lista)
        osszes_min = osszes_sec / 60
        zarvatartas_ptc = (osszes_sec / vizsgalt_idoszak_sec) * 100
        szabad_pct = 100.0 - zarvatartas_ptc
        atlag_zaras_perc = osszes_min / db if db > 0 else 0

        return {
            "lezarasok_szama": db,
            "osszes_zaras_sec": osszes_sec,
            "osszes_zaras_min": round(osszes_min, 2),
            "zarvatartas_ptc": round(zarvatartas_ptc, 2),
            "szabad_pct": round(szabad_pct, 2),
            "atlag_zaras_perc": round(atlag_zaras_perc, 1)
        }

    lezarasok_szama = st.text_input(label="Adja meg a lezárások időtartamát, vesszővel elválasztva: ", value="84, 180, 74, 231, 113, 167, 85, 68")
    lezarasok_sec = [float(x.strip()) for x in lezarasok_szama.split(",") if x.strip()]
    if lezarasok_sec:
        zarvatartas_adatok = szamol_zarvatartas(lezarasok_sec)
        st.session_state["osszes_zaras_min"] = zarvatartas_adatok["osszes_zaras_min"]
        st.session_state["atlag_zaras_perc"] = zarvatartas_adatok["atlag_zaras_perc"]
        st.session_state["zarvatartas_ptc"] = zarvatartas_adatok["zarvatartas_ptc"]

    if st.button("Keresztmetszeti áteresztőképesség meghatározása: ", use_container_width = True):
        with st.container(border=True):
            st.write(f"Lezárások száma: {zarvatartas_adatok['lezarasok_szama']} db")
            st.write("Összes zárvatartási idő:"
          f" {zarvatartas_adatok['osszes_zaras_sec']} másodperc = "
          f" {zarvatartas_adatok['osszes_zaras_min']} perc")
            st.write(f"Átlagos egyedi lezárási idő: {zarvatartas_adatok['atlag_zaras_perc']} perc")
            st.write(f"A csúcsóra korlátozottsága: {zarvatartas_adatok['zarvatartas_ptc']} %")
            st.write(f"A szabad áthaladási időaránya: {zarvatartas_adatok['szabad_pct']} %")

    st.subheader("Csúcsóra korlátozottsága")
    df_zarvatartas = pd.DataFrame({"Kategória": ["Áthaladás korlátozva", "Szabad áthaladás"], "Arány": [zarvatartas_adatok["zarvatartas_ptc"], zarvatartas_adatok["szabad_pct"]]})
    fig = px.pie(df_zarvatartas, values= "Arány", names="Kategória", hole=0.6, color_discrete_sequence = ['#2563EB', '#38BDF8', '#F59E0B', '#10B981'])
    fig.update_traces(textinfo='none', hovertemplate='<b>%{label}</b><br>Arány: %{percent}<extra></extra>')
    fig.update_layout(font=dict(family="Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif",size=13,color="#E5E7EB"),showlegend=True,legend=dict(
    orientation="h",yanchor="bottom",y=-0.25,xanchor="center",x=0.5,font=dict(size=12)),margin=dict(t=20, b=40, l=20, r=20),paper_bgcolor='rgba(0,0,0,0)',)
    st.plotly_chart(fig, use_container_width=True)