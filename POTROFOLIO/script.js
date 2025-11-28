// ===============================
// 1. TOMBOL MODE GELAP (DARK/LIGHT MODE)
// ===============================

// Ambil tombol mode gelap dari HTML
const themeBtn = document.getElementById("themeBtn");

// Event ketika tombol di-klik
themeBtn.addEventListener("click", function () {
    console.log("Tombol Mode Gelap diklik");  // Console logger

    // Toggle kelas dark-mode pada body
    document.body.classList.toggle("dark-mode");

    // Ubah teks tombol
    if (document.body.classList.contains("dark-mode")) {
        themeBtn.textContent = "Mode Terang";
    } else {
        themeBtn.textContent = "Mode Gelap";
    }
});


// ===============================
// 2. TOMBOL SAPA PENGUNJUNG
// ===============================

// Ambil tombol dan elemen paragraf sapaan
const greetBtn = document.getElementById("greetBtn");
const greeting = document.getElementById("greeting");

// Event klik tombol sapaan
greetBtn.addEventListener("click", function () {
    console.log("Tombol Sapaan diklik");  // Console logger

    // Minta nama lewat prompt
    const nama = prompt("Siapa nama Anda?");

    // Jika user mengisi nama → tampilkan ke dalam paragraf
    if (nama) {
        greeting.innerText = "Halo, " + nama + "!";
    } else {
        greeting.innerText = "Hai sayang.";
    }
});


// ===============================
// 3. UBAH WARNA PARAGRAF MENJADI HITAM SAAT MODE GELAP
// ===============================

document.addEventListener("DOMContentLoaded", function () {
    // Memastikan DOM terbaca
    console.log("Halaman selesai dimuat");
});

// ===============================
// 4. REFLEKSI (Syarat Tugas) – Ditulis Dalam Komentar
// ===============================

/*
REFLEKSI SINGKAT:
Bagian tersulit adalah memahami bagaimana cara menghubungkan HTML dan JavaScript,
karena kalau posisi <script> salah, tombol tidak merespons sama sekali.

Momen “WOW” terjadi saat fitur Dark Mode akhirnya berhasil,
dan ketika prompt bisa menampilkan nama pengunjung ke halaman web.
Saya merasa lebih percaya diri karena sekarang saya bisa membuat halaman HTML menjadi interaktif,
bukan hanya tampilan statis.
*/
