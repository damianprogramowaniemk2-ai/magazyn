import streamlit as st

# --- KONFIGURACJA ŚWIĄTECZNEGO TŁA I STYLI (CSS) ---
def inject_christmas_theme():
    """
    Funkcja wstrzykująca CSS dla efektu śniegu i stylizacji choinki.
    Wykorzystuje trik z wieloma gradientami tła, aby symulować płatki śniegu bez użycia obrazków.
    """
    christmas_css = """
    <style>
        /* 1. Tło aplikacji - ciemne niebo */
        .stApp {
            background-color: #1a2a3a; /* Ciemnoniebieskie tło */
            background-image: 
                radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 4px),
                radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 3px),
                radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 4px);
            background-size: 550px 550px, 350px 350px, 250px 250px;
            background-position: 0 0, 0 0, 0 0;
            animation: snow 15s linear infinite;
        }

        /* 2. Animacja padania śniegu */
        @keyframes snow {
            0% { background-position: 0px 0px, 0px 0px, 0px 0px; }
            100% { background-position: 550px 1000px, 350px 600px, 250px 400px; }
        }

        /* 3. Stylizacja tekstów, aby były czytelne na ciemnym tle */
        h1, h2, h3, p, div, label, .stMarkdown {
            color: #ffffff !important;
        }
        /* Styl dla choinki emoji */
        .tree-container {
            text-align: center;
            font-size: 80px;
            margin-bottom: -20px;
            text-shadow: 0 0 15px #fff, 0 0 30px #2ecc71; /* Świąteczna poświata */
        }
    </style>
    """
    # Wstrzyknięcie CSS do aplikacji
    st.markdown(christmas_css, unsafe_allow_html=True)

# --- GŁÓWNA APLIKACJA ---
def main():
    # Najpierw ładujemy motyw świąteczny
    inject_christmas_theme()

    # Dodajemy choinkę jako element HTML na górze
    st.markdown('<div class="tree-container">🎄</div>', unsafe_allow_html=True)
    
    st.title("Świąteczny Magazyn")

    # Inicjalizacja stanu aplikacji (Session State)
    if 'produkty' not in st.session_state:
        st.session_state.produkty = ["Prezent dla Mikołaja", "Worek węgla"] # Dodałem przykładowe produkty na start

    # --- Sekcja 1: Dodawanie produktu ---
    st.header("Dodaj produkt")
    nowy_produkt = st.text_input("Wpisz nazwę produktu", placeholder="np. Bombki choinkowe")

    if st.button("Dodaj 🎁"):
        if nowy_produkt:
            st.session_state.produkty.append(nowy_produkt)
            st.success(f"Dodano do worka: {nowy_produkt}")
            st.rerun()
        else:
            st.warning("Wpisz nazwę produktu przed dodaniem.")

    st.divider()

    # --- Sekcja 2: Lista i Usuwanie ---
    st.header("Stan Magazynu")

    if st.session_state.produkty:
        st.write("Twoje produkty:")
        for idx, produkt in enumerate(st.session_state.produkty, 1):
            # Używam st.markdown dla ładniejszej listy z kropkami
            st.markdown(f"❄️ **{idx}.** {produkt}")

        st.divider()

        st.subheader("Usuń produkt")
        produkt_do_usuniecia = st.selectbox(
            "Wybierz produkt do usunięcia", 
            options=st.session_state.produkty
        )

        # Zmiana koloru przycisku usuwania na czerwony (stylizacja Streamlit)
        if st.button("Usuń wybrany 🗑️", type="primary"):
            if produkt_do_usuniecia in st.session_state.produkty:
                st.session_state.produkty.remove(produkt_do_usuniecia)
                st.success(f"Usunięto: {produkt_do_usuniecia}")
                st.rerun()
    else:
        st.info("Magazyn jest pusty. Mikołaj wszystko rozdał!")

if __name__ == "__main__":
    main()
