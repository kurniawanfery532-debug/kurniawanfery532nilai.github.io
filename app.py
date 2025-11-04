from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# --- Fungsi Kalkulasi Nilai (Diambil dari program sebelumnya) ---
def kalkulasi_rata_rata(data_nilai):
    """Menghitung total nilai, rata-rata, dan menentukan predikat."""
    total_nilai = sum(data_nilai.values())
    jumlah_matkul = len(data_nilai)
    
    rata_rata = total_nilai / jumlah_matkul if jumlah_matkul > 0 else 0
    
    # Penentuan Predikat Kualitatif
    if rata_rata >= 85:
        predikat = "CUM LAUDE (Sangat Memuaskan) 🎉"
    elif rata_rata >= 75:
        predikat = "Sangat Baik 👍"
    elif rata_rata >= 60:
        predikat = "Cukup Baik 👌"
    else:
        predikat = "Perlu Peningkatan Belajar 📚"
        
    return {
        'total_nilai': total_nilai,
        'jumlah_matkul': jumlah_matkul,
        'rata_rata': rata_rata,
        'predikat': predikat,
        'nilai_matkul': data_nilai # Mengembalikan nilai_matkul untuk ditampilkan
    }

# --- Rute Halaman Input (index.html) ---
@app.route('/')
def index():
    # Menampilkan halaman form input
    return render_template('index.html')

# --- Rute untuk Memproses Form (POST) ---
@app.route('/hitung', methods=['POST'])
def hitung():
    # Mengambil data dari form HTML
    nama_mahasiswa = request.form.get('nama_mahasiswa')
    
    # Ambil nilai mata kuliah. Asumsi kita punya 4 mata kuliah tetap untuk contoh.
    data_nilai = {}
    
    # Ambil data input dan validasi
    matkul_list = [
        "Algoritma dan Pemrograman", 
        "Sistem Operasi", 
        "Basis Data", 
        "Pengantar TI"
    ]
    
    for matkul in matkul_list:
        try:
            # Mengambil nilai dari field form dengan nama yang sesuai (contoh: nilai_Basis Data)
            nilai = float(request.form.get(f'nilai_{matkul.replace(" ", "_")}'))
            if 0 <= nilai <= 100:
                data_nilai[matkul] = nilai
            else:
                # Jika nilai tidak valid, berikan pesan error
                return f"Nilai '{matkul}' harus antara 0 dan 100.", 400
        except ValueError:
            return f"Input nilai untuk '{matkul}' harus berupa angka.", 400
        except TypeError:
             # Menangani jika field input kosong
             return f"Input nilai untuk '{matkul}' tidak boleh kosong.", 400

    # Kalkulasi hasil
    hasil_kalkulasi = kalkulasi_rata_rata(data_nilai)
    
    # Render halaman hasil dengan data yang sudah dihitung
    return render_template(
        'hasil.html',
        nama=nama_mahasiswa, 
        hasil=hasil_kalkulasi
    )

if __name__ == '__main__':
    # Pastikan server berjalan di debug mode (matikan untuk produksi)
    app.run(debug=True)