import streamlit as st
import pandas as pd

st.markdown("""<style>div[data-testid="stMetricValue"] {font-size: 30px !important;}</style>""", unsafe_allow_html=True)
st.markdown("<h1 style = 'text-align: center;'>Baleseti kockázatváltozás monetizálása</style>", unsafe_allow_html=True)

tab1, = st.tabs(['Baleseti kockázatváltozás'])

feluljaro_hossz = float(st.session_state.get('feluljaro_hossz', 0.0))
szemelygepjarmu = float(st.session_state.get('szemelygepjarmu', 0.0))
teher_osszesen = float(st.session_state.get('teher_osszesen', 0.0))

fajlagos_balesetikoltseg_szgk = 55.14 # Ft/jkm
fajlagos_balesetikoltseg_teher = 56.14 # Ft/jkm

eves_futasteljesitmeny_szgk = 365 * szemelygepjarmu * (feluljaro_hossz / 1000)
eves_futasteljesitmeny_teher = 365 * (teher_osszesen / 2.5) * (feluljaro_hossz / 1000)

elsoevi_tarsadalmikoltseg_baleset = (fajlagos_balesetikoltseg_szgk * eves_futasteljesitmeny_szgk) + (fajlagos_balesetikoltseg_teher * eves_futasteljesitmeny_teher)

with tab1:
    with st.container(border=True):
        st.metric(label="A veszélyeztetett keresztmetszet hossza:", value=f"{feluljaro_hossz} méter", help="A megadott felüljáró hossza")
        st.write(f"A személygépjárművek fajlagos baleseti költsége {fajlagos_balesetikoltseg_szgk} Ft/járműkm.")
        st.write(f"A tehergépjárművek fajlagos baleseti költsége {fajlagos_balesetikoltseg_teher} Ft/járműkm.")

    def fmt(ertek):
        return f"{ertek:,.0f}".replace(",", " ")

    if st.button("Baleseti kockázatváltozás monetizálása", use_container_width=True):
        with st.container(border=True):
            st.metric(label=f"Az első évben a baleseti kockázat nullára csökkenéséből", value=f"{fmt(elsoevi_tarsadalmikoltseg_baleset)} forint társadalmi költség keletkezik.")

    forgalom_novekedes = 1.015
    gdp_novekedese = 1.029
    diszkontrata = 1.030

    b6 = elsoevi_tarsadalmikoltseg_baleset

    jelenertekek_baleset = []
    tarsadalmi_hasznok_baleset = []
    aktualis_haszon_baleset = b6

    referencia_idoszak = int(st.session_state.get("referencia_idoszak", 30))

    for t in range(1, referencia_idoszak):
        if t == 1:
            haszon_baleset = b6
        else:
            haszon_baleset = aktualis_haszon_baleset * forgalom_novekedes * gdp_novekedese
            aktualis_haszon_baleset = haszon_baleset

        pv_baleset = haszon_baleset / (diszkontrata ** t)
        jelenertekek_baleset.append(pv_baleset)
        tarsadalmi_hasznok_baleset.append(haszon_baleset)
    osszes_tarsadalmihaszon_baleset = sum(tarsadalmi_hasznok_baleset)
    osszes_jelenertek_baleset = sum(jelenertekek_baleset)

    if st.button("A baleseti kockázat nullára csökkenéséből származó összes társadalmi haszon/költség a referencia-időszakban", use_container_width = True):
        with st.container(border=True):
            st.metric(label=f"Az összes haszon", value=f"{fmt(osszes_tarsadalmihaszon_baleset)} forint társadalmi haszon")
            st.metric(label=f"Az összes diszkontált haszon", value=f"{fmt(osszes_jelenertek_baleset)} Forint nettó jelenértékű haszon.")

    evek_szama = len(tarsadalmi_hasznok_baleset)
    with st.expander("\n--- Éves társadalmi hasznok a baleseti kockázatváltozásra nézve ---"):
        df_haszon = pd.DataFrame({"Év (t): ": [f"{i+1}. év" for i in range(evek_szama)], "Társadalmi haszon (Ft)": [f"{fmt(x)} Ft" for x in tarsadalmi_hasznok_baleset], "Diszkontált haszon (Ft)": [f"{fmt(x)} Ft" for x in jelenertekek_baleset]})
        st.dataframe(df_haszon, use_container_width=True, hide_index=True)
