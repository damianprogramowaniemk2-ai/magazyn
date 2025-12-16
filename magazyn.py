import streamlit as st

def main():
    st.title("📦 Prosty Magazyn")

    # Inicjalizacja stanu aplikacji (Session State)
    # Streamlit odświeża kod przy każdej akcji, więc musimy trzymać listę w pamięci podręcznej
    if 'produkty' not in st.session_state:
        st.session_state.produkty = []

    # --- Sekcja 1: Dodawanie produktu ---
    st.header("Dodaj produkt")
    nowy_produkt = st.text_input("Wpisz nazwę produktu", placeholder="np. Młotek")

    if st.button("Dodaj"):
        if nowy_produkt:
            # Dodajemy do listy w pamięci
            st.session_state.produkty.append(nowy_produkt)
            st.success(f"Dodano: {nowy_produkt}")
            # Rerun wymusza odświeżenie strony, by zaktualizować listy od razu
            st.rerun()
        else:
            st.warning("Wpisz nazwę produktu przed dodaniem.")

    st.divider()

    # --- Sekcja 2: Lista i Usuwanie ---
    st.header("Stan Magazynu")

    if st.session_state.produkty:
        # Wyświetlanie listy
        st.write("Twoje produkty:")
        for idx, produkt in enumerate(st.session_state.produkty, 1):
            st.text(f"{idx}. {produkt}")

        st.divider()

        # Usuwanie produktu
        st.subheader("Usuń produkt")
        # Selectbox pozwala wybrać produkt z obecnej listy
        produkt_do_usuniecia = st.selectbox(
            "Wybierz produkt do usunięcia", 
            options=st.session_state.produkty
        )

        if st.button("Usuń wybrany"):
            if produkt_do_usuniecia in st.session_state.produkty:
                st.session_state.produkty.remove(produkt_do_usuniecia)
                st.success(f"Usunięto: {produkt_do_usuniecia}")
                st.rerun()
    else:
        st.info("Magazyn jest pusty.")

if __name__ == "__main__":
    main()
