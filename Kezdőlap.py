import streamlit as st

st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>Vasúti átjárók kiváltásának költség-haszon elemzés modellje</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9CA3AF; font-size: 18px; margin-top: 8px;'>Különszintű csomóponti átépítés (felüljáró és körforgalom) társadalmi-gazdasági megtérülésének vizsgálata</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9CA3AF; font-size: 14px; margin-top: 8px;'>Kiss Áron Ágoston, 2026.11.16.</p>", unsafe_allow_html=True)
st.set_page_config(layout="wide")

st.divider()
st.set_page_config(
    page_title="Vasúti átjárók CBA modell",
    page_icon="🚆",
    layout="wide"
)

with st.expander("Használati útmutató"):
    col0, col1 = st.columns(2)

    with col0:
        with st.container(border=True):
            st.markdown("#### 0. Bemenő adatok")
            st.write(
                "A számítások elvégzéséhez különböző bemenő adatok szükségesek a **Kezdőlapon.** A modell ezeknek az értékeknek a figyelembevételével határozza meg a későbbi eredményeket.")
            st.caption("Kimenet: Referencia-időszak.")

    with col1:
        with st.container(border=True):
            st.markdown("#### 1. Működési költségadatok")
            st.write(
                "Amennyiben egy projekt megtérülését szeretné meghatározni, az 1. oldalon megadhatóak egy felüljáró és egy körforgalom műszaki adatai. Amennyiben csak a költségekre kíváncsi, úgy ez a lépés kihagyható.")
            st.caption("Kimenet: CAPEX, OPEX, pótlási költség és maradványérték.")

    col2, col3 = st.columns(2)

    with col2:
        with st.container(border=True):
            st.markdown("#### 2. Forgalom és zárvatartás")
            st.write(
                "Az **Átlagos Napi Forgalom** oldalon lehetőség van Átlagos Napi Forgalom lekérésére. Ezt csak az országos közúthálózat területére vetítve lehet használni. "
                "Amennyiben más típusú keresztmetszet forgalmára kíváncsi, úgy manuálisan kell beírni az értékeket.")
            st.write("A **Keresztmetszeti áteresztőképesség** fülön másodpercekben adja meg "
                "az egyes zárvatartási időket egy órára vetítve.")
            st.caption("Kimenet: Célévre vetített forgalom és csúcsórai korlátozottság (%).")

    with col3:
        with st.container(border=True):
            st.markdown("#### 3. Externáliák különböző szituációkban")
            st.write(
                "A modell következő részében lehetősége van kiszámítani a felmerült társadalmi költségeket/hasznokat. Lesznek olyan szegmensek, melyeknél újabb bemenő adatok megadása szükséges, lesznek olyanok, melyeket a rendszer már automatikusan meghatározott.")
            st.caption("Kimenet: Idő-, baleseti és környezeti hasznok")

    st.write("")

    # --- RÖVID MÓDSZERTANI TÁJÉKOZTATÓ ---
    with st.expander("Módszertani alapfeltevések és adatkezelés megtekintése"):
        c_info1, c_info2 = st.columns(2)
        with c_info1:
            st.write("• **Elemzési időtáv:** 30 éves referencia-időszak (1 építési + 29 üzemeltetési év)")
            st.write("• **Közgazdasági diszkontráta:** 3,0% reálértéken")
        with c_info2:
            st.write("• **Forgalmi adatbázis:** Országos Közúti Adatbank (2025. évi ÉÁNF)")
            st.write("• **Adatátadás:** A beállított paraméterek automatikusan szinkronizálódnak az aloldalak között.")

    st.markdown(
        "<br><p style='text-align: center; color: #6B7280; font-size: 13px;'>Széchenyi István Egyetem • Tudományos Diákköri Konferencia (2026)</p>",
        unsafe_allow_html=True)


if "referencia_idoszak" not in st.session_state:
    st.session_state["referencia_idoszak"] = 0
if "celev" not in st.session_state:
    st.session_state["celev"] = 2026
if "szemely_celevre" not in st.session_state:
    st.session_state["szemely_celevre"] = 0
if "teher_celevre" not in st.session_state:
    st.session_state["teher_celevre"] = 0
if "baleseti_evek" not in st.session_state:
    st.session_state["baleseti_evek"] = [3, 8, 13, 18, 23, 28]


alap_ertekek = {
    "szemelygepjarmu": 0.0,
    "teher_osszesen": 0.0,
    "szemely_celevre": 0.0,
    "teher_celevre": 0.0,
    "osszes_zaras_min": 0.0,
    "atlag_zaras_perc": 0.0,
    "zarvatartas_ptc": 0.0,
}

for kulcs, ertek in alap_ertekek.items():
    if kulcs not in st.session_state:
        st.session_state[kulcs] = ertek

projekt_referencia_idoszak = st.number_input(
    "Hány év a projekt referencia időszaka? (általánosan: 30 év) (év): ",
    value=30,
    step=1,
    format="%.1f",
    key="projekt_referencia_idoszak")

st.session_state["referencia_idoszak"] = projekt_referencia_idoszak

BAZISEV = 2025
col_celev, = st.columns(1)
with col_celev:
    celev = st.number_input('Melyik évre szeretné elvégezni a vizsgálatot (bázisév)? ', value=st.session_state.get("celev"))
    evek_szama = celev - BAZISEV
    st.session_state["celev"] = celev

col_szemely_pct, col_teher_pct = st.columns(2)
with col_szemely_pct:
    p_szemely_pct = st.number_input('Mekkora az éves forgalomnövekedési ütem személygépjárműveknél?', value=1.5)
with col_teher_pct:
    p_teher_pct = st.number_input('Mekkora az éves forgalomnövekedési ütem tehergépjárműveknél?', value=1.5)

if evek_szama < 0:
    print("A célév korábbi a bázisévnél! Az érték az eredeti marad.")
    faktor_szemely = 1.0
    faktor_teher = 1.0
else:
    faktor_szemely = (1 + (p_szemely_pct / 100.00)) ** evek_szama
    faktor_teher = (1 + (p_teher_pct / 100.00)) ** evek_szama

    st.session_state["p_szemely_pct"] = p_szemely_pct
    st.session_state["p_teher_pct"] = p_teher_pct

    baleseti_evek_input = st.text_input(label="Melyik években következik be baleset?", value=", ".join(str(ev) for ev in st.session_state["baleseti_evek"]))
    if baleseti_evek_input.strip():
        try: baleseti_evek = [int(x.strip()) for x in baleseti_evek_input.split(",") if x.strip().isdigit()]
        except ValueError:
            st.error("Kérjük, csak számokat adjon meg, vesszővel elválasztva")
            baleseti_evek = [3, 8, 13, 18, 23]
    else:
        baleseti_evek = [3, 8, 13, 18, 23, 28]

    st.session_state["baleseti_evek"] = baleseti_evek

with open("static/TDK_ZEL3XV.pdf", "rb") as pdf_file:
    st.download_button(
        label="📄 A teljes forrásanyag letöltése (PDF)",
        data=pdf_file,
        file_name="Kiss_Aron_TDK_2026.pdf",
        mime="application/pdf",
        use_container_width=True
    )