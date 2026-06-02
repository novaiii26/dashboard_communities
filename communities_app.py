# PERTANYAAN BISNIS 
# 1. Bagaimana karakteristik distribusi komunitas di setiap platform media (Discord vs Facebook)?
# 2. Kategori topik spesifik apa yang paling mendominasi pasar digital saat ini?
# 3. Bagaimana karakteristik pengelola komunitas dalam menyajikan informasi profil (Panjang Deskripsi)?
# 4. Kata kunci (Keywords) apa yang paling sering digunakan pada penamaan komunitas?

"""
====================================================================
DASHBOARD INTERAKTIF: ANALISIS EKSPLANATORI EKOSISTEM KOMUNITAS DIGITAL
====================================================================
Deskripsi : Aplikasi Business Intelligence berbasis web untuk 
            menjawab 4 pertanyaan bisnis ekosistem komunitas.
Library   : streamlit, pandas, plotly
Eksekusi  : streamlit run app.py
====================================================================
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import os
import re
from collections import Counter

# 1. Konfigurasi Utama Dashboard
st.set_page_config(
    page_title="Dashboard Analisis Komunitas Digital",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Fungsi Memuat & Membersihkan Data (Robust Caching)
@st.cache_data
def load_and_clean_data():
    file_path = 'merged_communities.csv'
    
    if os.path.exists(file_path):
        data = pd.read_csv(file_path)
        
        # Standardisasi data teks untuk menghindari duplikasi kapitalisasi
        data['platform'] = data['platform'].fillna('Unknown').str.title()
        data['category'] = data['category'].fillna('Other').str.title()
        data['community_name'] = data['community_name'].fillna('Unnamed Community')
        data['description'] = data['description'].fillna('')
        
        # Rekayasa Fitur (Feature Engineering): Analisis Panjang Teks Deskripsi
        data['desc_length'] = data['description'].apply(len)
        data['desc_word_count'] = data['description'].apply(lambda x: len(x.split()))
        
        return data
    return None

df = load_and_clean_data()

# Validasi Eksistensi Dataset
if df is None:
    st.error("❌ Berkas 'merged_communities.csv' tidak ditemukan. Pastikan file berada di folder yang sama dengan app.py.")
else:
    # 3. Pengaturan Panel Kontrol Filter (Sidebar)
    st.sidebar.header("⚙️ Panel Kontrol Filter")
    st.sidebar.markdown("Filter data secara dinamis untuk melihat insight spesifik.")
    
    # Filter Platform
    list_platform = ["Semua Platform"] + sorted(list(df['platform'].unique()))
    selected_platform = st.sidebar.selectbox("Pilih Platform:", list_platform)
    
    # Filter Kategori
    list_category = ["Semua Kategori"] + sorted(list(df['category'].unique()))
    selected_category = st.sidebar.selectbox("Pilih Kategori Topik:", list_category)
    
    # Logika Penyaringan Data
    filtered_df = df.copy()
    if selected_platform != "Semua Platform":
        filtered_df = filtered_df[filtered_df['platform'] == selected_platform]
    if selected_category != "Semua Kategori":
        filtered_df = filtered_df[filtered_df['category'] == selected_category]

    # 4. Bagian Judul Dashboard
    st.title("🌐 Dashboard Analisis Eksplanatori Jaringan Komunitas Digital")
    st.markdown("""
    Dashboard ini dirancang khusus untuk membedah karakteristik ekosistem komunitas berdasarkan data platform, 
    topik kategori, deskripsi tertulis, serta pola penamaan grup.
    """)
    st.write("---")

    # 5. Ringkasan Metrik Utama (KPI)
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    with col_kpi1:
        st.metric(label="Total Komunitas Teranalisis", value=f"{filtered_df.shape[0]} Grup")
    with col_kpi2:
        total_kategori = filtered_df['category'].nunique()
        st.metric(label="Kategori Topik Unik", value=f"{total_kategori} Topik")
    with col_kpi3:
        rata_rata_deskripsi = filtered_df['desc_length'].mean()
        st.metric(label="Rata-rata Panjang Deskripsi", value=f"{int(rata_rata_deskripsi)} Karakter")
    
    st.write("---")

    # ==========================================
    # VISUALISASI PERTANYAAN 1
    # ==========================================
    st.header("🏢 1. Lanskap Kompetisi & Dominasi Ekosistem Platform")
    st.markdown("""
    **Analisis Eksplanatori:** Grafik di bawah menunjukkan perbandingan kekuatan volume antar platform. 
    Ini menjawab platform mana yang paling populer dan paling banyak dipilih oleh pengelola komunitas saat ini.
    """)
    
    c1, c2 = st.columns([3, 2])
    with c1:
        fig_q1_bar = px.histogram(
            filtered_df,
            x="platform",
            color="platform",
            title="Kuantitas Komunitas per Platform",
            labels={'platform': 'Platform Media', 'count': 'Jumlah Komunitas'},
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        st.plotly_chart(fig_q1_bar, use_container_width=True)
    with c2:
        proporsi_platform = filtered_df['platform'].value_counts().reset_index()
        fig_q1_pie = px.pie(
            proporsi_platform,
            values='count',
            names='platform',
            title="Proporsi Pangsa Pasar Platform",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_q1_pie, use_container_width=True)
        
    st.write("---")

    # ==========================================
    # VISUALISASI PERTANYAAN 2
    # ==========================================
    st.header("🚀 2. Tren Kategori Terpopuler (Fokus Konten)")
    st.markdown("""
    **Analisis Eksplanatori:** Grafik ini memetakan klaster topik atau **Kategori** berdasarkan jumlah komunitas yang terbentuk. 
    Hal ini membantu bisnis mengidentifikasi ceruk pasar (*niche*) mana yang paling diminati dan paling padat kompetisinya.
    """)
    
    category_data = filtered_df['category'].value_counts().reset_index().head(10)
    
    fig_q2_cat = px.bar(
        category_data,
        x='count',
        y='category',
        orientation='h',
        title="Top 10 Kategori Komunitas Terbanyak",
        labels={'count': 'Total Komunitas', 'category': 'Kategori Topik'},
        color='count',
        color_continuous_scale=px.colors.sequential.Viridis
    )
    fig_q2_cat.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_q2_cat, use_container_width=True)
    
    st.write("---")

    # ==========================================
    # VISUALISASI PERTANYAAN 3
    # ==========================================
    st.header("🎯 3. Kelengkapan Informasi & Gaya Profil Komunitas")
    st.markdown("""
    **Analisis Eksplanatori:** Hubungan antara jumlah kata dan panjang karakter deskripsi mencerminkan pola komunikasi pengelola. 
    Titik sebaran data membuktikan apakah komunitas di platform tertentu cenderung menyajikan informasi detail (panjang) atau sekadar ringkasan pendek.
    """)
    
    fig_q3_scatter = px.scatter(
        filtered_df,
        x="desc_length",
        y="desc_word_count",
        color="platform",
        hover_data=["community_name", "category"],
        title="Matriks Hubungan Panjang Karakter vs Jumlah Kata Deskripsi",
        labels={'desc_length': 'Panjang Karakter Deskripsi', 'desc_word_count': 'Jumlah Kata Deskripsi'},
        color_discrete_sequence=px.colors.qualitative.Dark2
    )
    st.plotly_chart(fig_q3_scatter, use_container_width=True)
    
    st.write("---")

    # ==========================================
    # VISUALISASI PERTANYAAN 4
    # ==========================================
    st.header("📦 4. Tren Kata Kunci (Keywords) Terbanyak pada Nama Komunitas")
    st.markdown("""
    **Analisis Eksplanatori:** Analisis penamaan (*naming convention*) mengekstrak kata-kata yang paling sering digunakan pada nama komunitas. 
    Ini berguna untuk strategi optimasi pencarian kata kunci (SEO) agar komunitas baru lebih mudah ditemukan audiens.
    """)
    
    # Logika NLP Sederhana untuk Ekstraksi Kata Kunci
    all_names = " ".join(filtered_df['community_name'].dropna().astype(str)).lower()
    words = re.findall(r'\b\w{4,}\b', all_names)
    # Menyaring stopword (kata umum) bahasa Indonesia & Inggris
    stopwords = {'community', 'grup', 'facebook', 'indonesia', 'server', 'official', 'sharing', 'group', 'tempat', 'video', 'editing'}
    filtered_words = [w for w in words if w not in stopwords]
    
    word_counts = Counter(filtered_words).most_common(10)
    words_df = pd.DataFrame(word_counts, columns=['Kata', 'Frekuensi'])
    
    c3, c4 = st.columns([3, 2])
    with c3:
        if not words_df.empty:
            fig_q4_bar = px.bar(
                words_df,
                x='Frekuensi',
                y='Kata',
                orientation='h',
                title="10 Kata Kunci Terbanyak pada Nama Komunitas",
                labels={'Frekuensi': 'Frekuensi Kemunculan', 'Kata': 'Kata Kunci'},
                color='Frekuensi',
                color_continuous_scale=px.colors.sequential.Plasma
            )
            fig_q4_bar.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_q4_bar, use_container_width=True)
        else:
            st.warning("Data kata kunci tidak cukup untuk ditampilkan.")
    with c4:
        if not words_df.empty:
            fig_q4_pie = px.pie(
                words_df,
                values='Frekuensi',
                names='Kata',
                title="Proporsi Distribusi Kata Kunci",
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            st.plotly_chart(fig_q4_pie, use_container_width=True)
        else:
            st.write("Tidak ada data proporsi.")

    st.write("---")

    # ==========================================
    # KESIMPULAN STRATEGIS BERDASARKAN DATA
    # ==========================================
    st.header("📌 Kesimpulan & Rekomendasi Bisnis")
    
    top_platform_name = proporsi_platform.iloc[0]['platform'] if not proporsi_platform.empty else "Platform Utama"
    top_category_name = category_data.iloc[0]['category'] if not category_data.empty else "Kategori Utama"
    top_keyword_name = words_df.iloc[0]['Kata'].upper() if not words_df.empty else "KEYWORD"
    
    st.markdown(f"""
    Berdasarkan pengolahan data eksploratif pada berkas komunitas, berikut adalah rekomendasi strategis:
    
    1. **Fokus Alokasi Platform:** Platform **{top_platform_name}** memimpin volume pembuatan komunitas di dalam dataset ini. Jika Anda berencana merilis produk baru atau kampanye komunitas skala besar, disarankan memprioritaskan platform tersebut karena ekosistemnya sudah matang.
    2. **Pemetaan Kompetisi Ceruk Pasar:** Kategori **{top_category_name}** merupakan area dengan tingkat persaingan paling jenuh (*high supply*). Masuk ke kategori ini menuntut keunikan ekstra, sementara kategori dengan volume kecil bisa menjadi peluang pasar baru (*blue ocean*).
    3. **Optimalisasi Pengenalan Profil:** Berdasarkan grafik sebaran, profil komunitas yang menyajikan deskripsi lengkap dan informatif cenderung memberikan impresi awal yang lebih profesional. Pastikan deskripsi grup baru Anda merangkum aturan, manfaat, dan tautan eksternal secara jelas.
    4. **Strategi Penamaan SEO:** Integrasi kata kunci populer seperti **{top_keyword_name}** terbukti mendominasi pola penamaan grup. Terapkan kata kunci yang relevan dan sering dicari ke dalam judul komunitas Anda agar meningkatkan visibilitas pencarian organik di platform terkait.
    """)

    st.write("---")
    # ==========================================
    # PENJELAJAH DATA TABEL MENTAH
    # ==========================================
    st.subheader("🔍 Penjelajah Data Terfilter")
    st.dataframe(filtered_df[['platform', 'category', 'community_name', 'description', 'url']], use_container_width=True)