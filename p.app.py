import streamlit as st
from supabase import create_client, Client
import pandas as pd

# --- KONFIGURACJA POŁĄCZENIA ---
# Dane pobieramy ze Streamlit Secrets dla bezpieczeństwa
URL = st.secrets["SUPABASE_URL"]
KEY = st.secrets["SUPABASE_KEY"]

@st.cache_resource
def get_supabase_client() -> Client:
    return create_client(URL, KEY)

supabase = get_supabase_client()

# --- FUNKCJE LOGIKI ---
def get_data(table_name):
    response = supabase.table(table_name).select("*").execute()
    return pd.DataFrame(response.data)

def add_category(nazwa, opis):
    supabase.table("kategorie").insert({"nazwa": nazwa, "opis": opis}).execute()

def add_product(nazwa, liczba, cena, kategoria_id):
    supabase.table("produkt").insert({
        "produkty": nazwa, 
        "liczba": liczba, 
        "cena": cena, 
        "kategoria_id": kategoria_id
    }).execute()

def delete_item(table, item_id):
    supabase.table(table).delete().eq("id", item_id).execute()

# --- INTERFEJS STREAMLIT ---
st.set_page_config(page_title="Supabase + Streamlit", layout="wide")
st.title("☁️ Zarządzanie Magazynem (Supabase)")

tab_prod, tab_kat = st.tabs(["📦 Produkty", "📂 Kategorie"])

# --- ZAKŁADKA: KATEGORIE ---
with tab_kat:
    st.header("Kategorie")
    with st.form("form_kat"):
        nazwa = st.text_input("Nazwa kategorii")
        opis = st.text_area("Opis")
        if st.form_submit_button("Dodaj"):
            add_category(nazwa, opis)
            st.success("Dodano kategorię!")
            st.rerun()

    df_kat = get_data("kategorie")
    st.dataframe(df_kat, use_container_width=True)
    
    if not df_kat.empty:
        to_del = st.selectbox("Usuń kategorię (ID)", df_kat['id'])
        if st.button("Usuń kategorię"):
            delete_item("kategorie", to_del)
            st.rerun()

# --- ZAKŁADKA: PRODUKTY ---
with tab_prod:
    st.header("Produkty")
    df_kat_check = get_data("kategorie")
    
    if df_kat_check.empty:
        st.warning("Dodaj najpierw kategorię!")
    else:
        with st.form("form_prod"):
            p_nazwa = st.text_input("Nazwa produktu (kolumna 'produkty')")
            p_liczba = st.number_input("Liczba", step=1)
            p_cena = st.number_input("Cena", step=0.01)
            kat_map = dict(zip(df_kat_check['nazwa'], df_kat_check['id']))
            p_kat = st.selectbox("Kategoria", options=list(kat_map.keys()))
            
            if st.form_submit_button("Dodaj produkt"):
                add_product(p_nazwa, p_liczba, p_cena, kat_map[p_kat])
                st.rerun()

    # Wyświetlanie produktów z JOINem (pobieramy nazwę kategorii)
    res = supabase.table("produkt").select("*, kategorie(nazwa)").execute()
    if res.data:
        df_p = pd.json_normalize(res.data) # Rozbicie zagnieżdżonych danych kategorii
        st.dataframe(df_p, use_container_width=True)
        
        prod_del = st.selectbox("Usuń produkt (ID)", df_p['id'])
        if st.button("Usuń produkt"):
            delete_item("produkt", prod_del)
            st.rerun()
