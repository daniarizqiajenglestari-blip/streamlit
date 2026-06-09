import streamlit as st

# ==================================================
# KELAS NODE KATEGORI 
# ==================================================

class KategoriNode:
    def __init__(self, nama_kategori):
        self.nama = nama_kategori
        self.sub_kategori = []

    def tambah_sub(self, node_kategori):
        self.sub_kategori.append(node_kategori)

    # Mengubah fungsi print menjadi return string agar bisa ditampilkan di web

    def dapatkan_tree_string(self, level=0):
        indentasi = "  " * level
        simbol = " " if level > 0 else " + "
        hasil = f"{indentasi}{simbol}{self.nama}\n"

        for sub in self.sub_kategori:
            hasil += sub.dapatkan_tree_string(level + 1)
        return hasil
    
    def cari_node(self, target_nama):
        # Mencari node spesifik untuk menambahkan anak di bawahnya
        if self.nama.lower() == target_nama.lower():
            return self
            
        for sub in self.sub_kategori:
            hasil = sub.cari_node(target_nama)
            if hasil:
                return hasil
                
        return None

    def cari_jalur(self, target, path=""):
        # Mencari jalur lengkap (breadcrumb) seperti studi kasus sebelumnya
        jalur_saat_ini = path + " > " + self.nama if path else self.nama
        
        if self.nama.lower() == target.lower():
            return jalur_saat_ini
            
        for sub in self.sub_kategori:
            hasil = sub.cari_jalur(target, jalur_saat_ini)
            if hasil:
                return hasil
                
        return None

# ==========================================
# PROGRAM UTAMA (STREAMLIT UI)
# ==========================================
st.set_page_config(page_title="Struktur Kategori", page_icon=" + ")

st.title("Pembuat Struktur Kategori")
st.write("Aplikasi interaktif untuk mensimulasikan struktur data Tree.")

# Inisialisasi session state untuk menyimpan struktur Tree agar tidak hilang saat halaman di-refresh #
if 'root' not in st.session_state:
    st.session_state.root = None

# Jika Root belum dibuat, tampilkan form pembuatan Root 
if st.session_state.root is None:
    st.info("Sistem belum memiliki kategori utama.Silahkan buat terlebih dahulu.")
    nama_root = st.text_input("Masukkan nama kategori uatama (Root):", value="Toko Saya")

    if st.button("Buat kategori utama", type="primary"):
        st.session_state.root = KategoriNode(nama_root)
        st.rerun() # Refresh Halaman

# Jika Root sudah ada, tampikkan Menu Utama menggunakan Tabs
else:
    root = st.session_state.root

    # Mengganti menu CLI dengan sistem Tab yang lebih modern 
    tab1, tab2, tab3 = st.tabs([" Lihat Struktur", " Tambah sub-Kategori", "Cari Jalur"])

    # TAB 1: Lihat struktur
    with tab1 :
        st.subheader("Struktur kategori saat ini")
        tree_teks = root.dapatkan_tree_string()
        # Menggunakan st.code agar format indentasi (spasi) tetap rapi
        st.code(tree_teks, language="text")

    # Tab 2: Tambah Sub-kategori
    with tab2 :
        st.subheader("Tambah Cabang Baru")
        induk_nama = st.text_input("Nama kategori induk tempat cabang ditambahkan:")
        anak_nama = st.text_input("Nama sub-kategori baru:")

        if st.button("Tambah kategori"):
            if induk_nama and anak_nama:
                induk_node = root.cari_node(induk_nama)
                if induk_node:
                    induk_node.tambah_sub(KategoriNode(anak_nama))
                    st.success(f"Berhasil menambahkan '{anak_nama}' dibawah '{induk_node.nama}'!")
                else:
                    st.error(f"Kategori '{induk_nama}' tidak ditemukan! pastikan ejaanya benar.")
            else:
                st.warning("Harap isi kedua kolom di atas.")

    # Tab 3: Cari Jalur
    with tab3:
        st.subheader("Pencarian Breadcrumb")
        target_cari = st.text_input("Nama kategori yang ingin dicari jalurnya:")

        if st.button("Cari Jalur"):
            if target_cari:
                hasil = root.cari_jalur(target_cari)
                if hasil:
                    st.success("Ditemukam!")
                    st.info(f"Jalur: {hasil}")
                else:
                    st.error(f"Kategori '{target_cari}' tidak ditemukan dalam sistem.")

            else:
                st.warning("Harap isi nama kategori yang dicari.")
# Tombol Reset
st.divider()
if st.button("Reset Sistem / Mulai dari Awal"):
    st.session_state.root = None
    st.rerun()


                