import streamlit as st
import os
import time
import re
import img2pdf
from bs4 import BeautifulSoup
from scrape import getComicList
import requests
import pandas as pd
from gemini import geminiSearch

def getChapters(manga):
    st.subheader(manga["title"])
    with st.sidebar:
        st.image(manga["image"], width=150)
        st.markdown(f"**{manga['title']}**")
        if st.button("⬅️ Kembali ke Daftar Komik", use_container_width=True, type="primary"):
                st.session_state.selected_manga = None
                st.session_state.chapters_limit = 10  # reset limit
                st.rerun()
                
    if "chapters_limit" not in st.session_state:
        st.session_state.chapters_limit = 10

    try:
        resp = requests.get(manga["link"], headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        if resp.status_code != 200:
            st.error("Gagal mengambil halaman detail komik.")
            return

        soup = BeautifulSoup(resp.text, "html.parser")

        desc_elem = soup.select_one("div.summary__content")
        description = desc_elem.get_text(strip=True) if desc_elem else "Deskripsi tidak ditemukan."

        chapters = []
        for ch in soup.select("ul.main.version-chap li.wp-manga-chapter"):
            ch_title = ch.select_one("a").get_text(strip=True)
            ch_link = ch.select_one("a")["href"]
            ch_date = ch.select_one("span.chapter-release-date i")
            ch_date = ch_date.get_text(strip=True) if ch_date else ""
            chapters.append({"title": ch_title, "link": ch_link, "date": ch_date})

        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(manga["image"], width=300)
        with col2:
            st.markdown("### 🧾 Deskripsi")
            st.write(description)
            st.markdown(f"🔗 [Buka di Browser]({manga['link']})")

        st.markdown("---")
        st.markdown("### 📜 Daftar Chapter")

        if not chapters:
            st.warning("Belum ada chapter yang ditemukan.")
        else:
            visible_chapters = chapters[:st.session_state.chapters_limit]
            cols = st.columns(5)
            for i, ch in enumerate(visible_chapters):
                with cols[i % 5]:
                    st.markdown(
                        f"<p style='margin-bottom:4px;'>"
                        f"📖 <a href='{ch['link']}' target='_blank'>{ch['title']}</a><br>"
                        f"<span style='color:gray; font-size:0.8em;'>{ch['date']}</span>"
                        f"</p>",
                        unsafe_allow_html=True
                    )
            if st.session_state.chapters_limit < len(chapters):
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("⬇️ Tampilkan Lebih Banyak Chapter", use_container_width=True):
                    st.session_state.chapters_limit += 10
                    st.rerun()
            else:
                st.info("✅ Semua chapter sudah ditampilkan.")

    except Exception as e:
        st.error(f"Terjadi kesalahan saat scraping detail: {e}")
def download_images(image_urls, manga_slug, ch_link, base_dir, st_status):
    pass
def convertPDF(mangaDirectory, st_status):
    pass

def display_manga_grid():
    prompt = st.sidebar.text_input("Tanya Gemini")
    if prompt:
            geminiSearch(prompt)
    else:
        st.sidebar.header("Filter Komik")
        filter_type = st.sidebar.selectbox(
                "Pilih jenis komik:",
                ["Semua", "manga", "manhwa", "manhua"],
                key="selected_filter"
        )
        if filter_type != 'Semua':
                order_type = st.sidebar.selectbox(
                        "Order By:",
                        ["latest", "alphabet", "rating", "trending", "views", "new-manga"],
                        key="selected_order"
                )
    if st.sidebar.button("📥 Ambil Daftar Komik", type="primary"):
        st.session_state.current_page = 1 
        st.session_state.current_filter = None if filter_type == "Semua" else filter_type
        if st.session_state.current_filter != None:
                st.session_state.order_by = None if order_type == "latest" else order_type
        st.session_state.search_active = True
        st.rerun()

    if st.session_state.search_active:
        current_page = st.session_state.current_page
        current_filter = st.session_state.current_filter
        if current_filter != None:
                order_by = st.session_state.order_by
        
        with st.spinner(f"Mengambil data halaman {current_page} untuk '{current_filter or 'Semua'}'..."):
            if current_filter:
                mangas = getComicList(current_filter, current_page, order_by)
            else:
                mangas = getComicList(current_filter, current_page)
            
            if mangas:
                st.success(f"Berhasil mengambil {len(mangas)} komik (Halaman {current_page})")
                cols = st.columns(4)
                for i, manga in enumerate(mangas):
                    with cols[i % 4]:
                        with st.container(border=True):
                            st.image(manga["image"], width= "stretch")
                            st.markdown(
                                f"<p style='text-align: center; font-weight: bold; height: 3em; overflow: hidden;'>"
                                f"{manga['title']}"
                                f"</p>", 
                                unsafe_allow_html=True
                            )
                            if st.button("Pilih Manga Ini", key=manga['slug'], use_container_width=True):
                                st.session_state.selected_manga = manga
                                st.rerun() 
            else:
                st.warning("Tidak ada komik ditemukan di halaman ini.")
                
            st.divider()
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                if st.button("⬅️ Halaman Sebelumnya", use_container_width=True, disabled=(current_page == 1)):
                    st.session_state.current_page -= 1
                    st.rerun()
            
            with col2:
                st.markdown(f"<h3 style='text-align: center;'>Halaman {current_page}</h3>", unsafe_allow_html=True)
            
            with col3:
                if st.button("Halaman Berikutnya ➡️", use_container_width=True, disabled=(not mangas)):
                    st.session_state.current_page += 1
                    st.rerun()

def display_downloader_ui():
    st.header("Download ")
    st.info("Sek-sek masih development le")

    manga = st.session_state.selected_manga
    st.sidebar.image(manga['image'])
    st.sidebar.markdown(f"**{manga['title']}**")
    if st.sidebar.button("⬅️ Kembali ke Daftar Komik"):
        st.session_state.selected_manga = None
        st.rerun()

def main():
    st.set_page_config(page_title="Duta Comic", layout="wide")
    st.title("📚 Duta Comic Reader & Downloader")

    if 'selected_manga' not in st.session_state:
        st.session_state.selected_manga = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 1
    if 'current_filter' not in st.session_state:
        st.session_state.current_filter = None
    if 'order_by' not in st.session_state:
        st.session_state.order_by = None
    if 'search_active' not in st.session_state:
        st.session_state.search_active = False 
        
    if st.session_state.selected_manga:
        getChapters(st.session_state.selected_manga)
    else:
        display_manga_grid()

if __name__ == "__main__":
    main()