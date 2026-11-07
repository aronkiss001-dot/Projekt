import streamlit as st
import pandas as pd
import plotly.express as px

st.markdown("<h1 style='text-align: center;'>Működési költség meghatározása", unsafe_allow_html=True)

st.markdown("""<style>div[data-testid="stMetricValue"] {font-size: 30px !important;}</style>""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Beruházási költség", "Üzemeltetési és fenntartási költség", "Pótlási költség", "Maradványérték", "Teljes működési költség"])

with tab1:

    col1, col2 = st.columns([1, 1])

    with col1:
        feluljaro_hossz = st.number_input("Mekkora a felüljáró tervezett hossza? (m): ",
        value = 367.0,
        step = 1.0,
        format = "%.1f")
        korforgalom_hossz = st.number_input("Mekkora a körforgalom kerülete? (m): ",
        value = 121.0,
        step = 1.0,
        format = "%.1f")

    with col2:
        kisajatitando_terulet = st.number_input("Mekkora a kisajátítandó zöldterület? (m2): ",
        value = 8000.0,
        step = 1.0,
        format = "%.1f")
        fairtas = st.number_input("Mekkora területen szükséges a fa- és bozótirtás? (m2): ",
        value = 6800.0,
        step = 1.0,
        format = "%.1f")

        fajlagos_zoldterulet_ara = 1990000 / 10000
        fajlagos_fairtas_ara = 515
        epitesi_koltseg_meterenkent =  7908719
        epitesi_koltseg_korforgalom = 2665289

    foldvasarlas_koltseg = kisajatitando_terulet * fajlagos_zoldterulet_ara
    fairtas_koltseg = fairtas * fajlagos_fairtas_ara
    feluljaro_epitesikoltseg = feluljaro_hossz * epitesi_koltseg_meterenkent
    korforgalom_epitesikoltseg = korforgalom_hossz * epitesi_koltseg_korforgalom

    teljes_beruhazasi_koltseg = foldvasarlas_koltseg + fairtas_koltseg + feluljaro_epitesikoltseg + korforgalom_epitesikoltseg

    st.divider()

    st.markdown("<h2 style='text-align: center;'>Beruházási Költség Eredményei</h2>", unsafe_allow_html=True)
    if st.button("Beruházási költség meghatározása", use_container_width=True):
        col_a, col_b, col_c = st.columns([1, 2, 1])
        with col_b:
            with st.container(border = True):
                st.metric(label = "Teljes beruházási költség (CAPEX)", value=f"{teljes_beruhazasi_koltseg:,.0f} Ft".replace(".", ","))
        st.write("")
        left_col, right_col = st.columns([1, 1])
        with left_col:
            st.subheader("Költségek megoszlása")
            df_koltseg = pd.DataFrame({"Tétel": ["Földvásárlás", "Faírtás", "Felüljáró építés", "Körforgalom építés"], "Összeg (Ft)": [foldvasarlas_koltseg, fairtas_koltseg,feluljaro_epitesikoltseg, korforgalom_epitesikoltseg], })
            fig = px.pie(df_koltseg, values = "Összeg (Ft)", names = "Tétel",hole=0.6, color_discrete_sequence = ['#2563EB', '#38BDF8', '#F59E0B', '#10B981'])
            fig.update_traces(
                textinfo='none',
                hovertemplate='<b>%{label}</b><br>Összeg: %{value:,.0f} Ft<br>Arány: %{percent}<extra></extra>'
            )
            fig.update_layout(
                font=dict(
                    family="Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif",
                    size=13,
                    color="#E5E7EB"
                ),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.25,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=12)
                ),
                margin=dict(t=20, b=40, l=20, r=20),
                paper_bgcolor='rgba(0,0,0,0)',  # Átlátszó háttér, hogy teljesen egybeolvadjon a filmmel
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)

        with right_col:
            st.subheader("Részletes tétellista")
            with st.container(border = True):
                st.write(f"• **Földvásárlás:** {foldvasarlas_koltseg:,.0f} Ft".replace(",", " "))
                st.write(f"• **Fairtás:** {fairtas_koltseg:,.0f} Ft".replace(",", " "))
                st.write(f"• **Felüljáró építése:** {feluljaro_epitesikoltseg:,.0f} Ft".replace(",", " "))
                st.write(f"• **Körforgalom építése:** {korforgalom_epitesikoltseg:,.0f} Ft".replace(",", " "))


with tab2:

    col3, = st.columns([1])

    with col3:
        projekt_referencia_idoszak = st.number_input(
            "Hány év a projekt referencia időszaka? (általánosan: 30 év) (év): ",
            value=30,
            step=1,
            format="%.1f")

        feluljaro_mukodesi_ertek = 114750000
        korforgalom_mukodesi_ertek = 4080000
        r = 0.03
        evek_szama = projekt_referencia_idoszak - 1

        feluljaro_mukodesi_koltseg = feluljaro_mukodesi_ertek * (feluljaro_hossz/1000)
        korforgalom_mukodesi_koltseg = korforgalom_mukodesi_ertek * (korforgalom_hossz/1000)
        teljes_mukodesi_koltseg = korforgalom_mukodesi_koltseg + feluljaro_mukodesi_koltseg
        teljes_mukodesi_koltseg_jelenertek = teljes_mukodesi_koltseg * (1-(1+0.03) ** -(projekt_referencia_idoszak - 1)) / 0.03

        feluljaro_utolsoev = feluljaro_mukodesi_koltseg * evek_szama
        korforgalom_utolsoev = korforgalom_mukodesi_koltseg * evek_szama
        teljes_utolsoev = teljes_mukodesi_koltseg * evek_szama

        faktor = (1 - (1 + r) ** -evek_szama) / r
        feluljaro_pv = feluljaro_mukodesi_koltseg * faktor
        korforglaom_pv = korforgalom_mukodesi_koltseg * faktor
        teljes_pv = teljes_mukodesi_koltseg * faktor

    with st.container(border=True):
        st.write("Egy felüljáró km-enkénti működési költsége 114 750 000 Ft/km/év.")
        st.write("Egy körforgalom km-enkénti működési költsége 4 080 000 Ft/km/év.")

    st.divider()

    st.markdown("<h2 style='text-align: center;'>Üzemeltetési és karbantartási költség meghatározása</h2>", unsafe_allow_html=True)
    if st.button("Üzemeltetési és karbantartási költség meghatározása", use_container_width=True):
        col_a, col_b = st.columns([1, 1])
        with col_a:
            with st.container(border=True):
                st.metric(label = "Felüljáró, 1. év", value=f"{feluljaro_mukodesi_koltseg:,.0f} Ft".replace(".", ","))
        with col_b:
            with st.container(border=True):
                st.metric(label = "Körforgalom, 1. év", value=f"{korforgalom_mukodesi_koltseg:,.0f} Ft".replace(".", ","))
        st.write("")
        col_f, col_g = st.columns([1, 1])
        with col_f:
            with st.container(border=True):
                st.metric(label="Felüljáró, referencia-időszak utolsó éve, PV",
                            value=f"{float(feluljaro_pv):,.0f} Ft".replace(".", ","))
            with col_g:
                with st.container(border=True):
                    st.metric(label="Körforgalom, referencia-időszak utolsó éve, PV",
                              value=f"{float(korforglaom_pv):,.0f} Ft".replace(".", ","))
            st.write("")

if st.button("Üzemeltetési és karbantartási költségek bontása", use_container_width=True):
    df_opex_summary = pd.DataFrame({
        "Műtárgy típusa": ["Felüljáró", "Körforgalom", "ÖSSZESEN"],
        "Terület / kerület [m]": [f"{feluljaro_hossz:.0f} m", f"{korforgalom_hossz:.0f} m", "-"],
        "1. évi költség [Ft]": [f"{feluljaro_mukodesi_koltseg:,.0f} Ft", f"{korforgalom_mukodesi_koltseg:,.0f} Ft", f"{teljes_mukodesi_koltseg:,.0f} Ft"],
        "29 éves névleges ár [Ft]": [f"{feluljaro_utolsoev:,.0f} Ft", f"{korforgalom_utolsoev:,.0f} Ft",
                                     f"{teljes_utolsoev:,.0f} Ft"],
        "29 éves jelenérték (PV) [Ft]": [f"{feluljaro_pv:,.0f} Ft", f"{korforglaom_pv:,.0f} Ft", f"{teljes_pv:,.0f} Ft"]
    })

    st.dataframe(df_opex_summary, use_container_width=True, hide_index=True)

    with st.expander("Évenkénti diszkontált pénzáramok részletezése (1–29. év)"):
        evek = list(range(1, evek_szama + 1))
        nevleges_lista = [teljes_mukodesi_koltseg] * evek_szama
        jelenertek_lista = [teljes_mukodesi_koltseg / ((1 + r) ** t) for t in evek]

        df_eves_bontas = pd.DataFrame({
            "Év (t)": evek,
            "Névleges üzemeltetési költség (Ft)": [f"{val:,.0f} Ft".replace(",", " ") for val in nevleges_lista],
            "Diszkontált jelenérték (Ft)": [f"{val:,.0f} Ft".replace(",", " ") for val in jelenertek_lista]
        })

        st.dataframe(df_eves_bontas, use_container_width=True, hide_index=True)

with tab3:
    feluljaro_potlasi_ertek = 1750000000
    korforgalom_potlasi_ertek = 200000

    col4, col5 = st.columns([1, 1])

    with col4:
        feluljaro_elettartam = st.number_input(
            "Hány év a felüljáró élettartama? (év): ",
            value=50,
            step=1,
            format="%.1f")

    with col5:
        korforgalom_elettartam = st.number_input(
            "Hány év a körforgalom élettartama? (év): ",
            value=20,
            step=1,
            format="%.1f")


    if feluljaro_elettartam > projekt_referencia_idoszak:
        feluljaro_potlasi_ertek = 0
    else:
        feluljaro_potlasi_ertek = 175000000

    feluljaro_potlasi_koltseg = feluljaro_potlasi_ertek * (feluljaro_hossz / 1000)
    korforgalom_potlasi_koltseg = korforgalom_potlasi_ertek * korforgalom_hossz

    with st.container(border=True):
        st.write(f"A felüljáró pótlási költsége a referencia időszak miatt {feluljaro_potlasi_koltseg:,.0f} Ft.")
        st.write(f"A körforgalom pótlási költsége a referencia időszak miatt {korforgalom_potlasi_ertek:,.0f} Ft.")
    st.divider()

    st.markdown("<h2 style='text-align: center;'>Pótlási költség meghatározása</h2>", unsafe_allow_html=True)
    if st.button("Pótlási költség meghatározása", use_container_width=True):
        col_d, col_e = st.columns([1, 1])
        with col_d:
            with st.container(border=True):
                st.metric(label = "Felüljáró pótlási költsége", value=f"{feluljaro_potlasi_koltseg:,.0f} Ft".replace(".", ","))
        with col_e:
            with st.container(border=True):
                st.metric(label = "Körforgalom pótlási költsége", value=f"{korforgalom_potlasi_koltseg:,.0f} Ft".replace(".", ","))

with tab4:
    def szamol_maradvanyertek_feluljaro(feluljaro_elettartam, projekt_referencia_idoszak, feluljaro_epitesikoltseg,
                                        feluljaro_potlasi_koltseg):
        if feluljaro_elettartam > projekt_referencia_idoszak:
            return ((feluljaro_elettartam - projekt_referencia_idoszak) / feluljaro_elettartam) * feluljaro_epitesikoltseg
        else:
            return ((projekt_referencia_idoszak - feluljaro_elettartam) / feluljaro_elettartam) * feluljaro_potlasi_koltseg

    feluljaro_maradvanyertek = szamol_maradvanyertek_feluljaro(feluljaro_elettartam, projekt_referencia_idoszak, feluljaro_epitesikoltseg, feluljaro_potlasi_koltseg)


    def szamol_maradvanyertek_korforgalom(korforgalom_elettartam, projekt_referencia_idoszak,korforgalom_epitesikoltseg, korforgalom_potlasi_koltseg):
        if korforgalom_elettartam > projekt_referencia_idoszak:
            return ((korforgalom_elettartam - projekt_referencia_idoszak) / korforgalom_elettartam) * korforgalom_epitesikoltseg
        else:
            return ((projekt_referencia_idoszak - korforgalom_elettartam)) / korforgalom_elettartam * korforgalom_potlasi_koltseg
    korforgalom_maradvanyertek = szamol_maradvanyertek_korforgalom(korforgalom_elettartam, projekt_referencia_idoszak,korforgalom_epitesikoltseg,korforgalom_potlasi_koltseg)

    st.markdown("<h2 style='text-align: center;'>Maradványérték meghatározása</h2>", unsafe_allow_html=True)
    if st.button("Maradványérték meghatározása", use_container_width=True):
        col_d, col_e = st.columns([1, 1])
        with col_d:
            with st.container(border=True):
                st.metric(label="Felüljáró maradványértéke",
                          value=f"{feluljaro_maradvanyertek:,.0f} Ft".replace(".", ","))
        with col_e:
            with st.container(border=True):
                st.metric(label="Körforgalom maradványértéke",
                          value=f"{korforgalom_maradvanyertek:,.0f} Ft".replace(".", ","))


