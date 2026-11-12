import streamlit as st
import pandas as pd

st.markdown("""<style>div[data-testid="stMetricValue"] {font-size: 30px !important;}</style>""", unsafe_allow_html=True)
st.markdown("<h1 style = 'text-align: center;'>Légszennyezésből származó társadalmi költségek/hasznok</style>", unsafe_allow_html=True)

szemelygepjarmu = float(st.session_state.get('szemelygepjarmu', 0.0))
atlagos_varakozasi_ido = float(st.session_state.get('atlagos_varakozasi_ido', 0.0))
teher_osszesen = float(st.session_state.get('teher_osszesen', 0.0))
referencia_idoszak = int(st.session_state.get('referencia_idoszak', 30))
teher_celevre = float(st.session_state.get('teher_celevre', 0.0))
forgalomkorlatozas_rendkivuli = float(st.session_state.get('forgalomkorlatozas_rendkivuli', 0.0))
tobbletkm_rendkivuli = float(st.session_state.get('tobbletkm_rendkivuli', 0.0))
if 'egyenertekes_futasteljesitmeny_auto' not in st.session_state:
    st.session_state['egyenertekes_futasteljesitmeny_auto'] = 0.0
if 'egyenertekes_futasteljesitmeny_kamion' not in st.session_state:
    st.session_state['egyenertekes_futasteljesitmeny_kamion'] = 0.0

tab1, tab2 = st.tabs(['Járművek várakozásából származó légszennyezés', 'Járművek többlet-futásteljesítményéből származó légszennyezés'])

def fmt(ertek):
    return f"{ertek:,.0f}".replace(",", " ")

with tab1:
    col_1, = st.columns(1)
    with col_1:
        szemelygepjarmu_atlagfogyasztas = st.number_input("Mekkora a személygépjárművek átlagfogyasztása?", value = 614.0, step=0.1, help="[l/100km]", format="%.1f")
    col_2, = st.columns(1)
    with col_2:
        tehergepjarmu_atlagfogyasztas = st.number_input("Mekkora a tehergépjárművek átlagfogyasztása (l/100km)?", value= 22.5, step=0.1, help="[km]", format="%.1f")

    szemelygepjarmu_fajlagosertek_externalia = 0.68  # eurócent/jkm
    tehergepjarmu_fajlagosertek_externalia = 3.65  # eurócent/jkm
    idoveszteseg_szemelygepjarmu = (szemelygepjarmu * (atlagos_varakozasi_ido / 60)) * 365  # 131 400
    idoveszteseg_tehergepjarmu = ((teher_osszesen / 2.5) * (atlagos_varakozasi_ido / 60)) * 365  # 20 440

    alapjarati_uzemanyagveszteseg_auto = idoveszteseg_szemelygepjarmu * 0.78  # 102 492
    alapjarati_uzemanyagveszteseg_kamion = idoveszteseg_tehergepjarmu * 4.95  # 101 178

    egyenertekes_futasteljesitmeny_auto = alapjarati_uzemanyagveszteseg_auto / (szemelygepjarmu_atlagfogyasztas / 100)
    egyenertekes_futasteljesitmeny_kamion = alapjarati_uzemanyagveszteseg_kamion / (tehergepjarmu_atlagfogyasztas / 100)
    eves_legszennyezesi_haszon_auto = egyenertekes_futasteljesitmeny_auto * szemelygepjarmu_fajlagosertek_externalia
    eves_legszennyezesi_haszon_kamion = egyenertekes_futasteljesitmeny_kamion * tehergepjarmu_fajlagosertek_externalia
    eves_legszennyezesi_haszon = ((eves_legszennyezesi_haszon_auto / 100) + (eves_legszennyezesi_haszon_kamion / 100)) * 365

    st.session_state['egyenertekes_futasteljesitmeny_auto'] = egyenertekes_futasteljesitmeny_auto
    st.session_state['egyenertekes_futasteljesitmeny_kamion'] = egyenertekes_futasteljesitmeny_kamion

    with st.container(border=True):
        st.metric(label=f"Az első évben a járművek várakozásából keletkező társadalmi haszon a légszennyezés externális hatásából", value=f"{fmt(eves_legszennyezesi_haszon)} forint.")

    forgalom_novekedes = 1.015
    gdp_novekedese = 1.029
    diszkontrata = 1.030

    b13 = eves_legszennyezesi_haszon

    jelenertekek_legszennyezes_varakozas = []
    tarsadalmi_hasznok_legszennyezes_varakozas = []
    aktualis_haszon_legszennyezes_varakozas = b13

    for t in range(1, referencia_idoszak):
        if t == 1:
            haszon_legszennyezes_varakozas = b13
        else:
            haszon_legszennyezes_varakozas = aktualis_haszon_legszennyezes_varakozas * forgalom_novekedes
            aktualis_haszon_legszennyezes_varakozas = haszon_legszennyezes_varakozas

        pv_legszennyezes_varakozas = haszon_legszennyezes_varakozas / (diszkontrata ** t)
        jelenertekek_legszennyezes_varakozas.append(pv_legszennyezes_varakozas)
        tarsadalmi_hasznok_legszennyezes_varakozas.append(haszon_legszennyezes_varakozas)
    osszes_tarsadalmi_haszon_legszennyezes_varakozas = sum(tarsadalmi_hasznok_legszennyezes_varakozas)
    osszes_diszkontalt_haszon_legszennyezes_varakozas = sum(jelenertekek_legszennyezes_varakozas)


    if st.button("A járművek várakozásából adódó légszennyezés költsége/haszna a referencia időszakban", use_container_width=True):
        with st.container(border=True):
            st.metric(label=f"Az összes haszon", value=f"{fmt(osszes_tarsadalmi_haszon_legszennyezes_varakozas)} forint társadalmi haszon")
            st.metric(label=f"Az összes diszkontált haszon", value=f"{fmt(osszes_diszkontalt_haszon_legszennyezes_varakozas)} Forint nettó jelenértékű haszon.")

    evek_szama = len(tarsadalmi_hasznok_legszennyezes_varakozas)
    with st.expander("\n--- Éves társadalmi hasznok a járművek várakozásából adódó légszennyezésre nézve ---"):
        df_haszon_legszennyezes = pd.DataFrame({"Év (t): ": [f"{i+1}. év" for i in range(evek_szama)], "Társadalmi haszon (Ft)": [f"{fmt(x)} Ft" for x in tarsadalmi_hasznok_legszennyezes_varakozas], "Diszkontált haszon (Ft)": [f"{fmt(x)} Ft" for x in jelenertekek_legszennyezes_varakozas]})
        st.dataframe(df_haszon_legszennyezes, use_container_width=True, hide_index=True)

with tab2:
    erintett_szgk_rendkivuli = szemelygepjarmu * (forgalomkorlatozas_rendkivuli / 24)
    erintett_teher_rendkivuli = (teher_celevre / 2.5) * (forgalomkorlatozas_rendkivuli / 24)
    tobbletfutas_auto = erintett_szgk_rendkivuli * tobbletkm_rendkivuli
    tobbletfutas_kamion = erintett_teher_rendkivuli * tobbletkm_rendkivuli

    col_1, = st.columns(1)
    with col_1:
        st.metric(label = f"A forgalomkorlátozás",value=f"{round(erintett_szgk_rendkivuli, 0)} db személygépjárművet érintett.", help="A 7. oldalon megadott adatok alapján")
    col_2, = st.columns(1)
    with col_2:
        st.metric(label = f"A forgalomkorlátozás",value=f"{round(erintett_teher_rendkivuli, 0)} db tehergépjárművet érintett.", help="A 7. oldalon megadott adatok alapján")

    with st.container(border=True):
        st.metric(label = f"A személygépjárművek többletfutása", value=f"{round(tobbletfutas_auto, 1)} km, a tehergépjárműveké {round(tobbletfutas_kamion, 1)} km.", help="A 7. oldalon megadott adatok alapján")

    eves_legszennyezesi_haszon_tobbletfutas = (tobbletfutas_auto * szemelygepjarmu_fajlagosertek_externalia) + (
                tobbletfutas_kamion * tehergepjarmu_fajlagosertek_externalia)

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

    b14 = eves_legszennyezesi_haszon_tobbletfutas

    jelenertekek_legszennyezes_tobbletfutas = []
    tarsadalmi_hasznok_legszennyezes_tobbletfutas = []
    aktualis_haszon_legszennyezes_tobbletfutas = b14

    for t in range(1, referencia_idoszak):
        if t == 1:
            haszon_legszennyezes_tobbletfutas = b14
        else:
            haszon_legszennyezes_tobbletfutas = aktualis_haszon_legszennyezes_tobbletfutas * forgalom_novekedes
            aktualis_haszon_legszennyezes_tobbletfutas = haszon_legszennyezes_tobbletfutas

        if t in baleseti_evek:
            ujhaszon_legszennyezes_tobbletfutas = haszon_legszennyezes_tobbletfutas
        else:
            ujhaszon_legszennyezes_tobbletfutas = 0.0

        pv_legszennyezes_tobbletfutas = ujhaszon_legszennyezes_tobbletfutas / (diszkontrata ** t)
        jelenertekek_legszennyezes_tobbletfutas.append(pv_legszennyezes_tobbletfutas)
        tarsadalmi_hasznok_legszennyezes_tobbletfutas.append(ujhaszon_legszennyezes_tobbletfutas)
        osszes_tarsadalmihaszon_legszennyezes_tobbletfutas = sum(tarsadalmi_hasznok_legszennyezes_tobbletfutas)
        osszes_jelenertek_legszennyezes_tobbletfutas = sum(jelenertekek_legszennyezes_tobbletfutas)

    if st.button("A járművek várakozásából adódó légszennyezés költsége/haszna rendkívüli eseményeknél a referencia időszakban", use_container_width=True):
        with st.container(border=True):
            st.metric(label=f"Az összes haszon", value=f"{fmt(osszes_tarsadalmihaszon_legszennyezes_tobbletfutas)} forint társadalmi haszon")
            st.metric(label=f"Az összes diszkontált haszon", value=f"{fmt(osszes_jelenertek_legszennyezes_tobbletfutas)} Forint nettó jelenértékű haszon.")

    evek_szama_2 = len(tarsadalmi_hasznok_legszennyezes_tobbletfutas)
    with st.expander("\n--- Éves társadalmi hasznok a járművek várakozásából adódó légszennyezésre nézve ---"):
        df_haszon_legszennyezes_2 = pd.DataFrame({"Év (t): ": [f"{i+1}. év" for i in range(evek_szama_2)], "Társadalmi haszon (Ft)": [f"{fmt(x)} Ft" for x in tarsadalmi_hasznok_legszennyezes_tobbletfutas], "Diszkontált haszon (Ft)": [f"{fmt(x)} Ft" for x in jelenertekek_legszennyezes_tobbletfutas]})
        st.dataframe(df_haszon_legszennyezes_2, use_container_width=True, hide_index=True)

