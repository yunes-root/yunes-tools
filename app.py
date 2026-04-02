import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import io

# Sayfa Ayarları
st.set_page_config(page_title="Öğrenci Dostu PDF Araçları", page_icon="📄")
st.image("logo.png", width=200)
st.title("📄 PDF Birleştirici & Ayırıcı")
st.markdown("---")

# Yan Menü (Sidebar) Seçenekleri
islem = st.sidebar.selectbox("Yapmak istediğin işlemi seç:", ["PDF Birleştir", "PDF Sayfalarına Ayır"])

if islem == "PDF Birleştir":
    st.header("🤝 PDF Dosyalarını Birleştir")
    st.write("Birden fazla PDF seç, tek dosya olarak indir.")
    
    yuklenen_dosyalar = st.file_uploader("PDF'leri Seç (Sıralama yükleme sırasına göredir)", 
                                         accept_multiple_files=True, type="pdf")

    if st.button("Hepsini Birleştir"):
        if yuklenen_dosyalar:
            merger = PdfMerger()
            for pdf in yuklenen_dosyalar:
                merger.append(pdf)
            
            output = io.BytesIO()
            merger.write(output)
            st.success("Dosyalar başarıyla birleştirildi!")
            
            st.download_button(
                label="📥 Birleşmiş PDF'i İndir",
                data=output.getvalue(),
                file_name="birlesmis_dosya.pdf",
                mime="application/pdf"
            )
        else:
            st.error("Lütfen en az iki dosya yükle!")

elif islem == "PDF Sayfalarına Ayır":
    st.header("✂️ PDF Sayfalarını Ayır")
    st.write("Bir PDF dosyasının tüm sayfalarını ayrı dosyalar olarak ayırır.")
    
    tek_dosya = st.file_uploader("Ayırmak istediğin PDF'i seç", type="pdf")

    if st.button("Sayfalara Böl"):
        if tek_dosya:
            reader = PdfReader(tek_dosya)
            for i, page in enumerate(reader.pages):
                writer = PdfWriter()
                writer.add_page(page)
                
                output = io.BytesIO()
                writer.write(output)
                
                st.download_button(
                    label=f"📥 Sayfa {i+1} İndir",
                    data=output.getvalue(),
                    file_name=f"sayfa_{i+1}.pdf",
                    mime="application/pdf",
                    key=f"btn_{i}"
                )
            st.success("Tüm sayfalar hazır!")
        else:
            st.error("Lütfen bir dosya seç!")

st.markdown("---")
st.caption("Geliştirici: Yusuf Enes (yunes) ")
