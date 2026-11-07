import pip
import pandas as pd
import streamlit as st

st.title('Üdvözöljük! A program során lehetőség van különböző közlekedési infrastrukturális beruházások megtérülésének vizsgálata költség-haszon elemzés segítségével.')
st.header('Az első lépés a beruházási költség meghatározása.')

# 1. lépés, a beruházási költség meghatározása

feluljaro_hossz = float(input("Mekkora a felüljáró tervezett hossza? (m): "))
korforgalom_hossz = float(input("Mekkora a körforgalom kerülete? (m): "))
kisajatitando_terulet = float(input("Mekkora a kisajátítandó zöldterület? (m2): "))
fairtas = float(input("Mekkora területen szükséges a fa- és bozótirtás? (m2): "))
projekt_referencia_idoszak = int(input("Hány év a projekt referencia időszaka? (általánosan: 30 év) (év): "))


fajlagos_zoldterulet_ara = 1990000 / 10000
fajlagos_fairtas_ara = 515
epitesi_koltseg_meterenkent =  7908719
#367m-es felüljáró beruházási költsége 2 902 500 000 volt, tehát 1 m az 7 908 719 forint
epitesi_koltseg_korforgalom = 2665289
#A körforgalom kerülete 121 méter, ez került 322 500 000 ft-ba, tehát 1m az 2 665 289 ft

foldvasarlas_koltseg = kisajatitando_terulet * fajlagos_zoldterulet_ara
fairtas_koltseg = fairtas * fajlagos_fairtas_ara
feluljaro_epitesikoltseg = feluljaro_hossz * epitesi_koltseg_meterenkent
korforgalom_epitesikoltseg = korforgalom_hossz * epitesi_koltseg_korforgalom

teljes_beruhazasi_koltseg = foldvasarlas_koltseg + fairtas_koltseg + feluljaro_epitesikoltseg + korforgalom_epitesikoltseg



print("--- BERUHÁZÁSI KÖLTSÉG EREDMÉNYEK ---")
print(f"Földvásárlás költsége: {foldvasarlas_koltseg:,.0f} Ft")
print(f"Fairtás költsége: {fairtas_koltseg:,.0f} Ft")
print(f"A felüljáró építési költsége: {feluljaro_epitesikoltseg:,.0f} Ft")
print(f"A körforgalom építési költsége: {korforgalom_epitesikoltseg:,.0f} Ft")
print(f"A teljes beruházási költség: {teljes_beruhazasi_koltseg:,.0f} Ft")

# 2. lépés - Üzemeltetési és karbantartási költségek meghatározása

feluljaro_mukodesi_ertek = 114750000
korforgalom_mukodesi_ertek = 4080000

feluljaro_mukodesi_koltseg = feluljaro_mukodesi_ertek * (feluljaro_hossz/1000)
korforgalom_mukodesi_koltseg = korforgalom_mukodesi_ertek * (korforgalom_hossz/1000)
teljes_mukodesi_koltseg = korforgalom_mukodesi_koltseg + feluljaro_mukodesi_koltseg
teljes_mukodesi_koltseg_jelenertek = teljes_mukodesi_koltseg * (1-(1+0.03) ** -(projekt_referencia_idoszak - 1)) / 0.03

print("--- ÜZEMELTETÉSI ÉS KARBANTARTÁSI KÖLTSÉG EREDMÉNYEK ---")
print(f"Felüljáró üzemeltetési és karbantartási költsége: {feluljaro_mukodesi_koltseg:,.0f} Ft")
print(f"Körforgalom üzemeltetési és karbantartási költsége: {korforgalom_mukodesi_koltseg:,.0f} Ft")
print(f"A teljes beruházás üzemeltetési és karbantartási költsége: {teljes_mukodesi_koltseg:,.0f} Ft")
print(f"A teljes beruházás üzemeltetési és karbantartási költsége nettó jelenértékben: {teljes_mukodesi_koltseg_jelenertek:,.0f} Ft")

# 3. lépés - Pótlási költségek meghatározása

feluljaro_potlasi_ertek = 1750000000
korforgalom_potlasi_ertek = 200000

feluljaro_elettartam = int(input("Hány év a felüljáró élettartama? "))
korforgalom_elettartam = int(input("Hány év a körforgalom élettartama? "))

if feluljaro_elettartam > projekt_referencia_idoszak:
    feluljaro_potlasi_ertek = 0
else:
    feluljaro_potlasi_ertek = 175000000

feluljaro_potlasi_koltseg = feluljaro_potlasi_ertek * (feluljaro_hossz/1000)
korforgalom_potlasi_koltseg = korforgalom_potlasi_ertek * korforgalom_hossz

print(f"A felüljáró pótlási költsége a referencia időszak alatt: {feluljaro_potlasi_koltseg:,.0f} Ft")
print(f"A körforgalom pótlási költsége a referenciaidőszak alatt: {korforgalom_potlasi_koltseg:,.0f} Ft")

# 4. lépés - Maradványérték

def szamol_maradvanyertek_feluljaro(feluljaro_elettartam,projekt_referencia_idoszak,feluljaro_epitesikoltseg,feluljaro_potlasi_koltseg):
    if feluljaro_elettartam > projekt_referencia_idoszak:
        return ((feluljaro_elettartam - projekt_referencia_idoszak) / feluljaro_elettartam) * feluljaro_epitesikoltseg
    else:
        return ((projekt_referencia_idoszak - feluljaro_elettartam) / feluljaro_elettartam) * feluljaro_potlasi_koltseg
feluljaro_maradvanyertek = szamol_maradvanyertek_feluljaro(feluljaro_elettartam,projekt_referencia_idoszak,feluljaro_epitesikoltseg,feluljaro_potlasi_koltseg)

print(f"A felüljáró maradványértéke: {feluljaro_maradvanyertek:,.0f} Ft")

def szamol_maradvanyertek_korforgalom(korforgalom_elettartam,projekt_referencia_idoszak,korforgalom_epitesikoltseg,korforgalom_potlasi_koltseg):
    if korforgalom_elettartam > projekt_referencia_idoszak:
        return ((korforgalom_elettartam - projekt_referencia_idoszak) / korforgalom_elettartam) * korforgalom_epitesikoltseg
    else:
        return ((projekt_referencia_idoszak - korforgalom_elettartam)) / korforgalom_elettartam * korforgalom_potlasi_koltseg
korforgalom_maradvanyertek = szamol_maradvanyertek_korforgalom(korforgalom_elettartam,projekt_referencia_idoszak,korforgalom_epitesikoltseg,korforgalom_potlasi_koltseg)

print(f"A körforgalom maradványértéke: {korforgalom_maradvanyertek:,.0f} Ft")



# 5. lépés - ÁNF bekérése


import pandas as pd

def parse_szelveny(val):
    if pd.isna(val):
        return None
    try:
        val_str = str(val).strip().replace(" ", "")

        if "+" in val_str:
            parts = val_str.split("+")
            km = float(parts[0]) if parts[0] else 0.0
            m = float(parts[1]) if (len(parts) > 1 and parts[1]) else 0.0
            return km + (m / 1000.0)

        val_str = val.str.replace(",", ".")
        return float(val_str)

    except Exception:
        return None

excel_path = "2025_ANF.xlsx"
df = pd.read_excel(excel_path, sheet_name="eanf_2025_20261001", header=1)

df["Út száma"] = (df["Út száma"].astype(str).str.replace(r"\.0$", "", regex=True).str.strip())

df["eleje_km"] = df["Érv.eleje"].apply(parse_szelveny)
df["vege_km"] = df["Érv.vége"].apply(parse_szelveny)

def keres_szelveny(ut_szama, szelveny_input):
    user_km = parse_szelveny(szelveny_input)

    if user_km is None:
        print("Érvénytelen szelvényszám formátum!")
        return None

    ut_szama_clean = str(ut_szama).strip().replace('.0', '')
    feltetel_ut = df["Út száma"] == ut_szama_clean

    min_km = df[['eleje_km', 'vege_km']].min(axis=1)
    max_km = df[['eleje_km', 'vege_km']].max(axis=1)

    feltetel_szelveny = (min_km <= user_km) & (user_km <= max_km)

    talalatok = df[feltetel_ut & feltetel_szelveny]

    if talalatok.empty:
        print(f"Nem található szakasz a(z) {ut_szama} úton a(z) {szelveny_input} szelvénynél!")
        return None
    return talalatok

keresett_ut = input("Adja meg a keresett út számát: ")
keresett_szelvény = input("Adja meg a keresett szelvény számát: ")

talalat = keres_szelveny(keresett_ut, keresett_szelvény)

if talalat is not None:
    print("--- Megtalált szakasz ---")

    fontos_oszlopok = [
        "Út száma",
        "Megye",
        "Érv.eleje",
        "Érv.vége",
        "ÉÁNF (Ej)",
        "Személy-gépkocsi",
        "Szóló teher-gépkocsi",
        "Pótkocsis teher-gépkocsi",
        "Nyerges szerelvény",
    ]

    print(talalat[fontos_oszlopok].to_string(index=False))

    df['Tehergépjárművek'] = (
        df['Szóló teher-gépkocsi'].fillna(0)
        + df['Pótkocsis teher-gépkocsi'].fillna(0)
        + df['Nyerges szerelvény'].fillna(0)
    )

    if talalat is not None:
        szolo = talalat['Szóló teher-gépkocsi'].values[0]
        potkocsis = talalat['Pótkocsis teher-gépkocsi'].values[0]
        nyerges = talalat['Nyerges szerelvény'].values[0]
        szemelygepjarmi = talalat['Személy-gépkocsi'].values[0]

        teher_osszesen = (szolo + potkocsis + nyerges) * 2.5
        szemelygepjarmu = szemelygepjarmi

    print(f"A vizsgált keresztmetszeten a személygépjárművek száma {szemelygepjarmu} jármű, a tehergépjárművek száma {int(teher_osszesen)} egységjármű")

# 5.2 Forgalomprognózis

    BAZISEV = 2025
    print("\n--- FORGALOMPROGNÓZIS BEÁLLÍTÁSA ---")
    celev = int(input('Melyik évre szeretné elvégezni a vizsgálatot (bázisév)? '))

    p_szemely_pct = float(input("Éves személygépjármű forgalomnövekedési ütem (pl.: 1.5%)? "))
    p_teher_pct = float(input("Éves tehergépjármű forgalomnövekedési ütem (pl.: 1.5%)? "))

    evek_szama = celev - BAZISEV

    if evek_szama < 0:
        print("A célév korábbi a bázisévnél! Az érték az eredeti marad.")
        faktor_szemely = 1.0
        faktor_teher = 1.0
    else:
        faktor_szemely = (1 + (p_szemely_pct / 100.00)) ** evek_szama
        faktor_teher = (1 + (p_teher_pct / 100.00)) ** evek_szama

        szemely_celevre = szemelygepjarmu * faktor_szemely
        teher_celevre = teher_osszesen * faktor_teher

    print(f"A vizsgált keresztmetszeten {celev}-ben a személygépjárművek száma {round(szemely_celevre, 1)} jármű/nap, "
          f"a tehergépjárművek száma {round(teher_celevre, 1)} egységjármű/nap.")


    # 6. lépés - Zárvatartási idők meghatározása

print ("\n=== SOROMPÓ ZÁRVATARTÁSI IDEJÉNEK MEGHATÁROZÁSA ---")

lezarasok_szama = input("Adja meg a lezárások időtartamát másodpercben, vesszővel elválasztva (pl. 84, 180, 74, 231, 113, 167, 85, 68): ")

lezarasok_sec = [float(x.strip()) for x in lezarasok_szama.split(",") if x.strip()]

def szamol_zarvatartas(lezaras_lista, vizsgalt_időszak_sec =3600):
        db = len(lezaras_lista)
        osszes_sec = sum(lezaras_lista)
        osszes_min = osszes_sec / 60
        zarvatartas_ptc = (osszes_sec / vizsgalt_időszak_sec) * 100
        szabad_pct = 100.0 - zarvatartas_ptc
        atlag_zaras_perc = osszes_min / db if db > 0 else 0

        return {
            "lezarasok_szama": db,
            "osszes_zaras_sec": osszes_sec,
            "osszes_zaras_min": round(osszes_min, 2),
            "zarvatartas_ptc": round(zarvatartas_ptc, 2),
            "szabad_pct": round(szabad_pct, 2),
            "atlag_zaras_perc": round(atlag_zaras_perc, 1)
        }

print("\n--- Zárva tartás eredményei ---")

zarvatartas_adatok = szamol_zarvatartas(lezarasok_sec)

print(f"Lezárások száma: {zarvatartas_adatok['lezarasok_szama']} db")
print("Összes zárvatartási idő:"
      f" {zarvatartas_adatok['osszes_zaras_sec']} másodperc = "
      f" {zarvatartas_adatok['osszes_zaras_min']} perc")
print(f"Átlagos egyedi lezárási idő: {zarvatartas_adatok['atlag_zaras_perc']} perc")
print(f"A csúcsóra korlátozottsága: {zarvatartas_adatok['zarvatartas_ptc']} %")
print(f"A szabad áthaladási időaránya: {zarvatartas_adatok['szabad_pct']} %")

# 7. lépés - Személygépjárműforgalom időnyereségének számszerűsítése és monetizálása

print ("\n=== SZEMÉLYGÉPJÁRMŰVEK IDŐNYERESÉGÉNEK SZÁMSZERŰSÍTÉSE ÉS MONETIZÁLÁSA ---")

szemely_gepjarmu_szemelyek = szemely_celevre * 1.5
atlagos_lezaras_veszteseggel = (zarvatartas_adatok['osszes_zaras_min'] / 2)
atlagos_varakozasi_ido = atlagos_lezaras_veszteseggel * (zarvatartas_adatok['zarvatartas_ptc'] / 100)
napi_varakozasi_ido = atlagos_varakozasi_ido * szemely_gepjarmu_szemelyek

print(f"A személyenkénti átlagos várakozási idő {round(atlagos_varakozasi_ido, 2)} perc/személy")
print(f"A napi összes várakozási idő {round(napi_varakozasi_ido, 2)} perc/nap")

uzleti_utazasingazas = 7457 # forint/utasóra
egyeb_utazas = 2613 # forint/utasóra
uzleti_utazasingazas_arany = szemely_gepjarmu_szemelyek * 0.25
egyeb_utazas_arany = szemely_gepjarmu_szemelyek * 0.75

uzleti_utazas_varakozas = (napi_varakozasi_ido / 60) * 0.25
egyeb_utazas_varakozas = (napi_varakozasi_ido / 60) * 0.75

print(f"Üzleti utazás/ingázás kategóriában a napi összes várakozás {round(uzleti_utazas_varakozas, 2)} óra/nap")
print(f"Egyéb utazás kategóriában a napi összes várakozás {round(egyeb_utazas_varakozas, 2)} óra/nap")

elsoevi_tarsadalmikoltseg = ((uzleti_utazas_varakozas * uzleti_utazasingazas) + (egyeb_utazas_varakozas * egyeb_utazas)) * 365

def fmt(ertek):
    return f"{ertek:,.0f}".replace(",", " ")

print(f"Az első évben a személygépjárművek várakozásából {fmt(elsoevi_tarsadalmikoltseg)} forint társadalmi költség keletkezik.")

forgalom_novekedes = 1.015
gdp_novekedese = 1.029
diszkontrata = 1.030

b1 = elsoevi_tarsadalmikoltseg

jelenertekek = []
tarsadalmi_hasznok = []
aktualis_haszon = b1

print("\n--- Éves társdalmi hasznok a személygépjárművek várakozására nézve ---")

for t in range(1, 30):
    if t == 1:
        haszon_t = b1
    else:
        haszon_t = aktualis_haszon * forgalom_novekedes * gdp_novekedese
        aktualis_haszon = haszon_t

    pv_t = haszon_t / (diszkontrata ** t)
    jelenertekek.append(pv_t)
    tarsadalmi_hasznok.append(haszon_t)

    if t in [1, 2, 29]:
        print(f"{t}. év -> Társadalmi haszon: {fmt(haszon_t)} Ft | Jelenérték: {fmt(pv_t)}")

osszes_tarasdalmi_haszon = sum(tarsadalmi_hasznok)
osszes_diszkontalt_haszon = sum(jelenertekek)

print(f"Az összes diszkontált társadalmi haszon {fmt(osszes_tarasdalmi_haszon)} Forint társadalmi haszon, {fmt(osszes_diszkontalt_haszon)} Forint nettó jelenértékű haszon")



# 8. lépés - Tehergépjárművek időnyereségének monetizálása

print("\n--- Éves társadalmi hasznok a tehergépjárművek várakozására nézve ---")

teher_nemegysegjarmu = teher_celevre / 2.5
atlagos_lezaras_veszteseggel = (zarvatartas_adatok['osszes_zaras_min'] / 2)
atlagos_varakozasi_ido = atlagos_lezaras_veszteseggel * (zarvatartas_adatok['zarvatartas_ptc'] / 100)
napi_varakozasi_ido = atlagos_varakozasi_ido * teher_nemegysegjarmu

print(f"A tehegépjárművek átlagos várakozási ideje {round(atlagos_varakozasi_ido, 2)} perc/jármű")
print(f"A napi összes várakozási idő {round(napi_varakozasi_ido, 2)} perc/nap")

teher_fajlagos_idoertek = 595 # forint/árutonnaóra
teher_rakomany = 18 # tonna
teher_rakomany_oraerteke = teher_rakomany * teher_fajlagos_idoertek # Ft/járműóra
napi_varakozas_teher = napi_varakozasi_ido / 60

elsoevi_tarsadalmikoltseg_teher = (napi_varakozas_teher * teher_rakomany_oraerteke) * 365

print(f"Az első évben a tehergépjárművek várakozásából {fmt(elsoevi_tarsadalmikoltseg_teher)} forint társadalmi költség keletkezik.")

forgalom_novekedes = 1.015
gdp_novekedese_teher = 1.0
diszkontrata = 1.030

b2 = elsoevi_tarsadalmikoltseg_teher

jelenertekek_teher = []
tarsadalmi_hasznok_teher = []
aktualis_haszon_teher = b2

for t in range(1, 30):
    if t == 1:
        haszon_teher = b2
    else:
        haszon_teher = aktualis_haszon_teher * forgalom_novekedes * gdp_novekedese_teher
        aktualis_haszon_teher = haszon_teher

    pv_teher = haszon_teher / (diszkontrata ** t)
    jelenertekek_teher.append(pv_teher)
    tarsadalmi_hasznok_teher.append(haszon_teher)

    if t in [1, 2, 29]:
        print(f"{t}. év -> Társadalmi haszon: {fmt(haszon_teher)} Ft | Jelenérték: {fmt(pv_teher)}")

osszes_tarasdalmi_haszon_teher = sum(tarsadalmi_hasznok_teher)
osszes_diszkontalt_haszon_teher = sum(jelenertekek_teher)

print(f"Az összes diszkontált társadalmi haszon {fmt(osszes_tarasdalmi_haszon_teher)} Forint társadalmi haszon, {fmt(osszes_diszkontalt_haszon_teher)} Forint nettó jelenértékű haszon")

# 9. lépés - InterCity vonaton utazók időnyeresége

print("\n--- Éves társadalmi hasznok a vasúton IC vonattal utazók késésére nézve ---")

IC_utasszam = int(input("Mekkora az utasszám az InterCity vonatokon az adott vasútvonalon egy nap alatt? "))
uzemido = int(input("Hány óra a vasúti üzemidő az adott vasútvonalon a személyszállító vonatokra nézve? "))
csaporud_tores = int(input("Átlagosan hányször törik le a csapórudat egy évben? "))
forgalomkorlatozas = csaporud_tores * 3

print(f"A forgalomkorlátozás ideje egy évben összesen {forgalomkorlatozas} óra/év")

erintett_utasok = (3 / uzemido) * IC_utasszam

print(f"Egy forgalomkorlátozás átlagosan {erintett_utasok} utast érint.")

osszes_keses = erintett_utasok * 0.05 * csaporud_tores

print(f"Az összes késés {osszes_keses} óra az összes utasra nézve.")

uzleti_utazasingazas_eredeti = 4971 # forint/utasóra
egyeb_utazas_eredeti = 1742 # forint/utasóra
uzleti_utazasingazas_arany_vasut = osszes_keses * 0.25
egyeb_utazas_arany_vasut = osszes_keses * 0.75

elsoevi_tarsadalmikoltseg_vasutIC = ((uzleti_utazasingazas_eredeti * uzleti_utazasingazas_arany_vasut) + (egyeb_utazas_eredeti * egyeb_utazas_arany_vasut))

print(f"Az első évben az IC-n utazók késéséből {fmt(elsoevi_tarsadalmikoltseg_vasutIC)} forint társadalmi költség keletkezik.")

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

    if t in [1, 2, 29]:
        print(f"{t}. év -> Társadalmi haszon: {fmt(haszon_vasutIC)} Ft | Jelenérték: {fmt(pv_vasutIC)}")

osszes_tarsadalmi_haszon_vasutIC = sum(tarsadalmi_hasznok_vasutIC)
osszes_diszkontalt_haszon_vasutIC = sum(jelenertekek_vasutIC)

print(f"Az összes diszkontált társadalmi haszon {fmt(osszes_tarsadalmi_haszon_vasutIC)} Forint társadalmi haszon, {fmt(osszes_diszkontalt_haszon_vasutIC)} Forint nettó jelenértékű haszon")

# 10. lépés - Személyvonaton vonaton utazók időnyeresége

print("\n--- Éves társadalmi hasznok a vasúton személyvonattal vonattal utazók késésére nézve ---")

szemely_utasszam = int(input("Mekkora az utasszám a személyvonatokon adott vasútvonalon egy nap alatt? "))

print(f"A forgalomkorlátozás ideje egy évben összesen {forgalomkorlatozas} óra/év")

erintett_utasok_szemely = (3 / uzemido) * szemely_utasszam

print(f"Egy forgalomkorlátozás átlagosan {erintett_utasok_szemely} utast érint.")

osszes_keses_szemely = erintett_utasok_szemely * 0.05 * csaporud_tores

print(f"Az összes késés {osszes_keses_szemely} óra az összes utasra nézve.")

uzleti_utazasingazas_arany_vasutszemely = osszes_keses_szemely * 0.25
egyeb_utazas_arany_vasutszemely = osszes_keses_szemely * 0.75

elsoevi_tarsadalmikoltseg_vasutszemely = ((uzleti_utazasingazas_eredeti * uzleti_utazasingazas_arany_vasutszemely) + (egyeb_utazas_eredeti * egyeb_utazas_arany_vasutszemely))

print(f"Az első évben az IC-n utazók késéséből {fmt(elsoevi_tarsadalmikoltseg_vasutszemely)} forint társadalmi költség keletkezik.")

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

    if t in [1, 2, 29]:
        print(f"{t}. év -> Társadalmi haszon: {fmt(haszon_vasutszemely)} Ft | Jelenérték: {fmt(pv_vasutszemely)}")

osszes_tarsadalmi_haszon_vasutszemely = sum(tarsadalmi_hasznok_vasutszemely)
osszes_diszkontalt_haszon_vasutszemely = sum(jelenertekek_vasutszemely)

print(f"Az összes diszkontált társadalmi haszon {fmt(osszes_tarsadalmi_haszon_vasutszemely)} Forint társadalmi haszon, {fmt(osszes_diszkontalt_haszon_vasutszemely)} Forint nettó jelenértékű haszon")

# 11. lépés - Tehervonatok késésének monetizálása

print("\n--- Éves társadalmi hasznok a vasúti áruszállítás késésére vizsgálva ---")

tehervonatok_mennyiseg = int(input("Hány tehervonat halad át az adott keresztmetszeten átlagosan egy nap alatt? "))
tehervonatok_tomeg = int(input("Hány tonna árut szállítanak az adott tehervonatok egy nap alatt? "))
uzemido_teher = int(input("Hány óra a vasúti üzemidő az adott vasútvonalon az áruszállításra nézve? "))
forgalomkorlatozas = csaporud_tores * 3

print(f"A forgalomkorlátozás ideje egy évben összesen {forgalomkorlatozas} óra/év.")

napi_atlagos_aru = (tehervonatok_tomeg / tehervonatok_mennyiseg)

print(f"Egy tehervonat átlagos rakománya: {round(napi_atlagos_aru, 1)} tonna/vonat.")

erintett_vonatok_teher = (3 / uzemido_teher) * tehervonatok_mennyiseg

erintett_aru_teher_ev = (napi_atlagos_aru * erintett_vonatok_teher) * csaporud_tores

idoveszteseg_teher = 0.05 * erintett_aru_teher_ev

print(f"A teljes évi időveszteség az árukra nézve {round(idoveszteseg_teher, 1)} tonnaóra/év.")

arutonna_fajlagoskoltseg_2026 = 311.1

elsoevi_tarsadalmikoltseg_vasutteher = arutonna_fajlagoskoltseg_2026 * idoveszteseg_teher

print(f"Az első évben a tehervonatok késéséből {fmt(elsoevi_tarsadalmikoltseg_vasutteher)} forint társadalmi költség keletkezik.")

b5 = elsoevi_tarsadalmikoltseg_vasutteher

jelenertekek_vasutaru = []
tarsadalmi_hasznok_vasutaru = []
aktualis_haszon_vasutaru = b5

for t in range(1, 30):
    if t == 1:
        haszon_vasutaru = b5
    else:
        haszon_vasutaru = aktualis_haszon_vasutaru * forgalom_novekedes
        aktualis_haszon_vasutaru = haszon_vasutaru

    pv_vasutaru = haszon_vasutaru / (diszkontrata ** t)
    jelenertekek_vasutaru.append(pv_vasutaru)
    tarsadalmi_hasznok_vasutaru.append(haszon_vasutaru)

    if t in [1, 2, 29]:
        print(f"{t}. év -> Társadalmi haszon: {fmt(haszon_vasutaru)} Ft | Jelenérték: {fmt(pv_vasutaru)}")

osszes_tarsadalmi_haszon_vasutaru = sum(tarsadalmi_hasznok_vasutaru)
osszes_diszkontalt_haszon_vasutaru = sum(jelenertekek_vasutaru)

print(f"Az összes diszkontált társadalmi haszon {fmt(osszes_tarsadalmi_haszon_vasutaru)} Forint társadalmi haszon, {fmt(osszes_diszkontalt_haszon_vasutaru)} Forint nettó jelenértékű haszon")

# 12. lépés - Balesetek megszüntetésének monetizálása

print("\n--- Baleseti kockázatváltozás költségeinek monetizálása a vizsgált csomópontra ---")

feluljaro_hossz = 367

eves_futasteljesitmeny_szgk = 365 * szemelygepjarmu * (feluljaro_hossz / 1000)
eves_futasteljesitmeny_teher = 365 * (teher_osszesen / 2.5) * (feluljaro_hossz / 1000)

print(f"A személygépjárművek éves futásteljesítménye {fmt(round(eves_futasteljesitmeny_szgk, 1))} járműkm/év.")
print(f"A tehergépjárművek éves futásteljesítménye {fmt(round(eves_futasteljesitmeny_teher, 1))} járműkm/év.")

fajlagos_balesetikoltseg_szgk = 55.14 # Ft/jkm
fajlagos_balesetikoltseg_teher = 56.14 # Ft/jkm

print(f"A személygépjárművek fajlagos baleseti költsége {fajlagos_balesetikoltseg_szgk} Ft/járműkm.")
print(f"A tehergépjárművek fajlagos baleseti költsége {fajlagos_balesetikoltseg_teher} Ft/járműkm.")

elsoevi_tarsadalmikoltseg_baleset = (fajlagos_balesetikoltseg_szgk * eves_futasteljesitmeny_szgk) + (fajlagos_balesetikoltseg_teher * eves_futasteljesitmeny_teher)

print(f"Az első évben a baleseti kockázat nullára csökkenéséből {fmt(elsoevi_tarsadalmikoltseg_baleset)} forint társadalmi költség keletkezik.")

forgalom_novekedes = 1.015
gdp_novekedese = 1.029
diszkontrata = 1.030

b6 = elsoevi_tarsadalmikoltseg_baleset

jelenertekek_baleset = []
tarsadalmi_hasznok_baleset = []
aktualis_haszon_baleset = b6

for t in range (1, 30):
    if t == 1:
        haszon_baleset = b6
    else:
        haszon_baleset = aktualis_haszon_baleset * forgalom_novekedes * gdp_novekedese
        aktualis_haszon_baleset = haszon_baleset

    pv_baleset = haszon_baleset / (diszkontrata ** t)
    jelenertekek_baleset.append(pv_baleset)
    tarsadalmi_hasznok_baleset.append(haszon_baleset)

    if t in [1, 2, 29]:
        print(f"{t}. év -> Társadalmi haszon: {fmt(haszon_baleset)} Ft | Jelenérték: {fmt(pv_baleset)}")

    osszes_tarsadalmihaszon_baleset = sum(tarsadalmi_hasznok_baleset)
    osszes_jelenertek_baleset = sum(jelenertekek_baleset)

print(f"Az összes diszkontált társadalmi haszon {fmt(osszes_tarsadalmihaszon_baleset)} Forint társadalmi haszon, {fmt(osszes_jelenertek_baleset)} Forint nettó jelenértékű haszon")

# 13. lépés - Csapórúdtörésekből származó anyagköltség monetizálása

print("\n--- Rendkívüli eseményekből adódó költségek a MÁV Pályaműködtetési Zrt. részére ---")

anyagkoltseg = 95000
evi_anyagkoltseg = anyagkoltseg * csaporud_tores

print(f"1 évben a csapórudak-letöréséből nagyjából {fmt(evi_anyagkoltseg)} Forint kár keletkezik a MÁV Pályaműködtetési Zrt. számára.")

b7 = evi_anyagkoltseg
jelenertekek_csaporud = []
tarsadalmihasznok_csaporud = []
aktualis_haszon_csaporud = b7

for t in range (1, 30):
    if t == 1:
        haszon_csaporud = b7
    else:
        haszon_csaporud = aktualis_haszon_csaporud * forgalom_novekedes
        aktualis_haszon_csaporud = haszon_csaporud

    pv_csaporud = haszon_csaporud / (diszkontrata ** t)
    jelenertekek_csaporud.append(pv_csaporud)
    tarsadalmihasznok_csaporud.append(haszon_csaporud)

    if t in [1, 2, 29]:
        print(f"{t}. év -> Társadalmi haszon: {fmt(haszon_csaporud)} Ft | Jelenérték: {fmt(pv_csaporud)}")

    osszes_tarsadalmihaszon_csaporud = sum(tarsadalmihasznok_csaporud)
    osszes_jelenertek_csaporud = sum(jelenertekek_csaporud)

print(f"Az összes diszkontált társadalmi haszon {fmt(osszes_tarsadalmihaszon_csaporud)} Forint társadalmi haszon, {fmt(osszes_jelenertek_csaporud)} Forint nettó jelenértékű haszon.")

# 14. lépés - MÁV Plusz üzemanyag monetizálása

print("\n--- Rendkívüli eseményekből adódó költségek a társadalom részére ---")

keszenlet_tavolsag = int(input("A készenléti szolgálat összesen hány km-t tesz meg egy rendkívüli esemény bekövetkeztekor (km)? "))
piaci_arszbas = float(input("Mekkora a piaci árszabása a készneléti szolgálat által használt jármű tüzelőanyagának (Ft/l)? "))
atlagfogyasztas_MAV = float(input("Mekkora az átlagfogyasztása a készenléti szolgálat által használt járműnek (l/100 km)? "))

fajlagos_uzemanyagkoltseg_MAV = (atlagfogyasztas_MAV / 100) * piaci_arszbas
uzemanyagkoltseg_1 = fajlagos_uzemanyagkoltseg_MAV * keszenlet_tavolsag
uzemanyagkoltseg_ev = uzemanyagkoltseg_1 * csaporud_tores

print(f"Az 1. évben a csapórudak-letöréséből nagyjából {fmt(uzemanyagkoltseg_ev)} Forint üzemanyagköltség keletkezik a MÁV Pályaműködtetési Zrt. számára.")

b8 = uzemanyagkoltseg_ev
jelenertekek_uzemanyagMAV = []
tarsadalmi_haszon_uzemanyagMAV = []
aktualis_haszon_uzemanyagMAV = b8

for t in range (1, 30):
    if t == 1:
        haszon_uzemanyagMAV = b8
    else:
        haszon_uzemanyagMAV = aktualis_haszon_uzemanyagMAV * forgalom_novekedes
        aktualis_haszon_uzemanyagMAV = haszon_uzemanyagMAV

    pv_uzemanyagMAV = haszon_uzemanyagMAV / (diszkontrata ** t)
    jelenertekek_uzemanyagMAV.append(pv_uzemanyagMAV)
    tarsadalmi_haszon_uzemanyagMAV.append(haszon_uzemanyagMAV)

    if t in [1, 2, 29]:
        print(f"{t}. év -> Társadalmi haszon: {fmt(haszon_uzemanyagMAV)} Ft | Jelenérték: {fmt(pv_uzemanyagMAV)}")
    osszes_tarasdalmihaszon_uzemanyagMAV = sum(tarsadalmi_haszon_uzemanyagMAV)
    osszes_jelenertek_uzemanyagMAV = sum(jelenertekek_uzemanyagMAV)

print(f"Az összes diszkontált társadalmi haszon {fmt(osszes_tarasdalmihaszon_uzemanyagMAV)} Forint társadalmi haszon, {fmt(osszes_jelenertek_uzemanyagMAV)} Forint nettó jelenértékű haszon.")

# 14. lépés - Rendkívüli események

print(f"\n--- Baleseti kockázatvizsgálat ---")

idoveszteseg_rendkivuli = int(input("Hány perces a legrövidebb kerülőútirány egy rendkívüli esemény bekövetkeztekor? "))
tobbletkm_rendkivuli = int(input("Mekkora a legkisebb kerülőútvonal egy rendkívüli esemény bekövetkeztekor? "))
forgalomkorlatozas_rendkivuli = int(input("Hány órán keresztül tart egy adott forgalomkorlátozás egy rendkívüli esemény bekövetkeztekor? "))

print(f"\n--- Baleseti kockázatvizsgálat a személygépjárművek vizsgálatában ---")

# 14.1 lépés - Rendkívüli események - Személygépjárművek

erintett_szgk_rendkivuli = szemelygepjarmu * (forgalomkorlatozas_rendkivuli / 24)
erintett_szemelyek_rendkivuli = erintett_szgk_rendkivuli * 1.5

print(f"A forgalomkorlátozás {round(erintett_szgk_rendkivuli, 1)} db személygépjárművet érintett.")
print(f"A forgalomkorlátozás {round(erintett_szemelyek_rendkivuli, 1)} személyt érintett.")

tarsadalmi_koltseg_szgk_rendkivuli_uzletiutazasingazas = ((erintett_szgk_rendkivuli * 0.25) * (idoveszteseg_rendkivuli / 60) * uzleti_utazasingazas_eredeti)
tarsadalmi_koltseg_szgk_rendkivuli_egyeb = ((erintett_szgk_rendkivuli * 0.75) * (idoveszteseg_rendkivuli / 60) * egyeb_utazas_eredeti)
tarsadalmi_koltseg_szgk_osszesen = tarsadalmi_koltseg_szgk_rendkivuli_uzletiutazasingazas + tarsadalmi_koltseg_szgk_rendkivuli_egyeb

print(f"Egy forgalomkorlátozás során összesen {fmt(tarsadalmi_koltseg_szgk_osszesen)} Forint társadalmi költség keletkezik a személygépjárművek kerülőútirány-igénybevétele miatt.")

tobbletkm_rendkivuli_osszes = tobbletkm_rendkivuli * erintett_szgk_rendkivuli
tobblet_uzemanyagfogyasztas_rendkivuli = tobbletkm_rendkivuli_osszes * 50

print(f"Egy forgalomkorlátozás során összesen {fmt(tobblet_uzemanyagfogyasztas_rendkivuli)} Forint üzemanyagköltség keletkezik 50 Ft/km-es fajlagos üzemanyag-költséggel számolva.")

elsoevi_tarsadalmikoltseg_szgk_rendkivuli = tarsadalmi_koltseg_szgk_osszesen + tobblet_uzemanyagfogyasztas_rendkivuli


baleseti_evek_input = input("Melyik években következik be baleset? (pl.: 3, 8, 13, 18, 23, 28) ")
if baleseti_evek_input.strip():
    baleseti_evek = [int(x.strip()) for x in baleseti_evek_input.split(",") if x.strip()]
else:
    baleseti_evek = [3, 8, 13, 18, 23, 28]

print(f"\n--- Baleseti kockázatvizsgálat a következő években: {baleseti_evek}")

b9 = elsoevi_tarsadalmikoltseg_szgk_rendkivuli
jelenertekek_szgk_baleset = []
tarsadalmi_hasznok_szgk_baleset = []
aktualis_haszon_szgk_baleset = b9

for t in range(1, 30):
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

    if t in baleseti_evek:
        print(f"{t}. év (Rendkívüli esemény) -> Névleges haszon: {fmt(ujhaszon_szgk_baleset)} Ft | Diszkontált haszon: {fmt(pv_szgk_baleset)}")

    osszes_tarsadalmihaszon_szgk_baleset = sum(tarsadalmi_hasznok_szgk_baleset)
    osszes_jelenertek_szgk_baleset = sum(jelenertekek_szgk_baleset)

print(f"\nAz összes névleges társadalmi haszon: {fmt(osszes_tarsadalmihaszon_szgk_baleset)} Ft")
print(f"Az összes diszkontált jelenértékű társadalmi haszon (ENPV): {fmt(osszes_jelenertek_szgk_baleset)} Ft")

print(f"\n--- Baleseti kockázatvizsgálat a tehergépjárművek vizsgálatában ---")

# 14.2 lépés - Rendkívüli események - Tehergépjárművek

erintett_teher_rendkivuli = (teher_celevre / 2.5) * (forgalomkorlatozas_rendkivuli / 24)

print(f"A forgalomkorlátozás {round(erintett_teher_rendkivuli, 1)} db tehergépjárművet érintett.")

teher_fajlagos_idoertek = 595
teher_rakomany = 18
erintett_rakomany = erintett_teher_rendkivuli * teher_rakomany

print(f"A forgalomkorlátozás {round(erintett_rakomany, 1)} tonna árut érintett.")

tarsadalmi_koltseg_teher_rendkivuli_osszesen = (erintett_rakomany * (idoveszteseg_rendkivuli / 60)) * teher_fajlagos_idoertek

print(f"Egy forgalomkorlátozás során összesen {fmt(tarsadalmi_koltseg_teher_rendkivuli_osszesen)} Forint társadalmi költség keletkezik a tehergépjárművek kerülőútirány-igénybevétele miatt.")

tobbletkm_teher_rendkivuli_osszes = tobbletkm_rendkivuli * erintett_teher_rendkivuli
tobblet_uzemanyagfogyasztas_teher_rendkivuli = tobbletkm_teher_rendkivuli_osszes * (0.325 * 681)

print(f"Egy forgalomkorlátozás során összesen {fmt(tobblet_uzemanyagfogyasztas_teher_rendkivuli)} Forint üzemanyagköltség keletkezik 221.325 Ft/km-es fajlagos üzemanyag-költséggel számolva.")

elsoevi_tarsadalmikoltseg_teher_rendkivuli = tarsadalmi_koltseg_teher_rendkivuli_osszesen + tobblet_uzemanyagfogyasztas_teher_rendkivuli

print(f"\n--- Baleseti kockázatvizsgálat a következő években: {baleseti_evek}")

b10 = elsoevi_tarsadalmikoltseg_teher_rendkivuli
jelenertekek_teher_baleset = []
tarsadalmi_hasznok_teher_baleset = []
aktualis_haszon_teher_baleset = b10

for t in range(1, 30):
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

    if t in baleseti_evek:
        print(f"{t}. év (Rendkívüli esemény) -> Névleges haszon: {fmt(ujhaszon_teher_baleset)} Ft | Diszkontált haszon: {fmt(pv_teher_baleset)}")

    osszes_tarsadalmihaszon_teher_baleset = sum(tarsadalmi_hasznok_teher_baleset)
    osszes_jelenertek_teher_baleset = sum(jelenertekek_teher_baleset)

print(f"\nAz összes névleges társadalmi haszon: {fmt(osszes_tarsadalmihaszon_teher_baleset)} Ft")
print(f"Az összes diszkontált jelenértékű társadalmi haszon (ENPV): {fmt(osszes_jelenertek_teher_baleset)} Ft")

print(f"\n--- Baleseti kockázatvizsgálat a vasúti személyszállítás vizsgálatában ---")

# 14.3 lépés - Rendkívüli események - Vasúti SZESZA

erintett_vonatok_SZESZA = int(input("Hány személyszállító vonatot érint egy rendkívüli esemény? "))
atlagos_keses_SZESZA = int(input("Mekkora az átlagos késése egy vonatnak rendkívüli eseménynél [perc]? "))
erintett_utasok_rendkivuli_SZESZA = int(input("Hány utast érint egy rendkívüli esemény? "))

print(f"A rendkívüli esemény {round(erintett_vonatok_SZESZA, 1)} db személyvonatot, {erintett_utasok_rendkivuli_SZESZA} utast érintett. Az átlagos késés {atlagos_keses_SZESZA} perc volt.")

elsoevi_tarsadalmikoltseg_rendkivuli_vasutiSZESZA = ((uzleti_utazasingazas_eredeti * (erintett_utasok_rendkivuli_SZESZA * 0.25)) * atlagos_keses_SZESZA / 60) + ((egyeb_utazas_eredeti * (erintett_utasok_rendkivuli_SZESZA * 0.75)) * atlagos_keses_SZESZA / 60)

print(f"Egy rendkívüli esemény során összesen {fmt(elsoevi_tarsadalmikoltseg_rendkivuli_vasutiSZESZA)} Forint társadalmi haszon keletkezik abból, hogy a vasúton utazók nem késnek.")

print(f"\n--- Baleseti kockázatvizsgálat a következő években: {baleseti_evek}")

b11 = elsoevi_tarsadalmikoltseg_rendkivuli_vasutiSZESZA
jelenertekek_vasutiszesza_baleset = []
tarsadalmi_hasznok_vasutiszesza_baleset = []
aktualis_haszon_vasutiszesza_baleset = b11

for t in range(1, 30):
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

    if t in baleseti_evek:
        print(f"{t}. év (Rendkívüli esemény) -> Névleges haszon: {fmt(ujhaszon_vasutiszesza_baleset)} Ft | Diszkontált haszon: {fmt(pv_vasutiszesza_baleset)}")

    osszes_tarsadalmihaszon_vasutiszesza_baleset = sum(tarsadalmi_hasznok_vasutiszesza_baleset)
    osszes_jelenertek_vasutiszesza_baleset = sum(jelenertekek_vasutiszesza_baleset)

print(f"\nAz összes névleges társadalmi haszon: {fmt(osszes_tarsadalmihaszon_vasutiszesza_baleset)} Ft")
print(f"Az összes diszkontált jelenértékű társadalmi haszon (ENPV): {fmt(osszes_jelenertek_vasutiszesza_baleset)} Ft")

# 14.3 lépés - Rendkívüli események - Vasúti teher

print(f"\n--- Baleseti kockázatvizsgálat a vasúti áruszállítás vizsgálatában ---")

erintett_vonatok_teher_rendkivuli = int(input("Hány teherszállító vonatot érint egy rendkívüli esemény? "))
atlagos_keses_teher = int(input("Mekkora az átlagos késése egy vonatnak rendkívüli eseménynél [perc]? "))
erintett_aruk_rendkivuli_SZESZA = (erintett_vonatok_teher_rendkivuli * (atlagos_keses_teher / 60)) * napi_atlagos_aru

print(f"A rendkívüli esemény {round(erintett_vonatok_teher_rendkivuli, 1)} db tehervonatot, {round(erintett_aruk_rendkivuli_SZESZA, 1)} tonna árut érintett. Az átlagos késés {atlagos_keses_teher} perc volt.")

elsoevi_tarsadalmikoltseg_rendkivuli_vasutiteher = erintett_aruk_rendkivuli_SZESZA * arutonna_fajlagoskoltseg_2026

print(f"Egy rendkívüli esemény során összesen {fmt(elsoevi_tarsadalmikoltseg_rendkivuli_vasutiteher)} Forint társadalmi haszon keletkezik abból, hogy a vasúton szállított áruk nem késnek.")

print(f"\n--- Baleseti kockázatvizsgálat a következő években: {baleseti_evek}")

b12 = elsoevi_tarsadalmikoltseg_rendkivuli_vasutiteher
jelenertekek_vasutiteher_baleset = []
tarsadalmi_hasznok_vasutiteher_baleset = []
aktualis_haszon_vasutiteher_baleset = b12

for t in range(1, 30):
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

    if t in baleseti_evek:
        print(f"{t}. év (Rendkívüli esemény) -> Névleges haszon: {fmt(ujhaszon_vasutiteher_baleset)} Ft | Diszkontált haszon: {fmt(pv_vasutiteher_baleset)}")

    osszes_tarsadalmihaszon_vasutiteher_baleset = sum(tarsadalmi_hasznok_vasutiteher_baleset)
    osszes_jelenertek_vasutiteher_baleset = sum(jelenertekek_vasutiteher_baleset)

print(f"\nAz összes névleges társadalmi haszon: {fmt(osszes_tarsadalmihaszon_vasutiteher_baleset)} Ft")
print(f"Az összes diszkontált jelenértékű társadalmi haszon (ENPV): {fmt(osszes_jelenertek_vasutiteher_baleset)} Ft")

# 15. lépés - Légszennyezés

print("\n--- Éves társadalmi hasznok a légszennyezésre nézve a járművek várakozásából adódóan ---")

szemelygepjarmu_fajlagosertek_externalia = 0.68 # eurócent/jkm
tehergepjarmu_fajlagosertek_externalia = 3.65 # eurócent/jkm

idoveszteseg_szemelygepjarmu = (szemelygepjarmu * (atlagos_varakozasi_ido / 60)) * 365 # 131 400
idoveszteseg_tehergepjarmu = ((teher_osszesen / 2.5) * (atlagos_varakozasi_ido / 60)) * 365 # 20 440

szemelygepjarmu_atlagfogyasztas = float(input("Mekkora a személygépjárművek átlagfogyasztása (l/100km)? "))
tehergepjarmu_atlagfogyasztas = float(input("Mekkora a tehergépjárművek átlagfogyasztása (l/100km)? "))

alapjarati_uzemanyagveszteseg_auto = idoveszteseg_szemelygepjarmu * 0.78 # 102 492
alapjarati_uzemanyagveszteseg_kamion = idoveszteseg_tehergepjarmu * 4.95 # 101 178

egyenertekes_futasteljesitmeny_auto = alapjarati_uzemanyagveszteseg_auto / (szemelygepjarmu_atlagfogyasztas / 100)
egyenertekes_futasteljesitmeny_kamion = alapjarati_uzemanyagveszteseg_kamion / (tehergepjarmu_atlagfogyasztas / 100)

eves_legszennyezesi_haszon_auto = egyenertekes_futasteljesitmeny_auto * szemelygepjarmu_fajlagosertek_externalia
eves_legszennyezesi_haszon_kamion = egyenertekes_futasteljesitmeny_kamion * tehergepjarmu_fajlagosertek_externalia
eves_legszennyezesi_haszon = eves_legszennyezesi_haszon_auto + eves_legszennyezesi_haszon_kamion

print(f"Az első évben a járművek várakozásából {fmt(eves_legszennyezesi_haszon)} forint társadalmi haszon keletkezik a légszennyezés externális hatásából.")

b13 = eves_legszennyezesi_haszon

jelenertekek_legszennyezes_varakozas = []
tarsadalmi_hasznok_legszennyezes_varakozas = []
aktualis_haszon_legszennyezes_varakozas = b13

for t in range(1, 30):
    if t == 1:
        haszon_legszennyezes_varakozas = b13
    else:
        haszon_legszennyezes_varakozas = aktualis_haszon_legszennyezes_varakozas * forgalom_novekedes
        aktualis_haszon_legszennyezes_varakozas = haszon_legszennyezes_varakozas

    pv_legszennyezes_varakozas = haszon_legszennyezes_varakozas / (diszkontrata ** t)
    jelenertekek_legszennyezes_varakozas.append(pv_legszennyezes_varakozas)
    tarsadalmi_hasznok_legszennyezes_varakozas.append(haszon_legszennyezes_varakozas)

    if t in [1, 2, 29]:
        print(f"{t}. év -> Társadalmi haszon: {fmt(haszon_legszennyezes_varakozas)} Ft | Jelenérték: {fmt(pv_legszennyezes_varakozas)}")

osszes_tarsadalmi_haszon_legszennyezes_varakozas = sum(tarsadalmi_hasznok_legszennyezes_varakozas)
osszes_diszkontalt_haszon_legszennyezes_varakozas = sum(jelenertekek_legszennyezes_varakozas)

print(f"Az összes diszkontált társadalmi haszon {fmt(osszes_tarsadalmi_haszon_legszennyezes_varakozas)} Forint társadalmi haszon, {fmt(osszes_diszkontalt_haszon_legszennyezes_varakozas)} Forint nettó jelenértékű haszon")

# 15.2 lépés - Légszennyezés_baleset

print("\n--- Éves társadalmi hasznok a légszennyezésre nézve a rendkívüli események miatti kerülőútvonal miatt ---")

erintett_szgk_rendkivuli = szemelygepjarmu * (forgalomkorlatozas_rendkivuli / 24)

print(f"A forgalomkorlátozás {round(erintett_szgk_rendkivuli, 1)} db személygépjárművet érintett.")

erintett_teher_rendkivuli = (teher_celevre / 2.5) * (forgalomkorlatozas_rendkivuli / 24)

print(f"A forgalomkorlátozás {round(erintett_teher_rendkivuli, 1)} db tehergépjárművet érintett.")

tobbletfutas_auto = erintett_szgk_rendkivuli * tobbletkm_rendkivuli
tobbletfutas_kamion = erintett_teher_rendkivuli * tobbletkm_rendkivuli

print(f"A személygépjárművek többletfutása {round(tobbletfutas_auto, 1)} km, a tehergépjárműveké {round(tobbletfutas_kamion, 1)} km.")

eves_legszennyezesi_haszon_tobbletfutas = (tobbletfutas_auto * szemelygepjarmu_fajlagosertek_externalia) + (tobbletfutas_kamion * tehergepjarmu_fajlagosertek_externalia)

b14 = eves_legszennyezesi_haszon_tobbletfutas

jelenertekek_legszennyezes_tobbletfutas = []
tarsadalmi_hasznok_legszennyezes_tobbletfutas = []
aktualis_haszon_legszennyezes_tobbletfutas = b14

for t in range(1, 30):
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

    if t in baleseti_evek:
        print(f"{t}. év (Rendkívüli esemény) -> Névleges haszon: {fmt(ujhaszon_legszennyezes_tobbletfutas)} Ft | Diszkontált haszon: {fmt(pv_legszennyezes_tobbletfutas)}")

    osszes_tarsadalmihaszon_legszennyezes_tobbletfutas = sum(tarsadalmi_hasznok_legszennyezes_tobbletfutas)
    osszes_jelenertek_legszennyezes_tobbletfutas = sum(jelenertekek_legszennyezes_tobbletfutas)

print(f"\nAz összes névleges társadalmi haszon: {fmt(osszes_tarsadalmihaszon_legszennyezes_tobbletfutas)} Ft")
print(f"Az összes diszkontált jelenértékű társadalmi haszon (ENPV): {fmt(osszes_jelenertek_legszennyezes_tobbletfutas)} Ft")

# 16. lépés - Éghajlatváltozás

print("\n--- Éves társadalmi hasznok az éghajlatváltozásra nézve a járművek várakozásából adódóan ---")

fajlagos_arnyekar_2026 = 50.688
print("\n--- A fajlagos árnyékár 2026-ra vonatkozóan 50,688 Ft/kg CO2 kibocsátási költséget jelent ---")
fajlagoskar_auto_eghajlatvaltozas = fajlagos_arnyekar_2026 * 0.180
fajlagoskar_kamion_eghajlatvaltozas = fajlagos_arnyekar_2026 * 0.848
print("\n--- Egy személygépjármű 180 g CO2-t, egy tehergépjármű 848 g CO2-t emittál egy km alatt. ---")

eves_eghajlatvaltoasi_haszon = (egyenertekes_futasteljesitmeny_auto * fajlagoskar_auto_eghajlatvaltozas) + (egyenertekes_futasteljesitmeny_kamion * fajlagoskar_kamion_eghajlatvaltozas)

print(f"Az első évben a járművek várakozásából {fmt(eves_eghajlatvaltoasi_haszon)} forint társadalmi haszon keletkezik az éghajlatváltozás externális hatásából.")

b14 = eves_eghajlatvaltoasi_haszon

jelenertekek_eghajlatvaltozas_varakozas = []
tarsadalmi_hasznok_eghajlatvaltozas_varakozas = []
aktualis_haszon_eghajlatvaltozas_varakozas = b14

for t in range(1, 30):
    if t == 1:
        haszon_eghajlatvaltozas_varakozas = b14
    else:
        haszon_eghajlatvaltozas_varakozas = aktualis_haszon_eghajlatvaltozas_varakozas * forgalom_novekedes
        aktualis_haszon_eghajlatvaltozas_varakozas = haszon_eghajlatvaltozas_varakozas

    pv_eghajlatvaltozas_varakozas = haszon_eghajlatvaltozas_varakozas / (diszkontrata ** t)
    jelenertekek_eghajlatvaltozas_varakozas.append(pv_eghajlatvaltozas_varakozas)
    tarsadalmi_hasznok_eghajlatvaltozas_varakozas.append(haszon_eghajlatvaltozas_varakozas)

    if t in [1, 2, 29]:
        print(f"{t}. év -> Társadalmi haszon: {fmt(haszon_eghajlatvaltozas_varakozas)} Ft | Jelenérték: {fmt(pv_eghajlatvaltozas_varakozas)}")

osszes_tarsadalmi_haszon_eghajlatvaltozas_varakozas = sum(tarsadalmi_hasznok_eghajlatvaltozas_varakozas)
osszes_diszkontalt_haszon_eghajlatvaltozas_varakozas = sum(jelenertekek_eghajlatvaltozas_varakozas)

print(f"Az összes diszkontált társadalmi haszon {fmt(osszes_tarsadalmi_haszon_eghajlatvaltozas_varakozas)} Forint társadalmi haszon, {fmt(osszes_diszkontalt_haszon_eghajlatvaltozas_varakozas)} Forint nettó jelenértékű haszon")

# 16.2 lépés - Éghajlatváltozás rendkívüli eseményeknél

print("\n--- Éves társadalmi hasznok az éghajlatváltozásra nézve a rendkívüli események miatti kerülőútvonal miatt ---")

erintett_szgk_rendkivuli = szemelygepjarmu * (forgalomkorlatozas_rendkivuli / 24)
print(f"A forgalomkorlátozás {round(erintett_szgk_rendkivuli, 1)} db személygépjárművet érintett.")
erintett_teher_rendkivuli = (teher_celevre / 2.5) * (forgalomkorlatozas_rendkivuli / 24)
print(f"A forgalomkorlátozás {round(erintett_teher_rendkivuli, 1)} db tehergépjárművet érintett.")
print(f"A személygépjárművek többletfutása {round(tobbletfutas_auto, 1)} km, a tehergépjárműveké {round(tobbletfutas_kamion, 1)} km.")
eves_eghajlatvaltozasi_haszon_tobbletfutas = (tobbletfutas_auto * fajlagoskar_auto_eghajlatvaltozas) + (tobbletfutas_kamion * fajlagoskar_kamion_eghajlatvaltozas)

b16 = eves_eghajlatvaltozasi_haszon_tobbletfutas

jelenertekek_eghajlatvaltozas_tobbletfutas = []
tarsadalmi_hasznok_eghajlatvaltozas_tobbletfutas = []
aktualis_haszon_eghajlatvaltozas_tobbletfutas = b16

for t in range(1, 30):
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

    if t in baleseti_evek:
        print(f"{t}. év (Rendkívüli esemény) -> Névleges haszon: {fmt(ujhaszon_eghajlatvaltozas_tobbletfutas)} Ft | Diszkontált haszon: {fmt(pv_eghajlatvaltozas_tobbletfutas)}")

    osszes_tarsadalmihaszon_eghajlatvaltozas_tobbletfutas = sum(tarsadalmi_hasznok_eghajlatvaltozas_tobbletfutas)
    osszes_jelenertek_eghajlatvaltozas_tobbletfutas = sum(jelenertekek_eghajlatvaltozas_tobbletfutas)

print(f"\nAz összes névleges társadalmi haszon: {fmt(osszes_tarsadalmihaszon_eghajlatvaltozas_tobbletfutas)} Ft")
print(f"Az összes diszkontált jelenértékű társadalmi haszon (ENPV): {fmt(osszes_jelenertek_eghajlatvaltozas_tobbletfutas)} Ft")

# 17. lépés - Zajszennyezés

print("\n--- Éves társadalmi hasznok a zajszennyezésre nézve a járművek várakozásából ---")

nappali_autok = szemelygepjarmu * (14/24)
ejszakai_autok = szemelygepjarmu * (10/24)
print(f"A fajlagos zajkár értéke nappali személygépjárműveknél 0,105 eurócent/járműkm, éjszakai személygépjárműveknél 0,195 eurócent/járműkm (2019).")
atlagos_zajkar = ((nappali_autok * 0.105) + (ejszakai_autok * 0.195)) / szemelygepjarmu
atlagos_zajkar_korrigalva = atlagos_zajkar * (0.01 * 1.3287 * 384)

zajkar_autok = egyenertekes_futasteljesitmeny_auto * atlagos_zajkar_korrigalva
print(f"A személygépjárművek várakozására eső éves zajterhelési kár {round(zajkar_autok, 1)} Ft/év.")

nappali_kamion = (teher_osszesen) * (14/24)
ejszaka_kamion = teher_osszesen * (10/24)
print(f"A fajlagos zajkár értéke nappali tehergépjárműveknél 1.62 eurócent/járműkm, éjszakai tehergépjárműveknél 3.06 eurócent/járműkm (2019).")
atlagos_zajkar_teher = ((nappali_kamion * 1.62) + (ejszaka_kamion * 3.06)) / teher_osszesen
atlagos_zajkar_teher_korrigalva = atlagos_zajkar_teher * (0.01 * 1.3287 * 384)

zajkar_teher = egyenertekes_futasteljesitmeny_kamion * atlagos_zajkar_teher_korrigalva
print(f"A tehergépjárművek várakozására eső éves zajterhelési kár {round(zajkar_teher, 1)} Ft/év.")
zajkar_osszesen = zajkar_autok + zajkar_teher

b17 = zajkar_osszesen

jelenertekek_zajkar_varakozas = []
tarsadalmi_hasznok_zajkar_varakozas = []
aktualis_haszon_zajkar_varakozas = b17

for t in range(1, 30):
    if t == 1:
        haszon_zajkar_varakozas = b17
    else:
        haszon_zajkar_varakozas = aktualis_haszon_zajkar_varakozas * forgalom_novekedes
        aktualis_haszon_zajkar_varakozas = haszon_zajkar_varakozas

    pv_zajkar_varakozas = haszon_zajkar_varakozas / (diszkontrata ** t)
    jelenertekek_zajkar_varakozas.append(pv_zajkar_varakozas)
    tarsadalmi_hasznok_zajkar_varakozas.append(haszon_zajkar_varakozas)

    if t in [1, 2, 29]:
        print(f"{t}. év -> Társadalmi haszon: {fmt(haszon_zajkar_varakozas)} Ft | Jelenérték: {fmt(pv_zajkar_varakozas)}")

osszes_tarsadalmi_haszon_zajkar_varakozas = sum(tarsadalmi_hasznok_zajkar_varakozas)
osszes_diszkontalt_haszon_zajkar_varakozas = sum(jelenertekek_zajkar_varakozas)

print(f"Az összes diszkontált társadalmi haszon {fmt(osszes_tarsadalmi_haszon_zajkar_varakozas)} Forint társadalmi haszon, {fmt(osszes_diszkontalt_haszon_zajkar_varakozas)} Forint nettó jelenértékű haszon")

# 18. lépés - Nettó jelenérték meghatározása

print("\n--- Közgazdasági nettó jelenérték (ENPV) ---")

haszon_jelenertek_lista = [
    jelenertekek,
    jelenertekek_teher,
    jelenertekek_vasutIC,
    jelenertekek_vasutszemely,
    jelenertekek_vasutaru,
    jelenertekek_baleset,
    jelenertekek_csaporud,
    jelenertekek_uzemanyagMAV,
    jelenertekek_szgk_baleset,
    jelenertekek_teher_baleset,
    jelenertekek_vasutiszesza_baleset,
    jelenertekek_vasutiteher_baleset,
    jelenertekek_legszennyezes_varakozas,
    jelenertekek_legszennyezes_tobbletfutas,
    jelenertekek_eghajlatvaltozas_varakozas,
    jelenertekek_eghajlatvaltozas_tobbletfutas,
    jelenertekek_zajkar_varakozas
]

eves_diszkontalt_hasznok = [sum(lista[t] for lista in haszon_jelenertek_lista) for t in range(29)]
osszes_diszkontalt_haszon = sum(eves_diszkontalt_hasznok)

eves_diszkontalt_mukodesikoltseg = [teljes_mukodesi_koltseg / (1.03 ** (t+1)) for t in range(29)]
osszes_diszkontalt_mukodesikoltseg = sum(eves_diszkontalt_mukodesikoltseg)

teljes_maradvanyertek = feluljaro_maradvanyertek + korforgalom_maradvanyertek
diszkontalt_maradvanyertek = teljes_maradvanyertek / (1.03 ** 29)

enpv = -teljes_beruhazasi_koltseg - osszes_diszkontalt_mukodesikoltseg + diszkontalt_maradvanyertek + osszes_diszkontalt_haszon

print(f"\n-------------------------------------------------------------")
print(f"KÖZGAZDASÁGI NETTÓ JELENÉRTÉK (ENPV): {fmt(enpv)} FT")
print("-------------------------------------------------------------")

# 19. lépés - Gazdasági belső megtérülési ráta kiszámítása

print("\n--- Közgazdasági belső megtérülési ráta (ERR) ---")

haszon_nevleges_lista = [
    tarsadalmi_hasznok,
    tarsadalmi_hasznok_teher,
    tarsadalmi_hasznok_vasutIC,
    tarsadalmi_hasznok_vasutszemely,
    tarsadalmi_hasznok_vasutaru,
    tarsadalmi_hasznok_baleset,
    tarsadalmihasznok_csaporud,
    tarsadalmi_haszon_uzemanyagMAV,
    tarsadalmi_hasznok_szgk_baleset,
    tarsadalmi_hasznok_teher_baleset,
    tarsadalmi_hasznok_vasutiszesza_baleset,
    tarsadalmi_hasznok_vasutiteher_baleset,
    tarsadalmi_hasznok_legszennyezes_varakozas,
    tarsadalmi_hasznok_legszennyezes_tobbletfutas,
    tarsadalmi_hasznok_eghajlatvaltozas_varakozas,
    tarsadalmi_hasznok_eghajlatvaltozas_tobbletfutas,
    tarsadalmi_hasznok_zajkar_varakozas
]

penzaramok = [-teljes_beruhazasi_koltseg]

for t in range(29):
    eves_haszon_nevleges = sum(lista[t] for lista in haszon_nevleges_lista)

    eves_netto = eves_haszon_nevleges - teljes_mukodesi_koltseg

    if t == 28:
        eves_netto += teljes_maradvanyertek

    penzaramok.append(eves_netto)

def szamol_err(cf_lista):
    try:
        import numpy_financial as npf
        return npf.irr(cf_lista)
    except ImportError:
        def npv_f(r):
            return sum(cf / ((1+ r) ** t) for t, cf in enumerate(cf_lista))

        low, high = 0.0, 2.0
        for _ in range(100):
            mid = (low + high) / 2
            val = npv_f(mid)
            if abs(val) < 1e-2:
                return mid
            if val > 0:
                low = mid
            else:
                high = mid
        return mid

err_ertek = szamol_err(penzaramok)

print(f"GAZDASÁGI BELSŐ MEGTÉRÜLÉSI RÁTA (ERR): {err_ertek * 100:.2f} %")
print(f"Elvárt társadalmi diszkontráta:          3.00 %")
if err_ertek > 0.03:
    print("ÉRTÉKELÉS: Az ERR > 3%, a beruházás társadalmilag megtérülő!")

# 20. lépés - Haszon-költség arány

print("\n--- Közgazdasági belső megtérülési ráta (BCR) ---")

osszes_lediszkontalt_netto_haszon = (osszes_diszkontalt_haszon - osszes_diszkontalt_mukodesikoltseg + diszkontalt_maradvanyertek)

bcr = osszes_lediszkontalt_netto_haszon / teljes_beruhazasi_koltseg

print(f"Kezdeti beruházási költség: {fmt(teljes_beruhazasi_koltseg)} Ft.")
print(f"Lediszkontált nettó társadalmi hasznok: {fmt(osszes_lediszkontalt_netto_haszon)} Ft.")
print(f"Haszon-költség arány: {bcr:.2f}")

if bcr > 1.0:
    print("Értékelés: Mivel BCR > 1, a beruházás társadalmilag megtérülő!")

# 21. lépés - Érzékenységvizsgálat

print("\n--- Érzékenységvizsgálat ---")

beruhazas_valtozasok = [-0.20, -0.10, 0.00, 0.10, 0.20, 0.50]
haszon_valtozasok = [-0.30, -0.20, -0.10, 0.00, 0.10, 0.20]

bcr_matrix = []

for c_var in beruhazas_valtozasok:
    row = []
    uj_beruhazas = teljes_beruhazasi_koltseg * (1 + c_var)
    for h_var in haszon_valtozasok:
        uj_netto_haszon = osszes_lediszkontalt_netto_haszon * (1 + h_var)
        uj_bcr = uj_netto_haszon / uj_beruhazas
        row.append(round(uj_bcr, 2))
    bcr_matrix.append(row)

df_bcr_erzekenyseg = pd.DataFrame(
    bcr_matrix,
    index=[f"Beruházási költség {c*100:+.0f}%" for c in beruhazas_valtozasok],
    columns=[f"Haszon {h*100:+.0f}%" for h in haszon_valtozasok]
)

print("\nHaszon-Költség Arány Érzékenységi Mátrix:")
print(df_bcr_erzekenyseg.to_string())




