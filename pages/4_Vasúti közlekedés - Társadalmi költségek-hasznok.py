import streamlit as st
import pandas as pd

st.markdown("<h1 style = 'text-align: center;'>Vasúti közlekedés időnyereségének számszerűsítése és monetizálása</style>", unsafe_allow_html=True)
st.markdown("""<style>div[data-testid="stMetricValue"] {font-size: 30px !important;}</style>""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(['Vasúti személyszállítás (InterCity)', 'Vasúti személyszállítás (Személyvonat)', 'Vasúti áruszállítás'])

with tab1:
    col_1, = st.columns(1)
    with col_1:
        IC_utasszam = st.number_input("Adja meg a napi InterCity utasforgalom értékét!", step=1, format="%.1f")
    col_2, col_3 = st.columns([1, 1])
    with col_2:
        uzemido = st.number_input("Hány óra a vasúti üzemidő a személyszállítást vizsgálva?", value=20, step=1, format="%.1f")
    with col_3:
        csaporud_tores = st.number_input("Hányszor törik le a csapórudat egy évben?", value=30, step=1, format="%.1f")
        forgalomkorlatozas = csaporud_tores * 3
        erintett_utasok = (3 / uzemido) * IC_utasszam
        osszes_keses = erintett_utasok * 0.05 * csaporud_tores

    if st.button("Várakozási idők meghatározása (IC)", use_container_width=True):
        with st.container(border=True):
            st.write(f"A forgalomkorlátozás ideje egy évben összesen {forgalomkorlatozas} óra/év.")
            st.write(f"Egy forgalomkorlátozás összesen {erintett_utasok} utast érint.")
            st.write(f"Az összes késés {round(osszes_keses, 1)} óra az összes utasra nézve.")

    uzleti_utazasingazas_eredeti = 4971  # forint/utasóra
    egyeb_utazas_eredeti = 1742  # forint/utasóra
    uzleti_utazasingazas_arany_vasut = osszes_keses * 0.25
    egyeb_utazas_arany_vasut = osszes_keses * 0.75

    elsoevi_tarsadalmikoltseg_vasutIC = ((uzleti_utazasingazas_eredeti * uzleti_utazasingazas_arany_vasut) + (
                egyeb_utazas_eredeti * egyeb_utazas_arany_vasut))
    def fmt(ertek):
        return f"{ertek:,.0f}".replace(",", " ")

    if st.button("InterCity utasok késéséből fakadó társadalmi költségek/hasznok", use_container_width=True):
        with st.container(border=True):
            st.metric(f"Az első évben az IC utasok késéséből származó társadalmi költség/haszon", value=f"{fmt(elsoevi_tarsadalmikoltseg_vasutIC)} Ft.")

    forgalom_novekedes = 1.015
    gdp_novekedese = 1.029
    diszkontrata = 1.030

    b3 = elsoevi_tarsadalmikoltseg_vasutIC

    jelenertekek_vasutIC = []
    tarsadalmi_hasznok_vasutIC = []
    aktualis_haszon_vasutIC = b3

    for t in range(1, 30):
        if t == 1:
            haszon_vasutIC = b3
        else:
            haszon_vasutIC = aktualis_haszon_vasutIC * forgalom_novekedes * gdp_novekedese
            aktualis_haszon_vasutIC = haszon_vasutIC

        pv_vasutIC = haszon_vasutIC / (diszkontrata ** t)
        jelenertekek_vasutIC.append(pv_vasutIC)
        tarsadalmi_hasznok_vasutIC.append(haszon_vasutIC)
    osszes_tarsadalmi_haszon_vasutIC = sum(tarsadalmi_hasznok_vasutIC)
    osszes_diszkontalt_haszon_vasutIC = sum(jelenertekek_vasutIC)

    if st.button("Az IC vonatokon utazók késéséből származó összes társadalmi költség/haszon a referencia időszakban", use_container_width=True):
        with st.container(border=True):
            st.metric(label=f"Az összes haszon", value=f"{fmt(osszes_tarsadalmi_haszon_vasutIC)} forint társadalmi haszon")
            st.metric(label=f"Az összes diszkontált haszon", value=f"{fmt(osszes_diszkontalt_haszon_vasutIC)} Forint nettó jelenértékű haszon.")

    evek_szama = len(tarsadalmi_hasznok_vasutIC)
    with st.expander("\n--- Éves társadalmi hasznok az IC vonatokon utazók várakozására nézve ---"):
        df_haszon = pd.DataFrame({"Év (t): ": [f"{i+1}. év" for i in range(evek_szama)], "Társadalmi haszon (Ft)": [f"{fmt(x)} Ft" for x in tarsadalmi_hasznok_vasutIC], "Diszkontált haszon (Ft)": [f"{fmt(x)} Ft" for x in jelenertekek_vasutIC]})
        st.dataframe(df_haszon, use_container_width=True, hide_index=True)

with tab2:
    col_1, = st.columns(1)
    with col_1:
        szemely_utasszam = st.number_input("Adja meg a napi személyvonati utasforgalom értéket!", step=1, format="%.1f", help="Ide tartozik az összes vonat, amelyren nem kötelező a helyjegy vásárlása (2026)")
        erintett_utasok_szemely = (3 / uzemido) * szemely_utasszam
        osszes_keses_szemely = erintett_utasok_szemely * 0.05 * csaporud_tores

    if st.button("Várakozási idők meghatározása (személyvonat)", use_container_width=True):
        with st.container(border=True):
            st.write(f"A forgalomkorlátozás ideje egy évben összesen {forgalomkorlatozas} óra/év.")
            st.write(f"Egy forgalomkorlátozás összesen {erintett_utasok_szemely} utast érint.")
            st.write(f"Az összes késés {round(osszes_keses_szemely, 1)} óra az összes utasra nézve.")

    uzleti_utazasingazas_arany_vasutszemely = osszes_keses_szemely * 0.25
    egyeb_utazas_arany_vasutszemely = osszes_keses_szemely * 0.75

    elsoevi_tarsadalmikoltseg_vasutszemely = ((uzleti_utazasingazas_eredeti * uzleti_utazasingazas_arany_vasutszemely) + (egyeb_utazas_eredeti * egyeb_utazas_arany_vasutszemely))

    def fmt(ertek):
        return f"{ertek:,.0f}".replace(",", " ")

    if st.button("Személyvonaton utazók késéséből fakadó társadalmi költségek/hasznok", use_container_width=True):
        with st.container(border=True):
            st.metric(f"Az első évben a személyvonaton utazók késéséből származó társadalmi költség/haszon", value=f"{fmt(elsoevi_tarsadalmikoltseg_vasutszemely)} Ft.")

    b4 = elsoevi_tarsadalmikoltseg_vasutszemely

    jelenertekek_vasutszemely = []
    tarsadalmi_hasznok_vasutszemely = []
    aktualis_haszon_vasutszemely = b4

    for t in range(1, 30):
        if t == 1:
            haszon_vasutszemely = b4
        else:
            haszon_vasutszemely = aktualis_haszon_vasutszemely * forgalom_novekedes * gdp_novekedese
            aktualis_haszon_vasutszemely = haszon_vasutszemely

        pv_vasutszemely = haszon_vasutszemely / (diszkontrata ** t)
        jelenertekek_vasutszemely.append(pv_vasutszemely)
        tarsadalmi_hasznok_vasutszemely.append(haszon_vasutszemely)

    osszes_tarsadalmi_haszon_vasutszemely = sum(tarsadalmi_hasznok_vasutszemely)
    osszes_diszkontalt_haszon_vasutszemely = sum(jelenertekek_vasutszemely)

    if st.button("A személyvonatokon utazók késéséből származó összes társadalmi költség/haszon a referencia időszakban", use_container_width=True):
        with st.container(border=True):
            st.metric(label=f"Az összes haszon", value=f"{fmt(osszes_tarsadalmi_haszon_vasutszemely)} forint társadalmi haszon")
            st.metric(label=f"Az összes diszkontált haszon", value=f"{fmt(osszes_diszkontalt_haszon_vasutszemely)} Forint nettó jelenértékű haszon.")

    evek_szama_2 = len(tarsadalmi_hasznok_vasutszemely)
    with st.expander("\n--- Éves társadalmi hasznok a személyvonaton utazók várakozására nézve ---"):
        df_haszon_szemely = pd.DataFrame({"Év (t): ": [f"{i+1}. év" for i in range(evek_szama_2)], "Társadalmi haszon (Ft)": [f"{fmt(x)} Ft" for x in tarsadalmi_hasznok_vasutszemely], "Diszkontált haszon (Ft)": [f"{fmt(x)} Ft" for x in jelenertekek_vasutszemely]})
        st.dataframe(df_haszon_szemely, use_container_width=True, hide_index=True)

