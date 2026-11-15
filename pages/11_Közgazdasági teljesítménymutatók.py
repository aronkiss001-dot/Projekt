import streamlit as st
import pandas as pd

st.markdown("""<style>div[data-testid="stMetricValue"] {font-size: 30px !important;}</style>""", unsafe_allow_html=True)
st.markdown("<h1 style = 'text-align: center;'>Közgazdasági teljesítménymutatók meghatározása</style>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(['Közgazdasági Nettó jelenérték', 'Közgazdasági Belső Megtérülési Ráta', 'Haszon-költség arány', 'Érzékenységvizsgálat'])

def fmt(ertek):
    return f"{ertek:,.0f}".replace(",", " ")
jelenertekek = st.session_state.get("jelenertekek", [])
jelenertekek_teher = st.session_state.get("jelenertekek_teher", [])
jelenertekek_vasutIC = st.session_state.get("jelenertekek_vasutIC", [])
jelenertekek_vasutszemely = st.session_state.get("jelenertekek_vasutszemely", [])
jelenertekek_vasutaru = st.session_state.get("jelenertekek_vasutaru", [])
jelenertekek_baleset = st.session_state.get("jelenertekek_baleset", [])
jelenertekek_csaporud = st.session_state.get("jelenertekek_csaporud", [])
jelenertekek_uzemanyagMAV = st.session_state.get("jelenertekek_uzemanyagMAV", [])
jelenertekek_szgk_baleset = st.session_state.get("jelenertekek_szgk_baleset", [])
jelenertekek_teher_baleset = st.session_state.get("jelenertekek_teher_baleset", [])
jelenertekek_vasutiszesza_baleset= st.session_state.get("jelenertekek_vasutiszesza_baleset", [])
jelenertekek_vasutiteher_baleset = st.session_state.get("jelenertekek_vasutiteher_baleset", [])
jelenertekek_legszennyezes_varakozas = st.session_state.get("jelenertekek_legszennyezes_varakozas", [])
jelenertekek_legszennyezes_tobbletfutas = st.session_state.get("jelenertekek_legszennyezes_tobbletfutas", [])
jelenertekek_eghajlatvaltozas_varakozas = st.session_state.get("jelenertekek_eghajlatvaltozas_varakozas", [])
jelenertekek_eghajlatvaltozas_tobbletfutas = st.session_state.get("jelenertekek_eghajlatvaltozas_tobbletfutas", [])
jelenertekek_zajkar_varakozas = st.session_state.get("jelenertekek_zajkar_varakozas", [])
referencia_idoszak = int(st.session_state.get("referencia_idoszak", 30))
teljes_mukodesi_koltseg = float(st.session_state.get("teljes_mukodesi_koltseg", 0.0))
feluljaro_maradvanyertek = float(st.session_state.get("feluljaro_maradvanyertek", 0.0))
korforgalom_maradvanyertek = float(st.session_state.get("korforgalom_maradvanyertek", 0.0))
teljes_beruhazasi_koltseg = float(st.session_state.get("teljes_beruhazasi_koltseg", 0.0))
tarsadalmi_hasznok = st.session_state.get("tarsadalmi_hasznok", [])
tarsadalmi_hasznok_teher = st.session_state.get("tarsadalmi_hasznok_teher", [])
tarsadalmi_hasznok_vasutIC = st.session_state.get("tarsadalmi_hasznok_vasutIC", [])
tarsadalmi_hasznok_vasutszemely = st.session_state.get("tarsadalmi_hasznok_vasutszemely", [])
tarsadalmi_hasznok_vasutaru = st.session_state.get("tarsadalmi_hasznok_vasutaru", [])
tarsadalmi_hasznok_baleset = st.session_state.get("tarsadalmi_hasznok_baleset", [])
tarsadalmihasznok_csaporud = st.session_state.get("tarsadalmihasznok_csaporud", [])
tarsadalmi_haszon_uzemanyagMAV = st.session_state.get("tarsadalmi_haszon_uzemanyagMAV", [])
tarsadalmi_hasznok_szgk_baleset = st.session_state.get("tarsadalmi_hasznok_szgk_baleset", [])
tarsadalmi_hasznok_teher_baleset = st.session_state.get("tarsadalmi_hasznok_teher_baleset", [])
tarsadalmi_hasznok_vasutiszesza_baleset = st.session_state.get("tarsadalmi_hasznok_vasutiszesza_baleset", [])
tarsadalmi_hasznok_vasutiteher_baleset = st.session_state.get("tarsadalmi_hasznok_vasutiteher_baleset", [])
tarsadalmi_hasznok_legszennyezes_varakozas = st.session_state.get("tarsadalmi_hasznok_legszennyezes_varakozas", [])
tarsadalmi_hasznok_legszennyezes_tobbletfutas = st.session_state.get("tarsadalmi_hasznok_legszennyezes_tobbletfutas", [])
tarsadalmi_hasznok_eghajlatvaltozas_varakozas = st.session_state.get("tarsadalmi_hasznok_eghajlatvaltozas_varakozas", [])
tarsadalmi_hasznok_eghajlatvaltozas_tobbletfutas = st.session_state.get("tarsadalmi_hasznok_eghajlatvaltozas_tobbletfutas", [])
tarsadalmi_hasznok_zajkar_varakozas = st.session_state.get("tarsadalmi_hasznok_zajkar_varakozas", [])

haszon_jelenertek_lista = [
        jelenertekek,
        jelenertekek_teher,
        jelenertekek_vasutIC,
        jelenertekek_vasutszemely,
        jelenertekek_vasutaru,
        jelenertekek_baleset,
        jelenertekek_csaporud,
        jelenertekek_uzemanyagMAV,
        jelenertekek_szgk_baleset,
        jelenertekek_teher_baleset,
        jelenertekek_vasutiszesza_baleset,
        jelenertekek_vasutiteher_baleset,
        jelenertekek_legszennyezes_varakozas,
        jelenertekek_legszennyezes_tobbletfutas,
        jelenertekek_eghajlatvaltozas_varakozas,
        jelenertekek_eghajlatvaltozas_tobbletfutas,
        jelenertekek_zajkar_varakozas
    ]

eves_diszkontalt_hasznok = [sum(lista[t] for lista in haszon_jelenertek_lista if t < len(lista)) for t in range(referencia_idoszak)]
osszes_diszkontalt_haszon = sum(eves_diszkontalt_hasznok)

eves_diszkontalt_mukodesikoltseg = [teljes_mukodesi_koltseg / (1.03 ** (t+1)) for t in range(referencia_idoszak)]
osszes_diszkontalt_mukodesikoltseg = sum(eves_diszkontalt_mukodesikoltseg)

teljes_maradvanyertek = feluljaro_maradvanyertek + korforgalom_maradvanyertek
diszkontalt_maradvanyertek = teljes_maradvanyertek / (1.03 ** referencia_idoszak)

enpv = -teljes_beruhazasi_koltseg - osszes_diszkontalt_mukodesikoltseg + diszkontalt_maradvanyertek + osszes_diszkontalt_haszon
with tab1:
        if st.button("Közgazdasági Nettó Jelenérték Meghatározása", use_container_width=True):
            with st.container(border=True):
                st.metric(label=f"A közgazdasági nettó jelenérték", value=f"{fmt(enpv)} Ft.")

with tab2:
    haszon_nevleges_lista = [
        tarsadalmi_hasznok,
        tarsadalmi_hasznok_teher,
        tarsadalmi_hasznok_vasutIC,
        tarsadalmi_hasznok_vasutszemely,
        tarsadalmi_hasznok_vasutaru,
        tarsadalmi_hasznok_baleset,
        tarsadalmihasznok_csaporud,
        tarsadalmi_haszon_uzemanyagMAV,
        tarsadalmi_hasznok_szgk_baleset,
        tarsadalmi_hasznok_teher_baleset,
        tarsadalmi_hasznok_vasutiszesza_baleset,
        tarsadalmi_hasznok_vasutiteher_baleset,
        tarsadalmi_hasznok_legszennyezes_varakozas,
        tarsadalmi_hasznok_legszennyezes_tobbletfutas,
        tarsadalmi_hasznok_eghajlatvaltozas_varakozas,
        tarsadalmi_hasznok_eghajlatvaltozas_tobbletfutas,
        tarsadalmi_hasznok_zajkar_varakozas
    ]

    penzaramok = [-teljes_beruhazasi_koltseg]

    for t in range(referencia_idoszak):
        eves_haszon_nevleges = sum(lista[t] for lista in haszon_nevleges_lista if t < len(lista))

        eves_netto = eves_haszon_nevleges - teljes_mukodesi_koltseg

        if t == 28:
            eves_netto += teljes_maradvanyertek

        penzaramok.append(eves_netto)


    def szamol_err(cf_lista):
        try:
            import numpy_financial as npf
            return npf.irr(cf_lista)
        except ImportError:
            def npv_f(r):
                return sum(cf / ((1 + r) ** t) for t, cf in enumerate(cf_lista))

            low, high = 0.0, 2.0
            for _ in range(100):
                mid = (low + high) / 2
                val = npv_f(mid)
                if abs(val) < 1e-2:
                    return mid
                if val > 0:
                    low = mid
                else:
                    high = mid
            return mid


    err_ertek = szamol_err(penzaramok)

    if st.button("Közgazdasági Belső Megtérülési Ráta meghatárotzása", use_container_width=True):
        with st.container(border=True):
            st.metric(label=f"A közgazdasági Belső Megtérülési Ráta", value=f"{fmt(err_ertek * 100)} %.")
            st.write(f"Elvárt társadalmi diszkontráta:          3.00 %")
        if err_ertek > 0.03:
            st.write("ÉRTÉKELÉS: Az ERR > 3%, a beruházás társadalmilag megtérülő!")

with tab3:
    osszes_lediszkontalt_netto_haszon = (
                osszes_diszkontalt_haszon - osszes_diszkontalt_mukodesikoltseg + diszkontalt_maradvanyertek)

    bcr = osszes_lediszkontalt_netto_haszon / teljes_beruhazasi_koltseg if teljes_beruhazasi_koltseg > 0 else 0.0
    if st.button("Haszon-Költség Arány meghatározása", use_container_width=True):
        if teljes_beruhazasi_koltseg == 0.0:
            st.write("A beruházási költség jelenleg 0 Forint. Kérjük, előbb számítsa ki az 1. oldalon!")
        else:
            with st.container(border=True):
                st.metric(label=f"Kezdeti beruházási költség:", value=f"{fmt(teljes_beruhazasi_koltseg)} Ft.")
                st.metric(label=f"Lediszkontált nettó társadalmi hasznok:", value=f"{fmt(osszes_lediszkontalt_netto_haszon)} Ft.")
                st.metric(label=f"Haszon-költség arány:", value=f"{fmt(bcr)}")

        if bcr > 1.0:
            st.write("Értékelés: Mivel BCR > 1, a beruházás társadalmilag megtérülő!")
            st.balloons()

with tab4:
    if teljes_beruhazasi_koltseg <= 0:
        st.warning("A beruházási költség jelenleg 0 Forint. Kérjük, előbb számítsa ki az 1. oldalon!")
    else:
        beruhazas_valtozasok = [-0.20, -0.10, 0.00, 0.10, 0.20, 0.50]
        haszon_valtozasok = [-0.30, -0.20, -0.10, 0.00, 0.10, 0.20]

        bcr_matrix = []

        for c_var in beruhazas_valtozasok:
            row = []
            uj_beruhazas = teljes_beruhazasi_koltseg * (1 + c_var)
            for h_var in haszon_valtozasok:
                uj_netto_haszon = osszes_lediszkontalt_netto_haszon * (1 + h_var)
                uj_bcr = uj_netto_haszon / uj_beruhazas
                row.append(round(uj_bcr, 2))
            bcr_matrix.append(row)

        df_bcr_erzekenyseg = pd.DataFrame(
            bcr_matrix,
            index=[f"Beruházási költség {c * 100:+.0f}%" for c in beruhazas_valtozasok],
            columns=[f"Haszon {h * 100:+.0f}%" for h in haszon_valtozasok]
        )

        def szinezes(val):
            if val > 1.0:
                return "background-color: rgba(46, 204, 113, 0.25);"
            return "background-color: rgba(231, 76, 60, 0.25);"

        st.dataframe(
            df_bcr_erzekenyseg.style.format("{:.2f}").map(szinezes), use_container_width=True)
        st.caption("Zöld: Társadalmilag megtérülő kombináció (BCR ≥ 1,00) | Piros: nem megtérülő (BCR < 1,00)")

        print("\nHaszon-Költség Arány Érzékenységi Mátrix:")
        print(df_bcr_erzekenyseg.to_string())

