import streamlit as st
import pandas as pd

st.markdown("""<style>div[data-testid="stMetricValue"] {font-size: 30px !important;}</style>""", unsafe_allow_html=True)
st.markdown("<h1 style = 'text-align: center;'>Zajszennyezésből származó társadalmi költségek/hasznok</style>", unsafe_allow_html=True)

def fmt(ertek):
    return f"{ertek:,.0f}".replace(",", " ")

szemelygepjarmu = float(st.session_state.get("szemelygepjarmu", 0.0))
teher_celevre = float(st.session_state.get("teher_celevre", 0.0))
egyenertekes_futasteljesitmeny_auto = float(st.session_state.get('egyenertekes_futasteljesitmeny_auto', 0.0))
teher_osszesen = float(st.session_state.get("teher_osszesen", 0.0))
egyenertekes_futasteljesitmeny_kamion = float(st.session_state.get('egyenertekes_futasteljesitmeny_kamion', 0.0))
referencia_idoszak = int(st.session_state.get("referencia_idoszak", 30))

tab1, = st.tabs(['Járművek várakozásából származó zajszennyezés'])
nappali_autok = szemelygepjarmu * (14/24)
ejszakai_autok = szemelygepjarmu * (10/24)
atlagos_zajkar = ((nappali_autok * 0.105) + (ejszakai_autok * 0.195)) / szemelygepjarmu if szemelygepjarmu > 0 else 0.0
atlagos_zajkar_korrigalva = atlagos_zajkar * (0.01 * 1.3287 * 384)
zajkar_autok = egyenertekes_futasteljesitmeny_auto * atlagos_zajkar_korrigalva
nappali_kamion = (teher_osszesen) * (14/24)
ejszaka_kamion = teher_osszesen * (10/24)
atlagos_zajkar_teher = ((nappali_kamion * 1.62) + (ejszaka_kamion * 3.06)) / teher_osszesen if teher_osszesen > 0 else 0.0
atlagos_zajkar_teher_korrigalva = atlagos_zajkar_teher * (0.01 * 1.3287 * 384)
zajkar_teher = egyenertekes_futasteljesitmeny_kamion * atlagos_zajkar_teher_korrigalva
zajkar_osszesen = zajkar_autok + zajkar_teher

with tab1:
    with st.container(border=True):
        st.metric(label=f"A személygépjárművek várakozására eső éves zajterhelési kár", value=f"{fmt(zajkar_autok)} Ft/év.")
        st.metric(label=f"A tehergépjárművek várakozására eső éves zajterhelési kár", value=f"{fmt(zajkar_teher)} Ft/év.")

    forgalom_novekedes = 1.015
    gdp_novekedese = 1.029
    diszkontrata = 1.030

    b17 = zajkar_osszesen

    jelenertekek_zajkar_varakozas = []
    tarsadalmi_hasznok_zajkar_varakozas = []
    aktualis_haszon_zajkar_varakozas = b17

    for t in range(1, referencia_idoszak):
        if t == 1:
            haszon_zajkar_varakozas = b17
        else:
            haszon_zajkar_varakozas = aktualis_haszon_zajkar_varakozas * forgalom_novekedes
            aktualis_haszon_zajkar_varakozas = haszon_zajkar_varakozas

        pv_zajkar_varakozas = haszon_zajkar_varakozas / (diszkontrata ** t)
        jelenertekek_zajkar_varakozas.append(pv_zajkar_varakozas)
        tarsadalmi_hasznok_zajkar_varakozas.append(haszon_zajkar_varakozas)
    osszes_tarsadalmi_haszon_zajkar_varakozas = sum(tarsadalmi_hasznok_zajkar_varakozas)
    osszes_diszkontalt_haszon_zajkar_varakozas = sum(jelenertekek_zajkar_varakozas)

    if st.button("A járművek várakozásából adódó zajszennyezés költsége/haszna a referencia időszakban", use_container_width=True):
        with st.container(border=True):
            st.metric(label=f"Az összes haszon", value=f"{fmt(osszes_tarsadalmi_haszon_zajkar_varakozas)} forint társadalmi haszon")
            st.metric(label=f"Az összes diszkontált haszon", value=f"{fmt(osszes_diszkontalt_haszon_zajkar_varakozas)} Forint nettó jelenértékű haszon.")

    evek_szama = len(tarsadalmi_hasznok_zajkar_varakozas)
    with st.expander("\n--- Éves társadalmi hasznok a járművek várakozásából adódó ózonszennyezésre nézve ---"):
        df_haszon_eghajlatvaltozas = pd.DataFrame({"Év (t): ": [f"{i+1}. év" for i in range(evek_szama)], "Társadalmi haszon (Ft)": [f"{fmt(x)} Ft" for x in tarsadalmi_hasznok_zajkar_varakozas], "Diszkontált haszon (Ft)": [f"{fmt(x)} Ft" for x in jelenertekek_zajkar_varakozas]})
        st.dataframe(df_haszon_eghajlatvaltozas, use_container_width=True, hide_index=True)
