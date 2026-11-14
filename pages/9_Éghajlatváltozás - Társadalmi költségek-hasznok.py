import streamlit as st
import pandas as pd

st.markdown("""<style>div[data-testid="stMetricValue"] {font-size: 30px !important;}</style>""", unsafe_allow_html=True)
st.markdown("<h1 style = 'text-align: center;'>Éghajlatváltozásból származó társadalmi költségek/hasznok</style>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(['Járművek várakozásából származó ózonszennyezés', 'Járművek többlet-futásteljesítményéből származó ózonszennyezés'])

def fmt(ertek):
    return f"{ertek:,.0f}".replace(",", " ")

szemelygepjarmu = float(st.session_state.get("szemelygepjarmu", 0.0))
teher_celevre = float(st.session_state.get("teher_celevre", 0.0))
forgalomkorlatozas_rendkivuli = float(st.session_state.get("forgalomkorlatozas_rendkivuli", 0.0))
tobbletkm_rendkivuli = float(st.session_state.get('tobbletkm_rendkivuli', 0.0))

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

with tab2:
    erintett_szgk_rendkivuli = szemelygepjarmu * (forgalomkorlatozas_rendkivuli / 24)
    erintett_teher_rendkivuli = (teher_celevre / 2.5) * (forgalomkorlatozas_rendkivuli / 24)
    tobbletfutas_auto = erintett_szgk_rendkivuli * tobbletkm_rendkivuli
    tobbletfutas_kamion = erintett_teher_rendkivuli * tobbletkm_rendkivuli
    eves_eghajlatvaltozasi_haszon_tobbletfutas = (tobbletfutas_auto * fajlagoskar_auto_eghajlatvaltozas) + (
                tobbletfutas_kamion * fajlagoskar_kamion_eghajlatvaltozas)

    col_1, = st.columns(1)
    with col_1:
        st.metric(label = f"A forgalomkorlátozás",value=f"{round(erintett_szgk_rendkivuli, 0)} db személygépjárművet érintett.", help="A 7. oldalon megadott adatok alapján")
    col_2, = st.columns(1)
    with col_2:
        st.metric(label = f"A forgalomkorlátozás",value=f"{round(erintett_teher_rendkivuli, 0)} db tehergépjárművet érintett.", help="A 7. oldalon megadott adatok alapján")

    with st.container(border=True):
        st.metric(label = f"A személygépjárművek többletfutása", value=f"{round(tobbletfutas_auto, 1)} km, a tehergépjárműveké {round(tobbletfutas_kamion, 1)} km.", help="A 7. oldalon megadott adatok alapján")

    baleseti_evek_input = st.text_input(label="Melyik években következik be baleset?", value="3, 8, 13, 18, 23, 28")
    if baleseti_evek_input.strip():
        try: baleseti_evek = [int(x.strip()) for x in baleseti_evek_input.split(",") if x.strip()]
        except ValueError:
            st.error("Kérjük, csak számokat adjon meg, vesszővel elválasztva")
            baleseti_evek = [3, 8, 13, 18, 23]
    else:
        baleseti_evek = [3, 8, 13, 18, 23, 28]

    if st.button("Baleseti évek listázása", use_container_width=True, key="baleseti_evek_vasutiszesza"):
        with st.container(border=True):
            st.metric(label=f"Baleseti kockázatvizsgálat a következő években:",
                      value=", ".join(str(x) for x in baleseti_evek))

    b16 = eves_eghajlatvaltozasi_haszon_tobbletfutas

    jelenertekek_eghajlatvaltozas_tobbletfutas = []
    tarsadalmi_hasznok_eghajlatvaltozas_tobbletfutas = []
    aktualis_haszon_eghajlatvaltozas_tobbletfutas = b16

    for t in range(1, referencia_idoszak):
        if t == 1:
            haszon_eghajlatvaltozas_tobbletfutas = b16
        else:
            haszon_eghajlatvaltozas_tobbletfutas = aktualis_haszon_eghajlatvaltozas_tobbletfutas * forgalom_novekedes
            aktualis_haszon_eghajlatvaltozas_tobbletfutas = haszon_eghajlatvaltozas_tobbletfutas

        if t in baleseti_evek:
            ujhaszon_eghajlatvaltozas_tobbletfutas = haszon_eghajlatvaltozas_tobbletfutas
        else:
            ujhaszon_eghajlatvaltozas_tobbletfutas = 0.0

        pv_eghajlatvaltozas_tobbletfutas = ujhaszon_eghajlatvaltozas_tobbletfutas / (diszkontrata ** t)
        jelenertekek_eghajlatvaltozas_tobbletfutas.append(pv_eghajlatvaltozas_tobbletfutas)
        tarsadalmi_hasznok_eghajlatvaltozas_tobbletfutas.append(ujhaszon_eghajlatvaltozas_tobbletfutas)
        osszes_tarsadalmihaszon_eghajlatvaltozas_tobbletfutas = sum(tarsadalmi_hasznok_eghajlatvaltozas_tobbletfutas)
        osszes_jelenertek_eghajlatvaltozas_tobbletfutas = sum(jelenertekek_eghajlatvaltozas_tobbletfutas)

    if st.button("A járművek várakozásából adódó ózonszennyezés költsége/haszna rendkívüli eseményeknél a referencia időszakban", use_container_width=True):
        with st.container(border=True):
            st.metric(label=f"Az összes haszon", value=f"{fmt(osszes_tarsadalmihaszon_eghajlatvaltozas_tobbletfutas)} forint társadalmi haszon")
            st.metric(label=f"Az összes diszkontált haszon", value=f"{fmt(osszes_jelenertek_eghajlatvaltozas_tobbletfutas)} Forint nettó jelenértékű haszon.")

    evek_szama_2 = len(tarsadalmi_hasznok_eghajlatvaltozas_tobbletfutas)
    with st.expander("\n--- Éves társadalmi hasznok a járművek várakozásából adódó ózonszennyezésre nézve ---"):
        df_haszon_eghajlatvaltozas_2 = pd.DataFrame({"Év (t): ": [f"{i+1}. év" for i in range(evek_szama_2)], "Társadalmi haszon (Ft)": [f"{fmt(x)} Ft" for x in tarsadalmi_hasznok_eghajlatvaltozas_tobbletfutas], "Diszkontált haszon (Ft)": [f"{fmt(x)} Ft" for x in jelenertekek_eghajlatvaltozas_tobbletfutas]})
        st.dataframe(df_haszon_eghajlatvaltozas_2, use_container_width=True, hide_index=True)


