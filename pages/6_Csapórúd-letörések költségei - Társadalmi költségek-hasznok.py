import streamlit as st
import pandas as pd

st.markdown("""<style>div[data-testid="stMetricValue"] {font-size: 30px !important;}</style>""", unsafe_allow_html=True)
st.markdown("<h1 style = 'text-align: center;'>Csapórúd-letörésekből származó anyagköltségek</style>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(['Csapórúd-letörésekből származó anyagköltség', 'Csapórúd-letörésekből származó többlet-üzemanyagköltség'])

csaporud_tores = float(st.session_state.get("csaporud_tores", 0.0))
anyagkoltseg = 95000
evi_anyagkoltseg = anyagkoltseg * csaporud_tores

def fmt(ertek):
    return f"{ertek:,.0f}".replace(",", " ")

with tab1:
    with st.container(border=True):
        st.write("Egy csapórúd-letörés során az anyagköltség átlagosan 95 000 Ft.")
        st.metric(label="Az 1. évben a csapórudak-letöréséből összesen", value=f"{fmt(evi_anyagkoltseg)} Forint kár keletkezik.")

    forgalom_novekedes = 1.015
    gdp_novekedese = 1.029
    diszkontrata = 1.030

    b7 = evi_anyagkoltseg
    jelenertekek_csaporud = []
    tarsadalmihasznok_csaporud = []
    aktualis_haszon_csaporud = b7

    referencia_idoszak = int(st.session_state.get("referencia_idoszak", 30))

    for t in range(1, referencia_idoszak):
        if t == 1:
            haszon_csaporud = b7
        else:
            haszon_csaporud = aktualis_haszon_csaporud * forgalom_novekedes
            aktualis_haszon_csaporud = haszon_csaporud

        pv_csaporud = haszon_csaporud / (diszkontrata ** t)
        jelenertekek_csaporud.append(pv_csaporud)
        tarsadalmihasznok_csaporud.append(haszon_csaporud)
    osszes_tarsadalmihaszon_csaporud = sum(tarsadalmihasznok_csaporud)
    osszes_jelenertek_csaporud = sum(jelenertekek_csaporud)

    if st.button("A csapórúd-letörésekből származó anyagköltség/haszon a teljes-referencia_időszakban", use_container_width = True):
        with st.container(border=True):
            st.metric(label=f"Az összes haszon", value=f"{fmt(osszes_tarsadalmihaszon_csaporud)} forint társadalmi haszon")
            st.metric(label=f"Az összes diszkontált haszon", value=f"{fmt(osszes_jelenertek_csaporud)} Forint nettó jelenértékű haszon.")

    evek_szama = len(tarsadalmihasznok_csaporud)
    with st.expander("Éves társadalmi hasznok a csapórúd-letörések anyagköltségére nézve"):
        df_haszon = pd.DataFrame({"Év (t): ": [f"{i+1}. év" for i in range(evek_szama)], "Társadalmi haszon (Ft)": [f"{fmt(x)} Ft" for x in tarsadalmihasznok_csaporud], "Diszkontált haszon (Ft)": [f"{fmt(x)} Ft" for x in jelenertekek_csaporud]})
        st.dataframe(df_haszon, use_container_width=True, hide_index=True)

with tab2:
    col_1, = st.columns(1)
    with col_1:
        keszenlet_tavolsag = st.number_input("A készenléti szolgálat mekkora távolságot tesz meg rendkívüli esemény bekövetkeztekor?", help="[km]")
    col_2, col_3 = st.columns([1, 1])
    with col_2:
        piaci_arszabas = st.number_input("Mekkora a piaci árszabása a készenléti szolgálat által használt jármű tüzelőanyagának?", help="[Ft/l]")
    with col_3:
        atlagfogyasztas_MAV = st.number_input("Mekkora az átlagfogyasztása a készenléti szolgálat által használt járműnek?", help="[l/100km]")

    fajlagos_uzemanyagkoltseg_MAV = (atlagfogyasztas_MAV / 100) * piaci_arszabas
    uzemanyagkoltseg_1 = fajlagos_uzemanyagkoltseg_MAV * keszenlet_tavolsag
    uzemanyagkoltseg_ev = uzemanyagkoltseg_1 * csaporud_tores

    if st.button("A készenléti szolgálat többlet-futásteljesítményének monetizálása", use_container_width=True):
        with st.container(border=True):
            st.metric(label=f"Az első évben a készenléti szolgálat többlet-futásteljesítményéből", value=f"{fmt(uzemanyagkoltseg_ev)} forint üzemanyagköltség keletkezik.")

    b8 = uzemanyagkoltseg_ev

    jelenertekek_uzemanyagMAV = []
    tarsadalmi_haszon_uzemanyagMAV = []
    aktualis_haszon_uzemanyagMAV = b8

    for t in range(1, referencia_idoszak):
        if t == 1:
            haszon_uzemanyagMAV = b8
        else:
            haszon_uzemanyagMAV = aktualis_haszon_uzemanyagMAV * forgalom_novekedes
            aktualis_haszon_uzemanyagMAV = haszon_uzemanyagMAV

        pv_uzemanyagMAV = haszon_uzemanyagMAV / (diszkontrata ** t)
        jelenertekek_uzemanyagMAV.append(pv_uzemanyagMAV)
        tarsadalmi_haszon_uzemanyagMAV.append(haszon_uzemanyagMAV)
        osszes_tarasdalmihaszon_uzemanyagMAV = sum(tarsadalmi_haszon_uzemanyagMAV)
        osszes_jelenertek_uzemanyagMAV = sum(jelenertekek_uzemanyagMAV)

    if st.button("A készenléti szolgálat többlet-futásteljesítményéből származó üzemanyagköltség a referencia-időszakban", use_container_width = True):
        with st.container(border=True):
            st.metric(label=f"Az összes haszon", value=f"{fmt(osszes_tarasdalmihaszon_uzemanyagMAV)} forint társadalmi haszon")
            st.metric(label=f"Az összes diszkontált haszon", value=f"{fmt(osszes_jelenertek_uzemanyagMAV)} Forint nettó jelenértékű haszon.")

    evek_szama = len(tarsadalmi_haszon_uzemanyagMAV)
    with st.expander("\n--- Éves társadalmi hasznok a készenléti szolgálat többlet-futásteljesítményére nézve ---"):
        df_haszon_2 = pd.DataFrame({"Év (t): ": [f"{i+1}. év" for i in range(evek_szama)], "Társadalmi haszon (Ft)": [f"{fmt(x)} Ft" for x in tarsadalmi_haszon_uzemanyagMAV], "Diszkontált haszon (Ft)": [f"{fmt(x)} Ft" for x in jelenertekek_uzemanyagMAV]})
        st.dataframe(df_haszon_2, use_container_width=True, hide_index=True)