import streamlit as st
import requests
import os
import time
import re
import img2pdf
import shutil
from bs4 import BeautifulSoup

BASE_API = 'https://www.mangaread.org/'

def getComicList(filter=None):
    try:
        if filter:
            # Menggunakan URL yang benar dari kode Anda
            url = f"{BASE_API}genres/{filter}/"
        else:
            url = BASE_API
            
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            comics = []
            
            for item in soup.select("div.page-item-detail"):
                title_link_elem = item.select_one("div.item-summary h3.h5 a")
                img_elem = item.select_one("div.item-thumb a img")

                if not (title_link_elem and img_elem):
                    continue

                link = title_link_elem["href"]
                
                # Ekstrak 'slug' dari link. Cth: 'a-returners-magic-should-be-special-manga'
                slug = link.split('/manga/')[1].strip('/')

                comics.append({
                    "title": title_link_elem.get_text(strip=True),
                    "link": link,
                    "image": img_elem.get("data-src") or img_elem.get("src"),
                    "slug": slug  # Slug ini akan kita gunakan untuk downloader
                })

            return comics
        else:
            st.warning(f"Gagal mengambil data (status {resp.status_code})")
            return []
    except Exception as e:
        st.error(f"Terjadi kesalahan saat mengambil data: {e}")
        return []
    
def getChapters(manga_slug, Ch_Start, Ch_End, st_status):
    pass

def scrape_img(ch_link, st_status):
    pass

def download_images(image_urls, manga_slug, ch_link, base_dir, st_status):
    pass

def convertPDF(mangaDirectory, st_status):
    pass

def display_manga_grid():
    st.sidebar.header("Filter Komik")
    filter_type = st.sidebar.selectbox(
        "Pilih jenis komik:",
        ["Semua", "manga", "manhwa", "manhua"]
    )
    filter_type = None if filter_type == "Semua" else filter_type

    if st.sidebar.button("📥 Ambil Daftar Komik", type="primary"):
        with st.spinner("Mengambil data dari Mangaread..."):
            mangas = getComicList(filter_type)
            if mangas:
                st.success(f"Berhasil mengambil {len(mangas)} komik!")
                
                cols = st.columns(4)
                for i, manga in enumerate(mangas):
                    with cols[i % 4]:
                        with st.container(border=True):
                            st.image(manga["image"])
                            st.markdown(
                                f"<p style='text-align: center; font-weight: bold; height: 3em; overflow: hidden;'>"
                                f"{manga['title']}"
                                f"</p>", 
                                unsafe_allow_html=True
                            )
                            if st.button("Pilih Manga Ini", key=manga['slug'], use_container_width=True):
                                st.session_state.selected_manga = manga
                                st.rerun() # Muat ulang aplikasi untuk pindah ke tampilan downloader
            else:
                st.warning("Tidak ada komik ditemukan.")

def display_downloader_ui():
    pass

def main():
    st.set_page_config(page_title="Duta Comic", layout="wide")
    st.title("📚 Duta Comic Reader & Downloader")

    # --- Navigasi Multi-Halaman Sederhana ---
    # Jika belum ada manga yang dipilih, tampilkan grid
    if 'selected_manga' not in st.session_state:
        st.session_state.selected_manga = None

    if st.session_state.selected_manga:
        # Jika ada manga yang dipilih, tampilkan UI downloader
        display_downloader_ui()
    else:
        # Jika tidak, tampilkan grid komik
        display_manga_grid()

if __name__ == "__main__":
    main()