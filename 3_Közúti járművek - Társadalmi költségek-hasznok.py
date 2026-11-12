import streamlit as st
import pandas as pd

st.markdown("<h1 style = 'text-align: center;'>Közúti járművek időnyereségének számszerűsítése és monetizálása</style>", unsafe_allow_html=True)
st.markdown("""<style>div[data-testid="stMetricValue"] {font-size: 30px !important;}</style>""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(['Személygépjárművek', 'Tehergépjárművek'])

szemely_celevre = float(st.session_state.get("szemely_celevre", 0.0))
atlag_zaras_perc = float(st.session_state.get("zarvatartas_ptc", 0.0))
osszes_zaras_min = float(st.session_state.get("osszes_zaras_min", 0.0))
teher_celevre = float(st.session_state.get("teher_celevre", 0.0))

if "atlagos_varakozasi_ido" not in st.session_state:
    st.session_state["atlagos_varakozasi_ido"] = 0

szemely_gepjarmu_szemelyek = szemely_celevre  * 1.5
atlagos_lezaras_veszteseggel = atlag_zaras_perc / 2
atlagos_varakozasi_ido = atlagos_lezaras_veszteseggel * osszes_zaras_min / 100
napi_varakozasi_ido = atlagos_varakozasi_ido * szemely_gepjarmu_szemelyek

st.session_state["atlagos_varakozasi_ido"] = atlagos_varakozasi_ido

uzleti_utazasingazas = 7457 # forint/utasóra
egyeb_utazas = 2613 # forint/utasóra
uzleti_utazasingazas_arany = szemely_gepjarmu_szemelyek * 0.25
egyeb_utazas_arany = szemely_gepjarmu_szemelyek * 0.75

uzleti_utazas_varakozas = (napi_varakozasi_ido / 60) * 0.25
egyeb_utazas_varakozas = (napi_varakozasi_ido / 60) * 0.75

teher_nemegysegjarmu = teher_celevre / 2.5
atlagos_lezaras_veszteseggel = atlag_zaras_perc / 2
atlagos_varakozasi_ido = atlagos_lezaras_veszteseggel * osszes_zaras_min / 100
napi_varakozasi_ido_teher = atlagos_varakozasi_ido * teher_nemegysegjarmu

teher_fajlagos_idoertek = 595 # forint/árutonnaóra
teher_rakomany = 18 # tonna
teher_rakomany_oraerteke = teher_rakomany * teher_fajlagos_idoertek # Ft/járműóra
napi_varakozas_teher = napi_varakozasi_ido / 60

elsoevi_tarsadalmikoltseg_teher = (napi_varakozas_teher * teher_rakomany_oraerteke) * 365

with tab1:

    if st.button("Személygépjárművek átlagos várakozási idejének meghatározása: ", use_container_width = True):
        with st.container(border=True):
            st.write(f"A személyenkénti átlagos várakozási idő {round(atlagos_varakozasi_ido, 2)} perc/személy")
            st.write(f"A napi összes várakozási idő {round(napi_varakozasi_ido, 2)} perc/nap")
            st.metric(label=f"Üzleti utazás/ingázás kategóriában a napi összes várakozás", value=f"{round(uzleti_utazas_varakozas, 2)} óra/nap", help="Üzleti utazás/ingázás fajlagos értéke: 7457 Ft/utasóra.")
            st.metric(label=f"Egyéb utazás kategóriában a napi összes várakozás", value=f"{round(egyeb_utazas_varakozas, 2)} óra/nap", help="Egyéb utazás fajlagos értéke = 2616 Ft/utasóra")

    elsoevi_tarsadalmikoltseg = ((uzleti_utazas_varakozas * uzleti_utazasingazas) + (egyeb_utazas_varakozas * egyeb_utazas)) * 365
    def fmt(ertek):
        return f"{ertek:,.0f}".replace(",", " ")

    if st.button("Személygépjárművek késéséből fakadó társadalmi költségek/hasznok: ", use_container_width = True):
        with st.container(border=True):
            st.metric(label=f"Az első évben a személygépjárművek várakozásából", value=f"{fmt(elsoevi_tarsadalmikoltseg)} forint társadalmi költség keletkezik.")

    forgalom_novekedes = 1.015
    gdp_novekedese = 1.029
    diszkontrata = 1.030

    b1 = elsoevi_tarsadalmikoltseg

    jelenertekek = []
    tarsadalmi_hasznok = []
    aktualis_haszon = b1

    referencia_idoszak = int(st.session_state.get("referencia_idoszak", 30))

    for t in range(1, referencia_idoszak):
        if t == 1:
            haszon_t = b1
        else:
            haszon_t = aktualis_haszon * forgalom_novekedes * gdp_novekedese
            aktualis_haszon = haszon_t

        pv_t = haszon_t / (diszkontrata ** t)
        jelenertekek.append(pv_t)
        tarsadalmi_hasznok.append(haszon_t)
    osszes_tarasdalmi_haszon = sum(tarsadalmi_hasznok)
    osszes_diszkontalt_haszon = sum(jelenertekek)

    if st.button("A személygépjárművek várakozásából adódó összes haszon a referencia-időszakban", use_container_width = True):
        with st.container(border=True):
            st.metric(label=f"Az összes haszon", value=f"{fmt(osszes_tarasdalmi_haszon)} forint társadalmi haszon")
            st.metric(label=f"Az összes diszkontált haszon", value=f"{fmt(osszes_diszkontalt_haszon)} Forint nettó jelenértékű haszon.")

    evek_szama = len(tarsadalmi_hasznok)
    with st.expander("\n--- Éves társadalmi hasznok a személygépjárművek várakozására nézve ---"):
        df_haszon = pd.DataFrame({"Év (t): ": [f"{i+1}. év" for i in range(evek_szama)], "Társadalmi haszon (Ft)": [f"{fmt(x)} Ft" for x in tarsadalmi_hasznok], "Diszkontált haszon (Ft)": [f"{fmt(x)} Ft" for x in jelenertekek]})
        st.dataframe(df_haszon, use_container_width=True, hide_index=True)

with tab2:
    if st.button("Tehergépjárművek átlagos várakozási idejének meghatározása: ", use_container_width=True):
        with st.container(border=True):
            st.write(f"A tehegépjárművek átlagos várakozási ideje {round(atlagos_varakozasi_ido, 2)} perc/jármű")
            st.write(f"A napi összes várakozási idő {round(napi_varakozas_teher, 2)} perc/nap")

    def fmt(ertek):
        return f"{ertek:,.0f}".replace(",", " ")
    
    if st.button("Tehergépjárművek késéséből fakadó társadalmi költségek/hasznok: ", use_container_width=True):
        with st.container(border=True):
            st.metric(label=f"Az első évben a tehergépjárművek várakozásából", value=f"{fmt(elsoevi_tarsadalmikoltseg_teher)} forint társadalmi költség keletkezik.", help="Áruszállítás fajlagos időértéke: 595 Ft/árutonnaóra; Átlagosan szállított rakomány: 18 tonna")

    forgalom_novekedes = 1.015
    gdp_novekedese_teher = 1.0
    diszkontrata = 1.030

    b2 = elsoevi_tarsadalmikoltseg_teher

    jelenertekek_teher = []
    tarsadalmi_hasznok_teher = []
    aktualis_haszon_teher = b2

    referencia_idoszak = int(st.session_state.get("referencia_idoszak", 30))

    for t in range(1, referencia_idoszak):
        if t == 1:
            haszon_teher = b2
        else:
            haszon_teher = aktualis_haszon_teher * forgalom_novekedes * gdp_novekedese_teher
            aktualis_haszon_teher = haszon_teher

        pv_teher = haszon_teher / (diszkontrata ** t)
        jelenertekek_teher.append(pv_teher)
        tarsadalmi_hasznok_teher.append(haszon_teher)
        osszes_tarasdalmi_haszon_teher = sum(tarsadalmi_hasznok_teher)
        osszes_diszkontalt_haszon_teher = sum(jelenertekek_teher)

    if st.button("A tehergépjárművek várakozásából adódó összes haszon a referencia-időszakban", use_container_width = True):
        with st.container(border=True):
            st.metric(label=f"Az összes haszon", value=f"{fmt(osszes_tarasdalmi_haszon_teher)} Ft társadalmi haszon.")
            st.metric(label=f"Az összes diszkontált haszon", value=f"{fmt(osszes_diszkontalt_haszon_teher)} Ft nettó jelenértékű haszon.")

    evek_szama_teher = len(tarsadalmi_hasznok_teher)
    with st.expander("\n--- Éves társadalmi hasznok a tehergépjárművek várakozására nézve ---"):
        df_haszon_teher = pd.DataFrame({"Év (t): ": [f"{i + 1}. év" for i in range(evek_szama_teher)], "Társadalmi haszon (Ft)": [f"{fmt(x)} Ft" for x in tarsadalmi_hasznok_teher],"Diszkontált haszon (Ft)": [f"{fmt(x)} Ft" for x in jelenertekek_teher]})
        st.dataframe(df_haszon_teher, use_container_width=True, hide_index=True)