import streamlit as st
import pandas as pd

st.markdown("""<style>div[data-testid="stMetricValue"] {font-size: 30px !important;}</style>""", unsafe_allow_html=True)
st.markdown("<h1 style = 'text-align: center;'>Rendkívüli eseményekből (RE) származó társadalmi költségek/hasznok</style>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(['RE - Személygépjárművek', 'RE - Tehergépjárművek', 'RE - Vasúti személyszállítás', 'RE - Vasúti áruszállítás'])

if "forgalomkorlatozas_rendkivuli" not in st.session_state:
    st.session_state["forgalomkorlatozas_rendkivuli"] = 0.0
if "tobbletkm_rendkivuli" not in st.session_state:
    st.session_state["tobbletkm_rendkivuli"] = 0.0
if "baleseti_evek" not in st.session_state:
    st.session_state["baleseti_evek"] = 0.0

def fmt(ertek):
    return f"{ertek:,.0f}".replace(",", " ")

with tab1:
    col_1, = st.columns(1)
    with col_1:
        idoveszteseg_rendkivuli = st.number_input("Hány perces a legrövidebb kerülőútirány egy rendkívüli esemény bekövetkeztekor?", step=1.0, help="[perc]")
    col_2, = st.columns(1)
    with col_2:
        tobbletkm_rendkivuli = st.number_input("Mekkora a legkisebb kerülőútvonal egy rendkívüli esemény bekövetkeztekor?", step=1.0, help="[km]")
    col_3, = st.columns(1)
    with col_3:
        forgalomkorlatozas_rendkivuli = st.number_input("Hány órán keresztül tart egy adott forgalomkorlátozás egy rendkívüli esemény bekövetkeztekor?", step=1.0, help="[óra/esemény]")

    szemelygepjarmu = float(st.session_state.get("szemelygepjarmu", 0.0))
    st.session_state["forgalomkorlatozas_rendkivuli"] = forgalomkorlatozas_rendkivuli
    st.session_state["tobbletkm_rendkivuli"] = tobbletkm_rendkivuli
    uzleti_utazasingazas_eredeti = 4971
    egyeb_utazas_eredeti = 1742
    erintett_szgk_rendkivuli = szemelygepjarmu * (forgalomkorlatozas_rendkivuli / 24)
    erintett_szemelyek_rendkivuli = erintett_szgk_rendkivuli * 1.5

    tarsadalmi_koltseg_szgk_rendkivuli_uzletiutazasingazas = ((erintett_szgk_rendkivuli * 0.25) * (idoveszteseg_rendkivuli / 60) * uzleti_utazasingazas_eredeti)
    tarsadalmi_koltseg_szgk_rendkivuli_egyeb = ((erintett_szgk_rendkivuli * 0.75) * (idoveszteseg_rendkivuli / 60) * egyeb_utazas_eredeti)
    tarsadalmi_koltseg_szgk_osszesen = tarsadalmi_koltseg_szgk_rendkivuli_uzletiutazasingazas + tarsadalmi_koltseg_szgk_rendkivuli_egyeb
    tobbletkm_rendkivuli_osszes = tobbletkm_rendkivuli * erintett_szgk_rendkivuli
    tobblet_uzemanyagfogyasztas_rendkivuli = tobbletkm_rendkivuli_osszes * 50

    with st.container(border=True):
        st.write(f"A forgalomkorlátozás {round(erintett_szgk_rendkivuli, 1)} db személygépjárművet érintett.")
        st.write(f"A forgalomkorlátozás {round(erintett_szemelyek_rendkivuli, 1)} személyt érintett.")
        st.metric(label=f"Egy forgalomkorlátozás során összesen a személygépjárművek kerülőútirány-igénybevétele miatt keletkező költség:", value=f"{fmt(tarsadalmi_koltseg_szgk_osszesen)} Forint.")
        st.metric(label=f"Egy forgalomkorlátozás során az üzemanyagköltség összesen:", value=f"{fmt(tobblet_uzemanyagfogyasztas_rendkivuli)} Forint.", help="Fajlagos üzemanyag-költség: 50 Ft/km")

    baleseti_evek_input = st.text_input(label="Melyik években következik be baleset?", value="3, 8, 13, 18, 23, 28")
    if baleseti_evek_input.strip():
        try: baleseti_evek = [int(x.strip()) for x in baleseti_evek_input.split(",") if x.strip()]
        except ValueError:
            st.error("Kérjük, csak számokat adjon meg, vesszővel elválasztva")
            baleseti_evek = [3, 8, 13, 18, 23]
    else:
        baleseti_evek = [3, 8, 13, 18, 23, 28]

    st.session_state["baleseti_evek"] = baleseti_evek

    if st.button("Baleseti évek listázása", use_container_width = True, key="baleseti_evek_szgk"):
        with st.container(border=True):
            st.metric(label=f"Baleseti kockázatvizsgálat a következő években:", value=", ".join(str(x) for x in baleseti_evek))

    elsoevi_tarsadalmikoltseg_szgk_rendkivuli = tarsadalmi_koltseg_szgk_osszesen + tobblet_uzemanyagfogyasztas_rendkivuli
    forgalom_novekedes = 1.015
    gdp_novekedese = 1.029
    diszkontrata = 1.030
    referencia_idoszak = int(st.session_state.get("referencia_idoszak", 30))

    b9 = elsoevi_tarsadalmikoltseg_szgk_rendkivuli
    jelenertekek_szgk_baleset = []
    tarsadalmi_hasznok_szgk_baleset = []
    aktualis_haszon_szgk_baleset = b9

    for t in range(1, referencia_idoszak):
        if t == 1:
            haszon_szgk_baleset = b9
        else:
            haszon_szgk_baleset = aktualis_haszon_szgk_baleset * forgalom_novekedes * gdp_novekedese
            aktualis_haszon_szgk_baleset = haszon_szgk_baleset

        if t in baleseti_evek:
            ujhaszon_szgk_baleset = haszon_szgk_baleset
        else:
            ujhaszon_szgk_baleset = 0.0

        pv_szgk_baleset = ujhaszon_szgk_baleset / (diszkontrata ** t)
        jelenertekek_szgk_baleset.append(pv_szgk_baleset)
        tarsadalmi_hasznok_szgk_baleset.append(ujhaszon_szgk_baleset)

        osszes_tarsadalmihaszon_szgk_baleset = sum(tarsadalmi_hasznok_szgk_baleset)
        osszes_jelenertek_szgk_baleset = sum(jelenertekek_szgk_baleset)

    if st.button("RE-ből származó társadalmi költségek/hasznok a személygépjárművekre nézve", use_container_width = True, key="szgk_rendkivuli_gomb"):
        with st.container(border=True):
            st.metric(label=f"Az összes haszon",value=f"{fmt(osszes_tarsadalmihaszon_szgk_baleset)} forint társadalmi haszon")
            st.metric(label=f"Az összes diszkontált haszon",value=f"{fmt(osszes_jelenertek_szgk_baleset)} Forint nettó jelenértékű haszon.")

    evek_szama = len(tarsadalmi_hasznok_szgk_baleset)
    with st.expander("Éves társadalmi hasznok a RE-ből a személygépjárművekre nézve", key="szgk_rendkivuli_gomb2"):
        df_haszon = pd.DataFrame({"Év (t): ": [f"{i + 1}. év" for i in range(evek_szama)],
                                      "Társadalmi haszon (Ft)": [f"{fmt(x)} Ft" for x in tarsadalmi_hasznok_szgk_baleset],
                                      "Diszkontált haszon (Ft)": [f"{fmt(x)} Ft" for x in jelenertekek_szgk_baleset],})
        st.dataframe(df_haszon, use_container_width=True, hide_index=True)

with tab2:
    teher_celevre = float(st.session_state.get("teher_osszesen", 0.0))
    erintett_teher_rendkivuli = (teher_celevre / 2.5) * (forgalomkorlatozas_rendkivuli / 24)
    teher_fajlagos_idoertek = 595
    teher_rakomany = 18
    erintett_rakomany = erintett_teher_rendkivuli * teher_rakomany
    tarsadalmi_koltseg_teher_rendkivuli_osszesen = (erintett_rakomany * (idoveszteseg_rendkivuli / 60)) * teher_fajlagos_idoertek
    tobbletkm_teher_rendkivuli_osszes = tobbletkm_rendkivuli * erintett_teher_rendkivuli
    tobblet_uzemanyagfogyasztas_teher_rendkivuli = tobbletkm_teher_rendkivuli_osszes * (0.325 * 681)

    with st.container(border=True):
        st.write(f"A forgalomkorlátozás {round(erintett_teher_rendkivuli, 1)} db tehergépjárművet érintett.")
        st.write(f"A forgalomkorlátozás {round(erintett_rakomany, 1)} tonna árut érintett.")
        st.metric(label=f"Egy forgalomkorlátozás során a tehergépjárművek kerülőútirány-igénybevétele miatt keletkező költség:", value=f"{fmt(tarsadalmi_koltseg_teher_rendkivuli_osszesen)} Forint.")
        st.metric(label=f"Egy forgalomkorlátozás során az üzemenyagköltség összesen:", value=f"{fmt(tobblet_uzemanyagfogyasztas_teher_rendkivuli)} Forint.", help="Fajlagos üzemanyagköltség: 221,325Ft/km")

    elsoevi_tarsadalmikoltseg_teher_rendkivuli = tarsadalmi_koltseg_teher_rendkivuli_osszesen + tobblet_uzemanyagfogyasztas_teher_rendkivuli

    if st.button("Baleseti évek listázása", use_container_width = True, key="baleseti_evek_teher"):
        with st.container(border=True):
            st.metric(label=f"Baleseti kockázatvizsgálat a következő években:", value=", ".join(str(x) for x in baleseti_evek))

    b10 = elsoevi_tarsadalmikoltseg_teher_rendkivuli
    jelenertekek_teher_baleset = []
    tarsadalmi_hasznok_teher_baleset = []
    aktualis_haszon_teher_baleset = b10

    for t in range(1, referencia_idoszak):
        if t == 1:
            haszon_teher_baleset = b10
        else:
            haszon_teher_baleset = aktualis_haszon_teher_baleset * forgalom_novekedes
            aktualis_haszon_teher_baleset = haszon_teher_baleset

        if t in baleseti_evek:
            ujhaszon_teher_baleset = haszon_teher_baleset
        else:
            ujhaszon_teher_baleset = 0.0

        pv_teher_baleset = ujhaszon_teher_baleset / (diszkontrata ** t)
        jelenertekek_teher_baleset.append(pv_teher_baleset)
        tarsadalmi_hasznok_teher_baleset.append(ujhaszon_teher_baleset)
        osszes_tarsadalmihaszon_teher_baleset = sum(tarsadalmi_hasznok_teher_baleset)
        osszes_jelenertek_teher_baleset = sum(jelenertekek_teher_baleset)

    if st.button("RE-ből származó társadalmi költségek/hasznok a tehergépjárművekre nézve", use_container_width = True, key="teher_rendkivuli_gomb"):
        with st.container(border=True):
            st.metric(label=f"Az összes haszon",value=f"{fmt(osszes_tarsadalmihaszon_teher_baleset)} forint társadalmi haszon")
            st.metric(label=f"Az összes diszkontált haszon",value=f"{fmt(osszes_jelenertek_teher_baleset)} Forint nettó jelenértékű haszon.")

    evek_szama_2 = len(tarsadalmi_hasznok_teher_baleset)
    with st.expander("Éves társadalmi hasznok a RE-ből a tehergépjárművekre nézve", key="teher_rendkivuli_gomb2"):
        df_haszon_2 = pd.DataFrame({"Év (t): ": [f"{i + 1}. év" for i in range(evek_szama_2)],
                                      "Társadalmi haszon (Ft)": [f"{fmt(x)} Ft" for x in tarsadalmi_hasznok_teher_baleset],
                                      "Diszkontált haszon (Ft)": [f"{fmt(x)} Ft" for x in jelenertekek_teher_baleset],})
        st.dataframe(df_haszon_2, use_container_width=True, hide_index=True)

with tab3:
        col_1, = st.columns(1)
        with col_1:
            erintett_vonatok_SZESZA = st.number_input(
                "Hány személyszállító vonatot érint egy rendkívüli esemény?", step=1.0,
                help="[db vonat/esemény]")
        col_2, = st.columns(1)
        with col_2:
            atlagos_keses_SZESZA = st.number_input(
                "Mekkora az átlagos késése egy személyszállító vonatnak egy rendkívüli esesménynél?", step=1.0, help="[perc/esemény]")
        col_3, = st.columns(1)
        with col_3:
            erintett_utasok_rendkivuli_SZESZA = st.number_input(
                "Hány utast érint egy rendkívüli esemény?",
                step=1.0, help="[utas/esemény]")

        elsoevi_tarsadalmikoltseg_rendkivuli_vasutiSZESZA = ((uzleti_utazasingazas_eredeti * (
                erintett_utasok_rendkivuli_SZESZA * 0.25)) * atlagos_keses_SZESZA / 60) + ((egyeb_utazas_eredeti * (
                erintett_utasok_rendkivuli_SZESZA * 0.75)) * atlagos_keses_SZESZA / 60)

        with st.container(border=True):
            st.write(f"A rendkívüli esemény {round(erintett_vonatok_SZESZA, 1)} db személyvonatot érintett.")
            st.write(f"A rendkívüli esemény {round(erintett_utasok_rendkivuli_SZESZA, 1)} utast érintett.")
            st.write(f"Az átlagos késés {round(atlagos_keses_SZESZA, 1)} perc.")
            st.metric(
                label=f"Egy rendkívüli esemény során a személyvonatok késéséből keletkezett társadalmi költség",
                value=f"{fmt(elsoevi_tarsadalmikoltseg_rendkivuli_vasutiSZESZA)} Forint.")

        if st.button("Baleseti évek listázása", use_container_width=True, key="baleseti_evek_vasutiszesza"):
            with st.container(border=True):
                st.metric(label=f"Baleseti kockázatvizsgálat a következő években:",
                          value=", ".join(str(x) for x in baleseti_evek))

        b11 = elsoevi_tarsadalmikoltseg_rendkivuli_vasutiSZESZA
        jelenertekek_vasutiszesza_baleset = []
        tarsadalmi_hasznok_vasutiszesza_baleset = []
        aktualis_haszon_vasutiszesza_baleset = b11

        for t in range(1, referencia_idoszak):
            if t == 1:
                haszon_vasutiszesza_baleset = b11
            else:
                haszon_vasutiszesza_baleset = aktualis_haszon_vasutiszesza_baleset * forgalom_novekedes * gdp_novekedese
                aktualis_haszon_vasutiszesza_baleset = haszon_vasutiszesza_baleset

            if t in baleseti_evek:
                ujhaszon_vasutiszesza_baleset = haszon_vasutiszesza_baleset
            else:
                ujhaszon_vasutiszesza_baleset = 0.0

            pv_vasutiszesza_baleset = ujhaszon_vasutiszesza_baleset / (diszkontrata ** t)
            jelenertekek_vasutiszesza_baleset.append(pv_vasutiszesza_baleset)
            tarsadalmi_hasznok_vasutiszesza_baleset.append(ujhaszon_vasutiszesza_baleset)
        osszes_tarsadalmihaszon_vasutiszesza_baleset = sum(tarsadalmi_hasznok_vasutiszesza_baleset)
        osszes_jelenertek_vasutiszesza_baleset = sum(jelenertekek_vasutiszesza_baleset)

        if st.button("RE-ből származó társadalmi költségek/hasznok a személyvonatok késésére nézve",
                     use_container_width=True, key="vasutiszesza_gomb1"):
            with st.container(border=True):
                st.metric(label=f"Az összes haszon",
                          value=f"{fmt(osszes_tarsadalmihaszon_vasutiszesza_baleset)} forint társadalmi haszon")
                st.metric(label=f"Az összes diszkontált haszon",
                          value=f"{fmt(osszes_jelenertek_vasutiszesza_baleset)} Forint nettó jelenértékű haszon.")

        evek_szama_3 = len(tarsadalmi_hasznok_vasutiszesza_baleset)
        with st.expander("Éves társadalmi hasznok a RE-ből a személyvonatok utasaira nézve", key="vasutiszesza_gomb2"):
            df_haszon_3 = pd.DataFrame({"Év (t): ": [f"{i + 1}. év" for i in range(evek_szama_3)],
                                        "Társadalmi haszon (Ft)": [f"{fmt(x)} Ft" for x in
                                                                   tarsadalmi_hasznok_vasutiszesza_baleset],
                                        "Diszkontált haszon (Ft)": [f"{fmt(x)} Ft" for x in
                                                                    jelenertekek_vasutiszesza_baleset], })
            st.dataframe(df_haszon_3, use_container_width=True, hide_index=True)

with tab4:
    col_1, = st.columns(1)
    with col_1:
        erintett_vonatok_teher_rendkivuli = st.number_input(
            "Hány teherszállító vonatot érint egy rendkívüli esemény?", step=1.0,
            help="[db vonat/esemény]")
    col_2, = st.columns(1)
    with col_2:
        atlagos_keses_teher = st.number_input(
            "Mekkora az átlagos késése egy teherszállító vonatnak egy rendkívüli esesménynél?", step=1.0, help="[perc/esemény]")

    napi_atlagos_aru = float(st.session_state.get("napi_atlagos_aru", 0.0))

    arutonna_fajlagoskoltseg_2026 = 311.1

    erintett_aruk_rendkivuli_SZESZA = (erintett_vonatok_teher_rendkivuli * (
                atlagos_keses_teher / 60)) * napi_atlagos_aru
    elsoevi_tarsadalmikoltseg_rendkivuli_vasutiteher = erintett_aruk_rendkivuli_SZESZA * arutonna_fajlagoskoltseg_2026

    with st.container(border=True):
        st.write(f"A rendkívüli esemény {round(erintett_vonatok_teher_rendkivuli, 1)} db tehervonatot érintett.")
        st.write(f"A rendkívüli esemény {round(erintett_aruk_rendkivuli_SZESZA, 1)} tonna árut érintett.")
        st.write(f"Az átlagos késés {round(atlagos_keses_teher, 1)} perc.")
        st.metric(
            label=f"Egy rendkívüli esemény során a tehervonatok késéséből keletkezett társadalmi költség",
            value=f"{fmt(elsoevi_tarsadalmikoltseg_rendkivuli_vasutiteher)} Forint.")

    b12 = elsoevi_tarsadalmikoltseg_rendkivuli_vasutiteher
    jelenertekek_vasutiteher_baleset = []
    tarsadalmi_hasznok_vasutiteher_baleset = []
    aktualis_haszon_vasutiteher_baleset = b12

    for t in range(1, referencia_idoszak):
        if t == 1:
            haszon_vasutiteher_baleset = b11
        else:
            haszon_vasutiteher_baleset = aktualis_haszon_vasutiteher_baleset * forgalom_novekedes
            aktualis_haszon_vasutiteher_baleset = haszon_vasutiteher_baleset

        if t in baleseti_evek:
            ujhaszon_vasutiteher_baleset = haszon_vasutiteher_baleset
        else:
            ujhaszon_vasutiteher_baleset = 0.0

        pv_vasutiteher_baleset = ujhaszon_vasutiteher_baleset / (diszkontrata ** t)
        jelenertekek_vasutiteher_baleset.append(pv_vasutiteher_baleset)
        tarsadalmi_hasznok_vasutiteher_baleset.append(ujhaszon_vasutiteher_baleset)
    osszes_tarsadalmihaszon_vasutiteher_baleset = sum(tarsadalmi_hasznok_vasutiteher_baleset)
    osszes_jelenertek_vasutiteher_baleset = sum(jelenertekek_vasutiteher_baleset)

    if st.button("RE-ből származó társadalmi költségek/hasznok a tehervonatok késésére nézve",
                 use_container_width=True, key="vasutiteher_gomb1"):
        with st.container(border=True):
            st.metric(label=f"Az összes haszon",
                      value=f"{fmt(osszes_tarsadalmihaszon_vasutiteher_baleset)} forint társadalmi haszon")
            st.metric(label=f"Az összes diszkontált haszon",
                      value=f"{fmt(osszes_jelenertek_vasutiteher_baleset)} Forint nettó jelenértékű haszon.")

    evek_szama_4 = len(tarsadalmi_hasznok_vasutiteher_baleset)
    with st.expander("Éves társadalmi hasznok a RE-ből a tehervonatok késésére nézve", key="vasutiteher_gomb2"):
        df_haszon_4 = pd.DataFrame({"Év (t): ": [f"{i + 1}. év" for i in range(evek_szama_4)],
                                    "Társadalmi haszon (Ft)": [f"{fmt(x)} Ft" for x in
                                                               tarsadalmi_hasznok_vasutiteher_baleset],
                                    "Diszkontált haszon (Ft)": [f"{fmt(x)} Ft" for x in
                                                                jelenertekek_vasutiteher_baleset], })
        st.dataframe(df_haszon_4, use_container_width=True, hide_index=True)
