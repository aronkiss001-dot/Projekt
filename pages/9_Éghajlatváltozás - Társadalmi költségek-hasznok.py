import streamlit as st
import pandas as pd

st.markdown("""<style>div[data-testid="stMetricValue"] {font-size: 30px !important;}</style>""", unsafe_allow_html=True)
st.markdown("<h1 style = 'text-align: center;'>Éghajlatváltozásból származó társadalmi költségek/hasznok</style>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(['Járművek várakozásából származó ózonszennyezés', 'Járművek többlet-futásteljesítményéből származó ózonszennyezés'])

def fmt(ertek):
    return f"{ertek:,.0f}".replace(",", " ")

egyenertekes_futasteljesitmeny_auto = float(st.session_state.get('egyenertekes_futasteljesitmeny_auto', 0.0))
egyenertekes_futasteljesitmeny_kamion = float(st.session_state.get('egyenertekes_futasteljesitmeny_kamion', 0.0))
referencia_idoszak = int(st.session_state.get('referencia_idoszak', 30))

with tab1:
    fajlagos_arnyekar_2026 = 50.688
    fajlagoskar_auto_eghajlatvaltozas = fajlagos_arnyekar_2026 * 0.180
    fajlagoskar_kamion_eghajlatvaltozas = fajlagos_arnyekar_2026 * 0.848
    col_1, = st.columns(1)
    with col_1:
        st.write("A fajlagos árnyékár 2026-ra vonatkozóan 50,688 Ft/kg CO2 kibocsátási költséget jelent.")
    col_2, = st.columns(1)
    with col_2:
        st.write("Egy személygépjármű 180 g CO2-t, egy tehergépjármű 848 g CO2-t emittál egy km megtétele alatt.")
    eves_eghajlatvaltoasi_haszon = (egyenertekes_futasteljesitmeny_auto * fajlagoskar_auto_eghajlatvaltozas) + (
                egyenertekes_futasteljesitmeny_kamion * fajlagoskar_kamion_eghajlatvaltozas)

    with st.container(border=True):
        st.metric(label=f"Az első évben a járművek várakozásából keletkező társadalmi haszon az ózonszennyezés externális hatásából", value=f"{fmt(eves_eghajlatvaltoasi_haszon)} forint.")

    forgalom_novekedes = 1.015
    gdp_novekedese = 1.029
    diszkontrata = 1.030

    b14 = eves_eghajlatvaltoasi_haszon

    jelenertekek_eghajlatvaltozas_varakozas = []
    tarsadalmi_hasznok_eghajlatvaltozas_varakozas = []
    aktualis_haszon_eghajlatvaltozas_varakozas = b14

    for t in range(1, referencia_idoszak):
        if t == 1:
            haszon_eghajlatvaltozas_varakozas = b14
        else:
            haszon_eghajlatvaltozas_varakozas = aktualis_haszon_eghajlatvaltozas_varakozas * forgalom_novekedes
            aktualis_haszon_eghajlatvaltozas_varakozas = haszon_eghajlatvaltozas_varakozas

        pv_eghajlatvaltozas_varakozas = haszon_eghajlatvaltozas_varakozas / (diszkontrata ** t)
        jelenertekek_eghajlatvaltozas_varakozas.append(pv_eghajlatvaltozas_varakozas)
        tarsadalmi_hasznok_eghajlatvaltozas_varakozas.append(haszon_eghajlatvaltozas_varakozas)
    osszes_tarsadalmi_haszon_eghajlatvaltozas_varakozas = sum(tarsadalmi_hasznok_eghajlatvaltozas_varakozas)
    osszes_diszkontalt_haszon_eghajlatvaltozas_varakozas = sum(jelenertekek_eghajlatvaltozas_varakozas)

    if st.button("A járművek várakozásából adódó ózonszennyezés költsége/haszna a referencia időszakban", use_container_width=True):
        with st.container(border=True):
            st.metric(label=f"Az összes haszon", value=f"{fmt(osszes_tarsadalmi_haszon_eghajlatvaltozas_varakozas)} forint társadalmi haszon")
            st.metric(label=f"Az összes diszkontált haszon", value=f"{fmt(osszes_diszkontalt_haszon_eghajlatvaltozas_varakozas)} Forint nettó jelenértékű haszon.")

    evek_szama = len(tarsadalmi_hasznok_eghajlatvaltozas_varakozas)
    with st.expander("\n--- Éves társadalmi hasznok a járművek várakozásából adódó ózonszennyezésre nézve ---"):
        df_haszon_eghajlatvaltozas = pd.DataFrame({"Év (t): ": [f"{i+1}. év" for i in range(evek_szama)], "Társadalmi haszon (Ft)": [f"{fmt(x)} Ft" for x in tarsadalmi_hasznok_eghajlatvaltozas_varakozas], "Diszkontált haszon (Ft)": [f"{fmt(x)} Ft" for x in jelenertekek_eghajlatvaltozas_varakozas]})
        st.dataframe(df_haszon_eghajlatvaltozas, use_container_width=True, hide_index=True)
