# modules/ui.py

def display_main_menu() -> str:
    """Menampilkan menu utama dan mengembalikan pilihan pengguna."""
    print("\n" + "="*40)
    print("      AUTOMATION BOT - MAIN MENU")
    print("="*40)
    print("1. Auto Signup (Membuat 1 akun baru)")
    print("2. Auto Login (Login dengan 1 akun)")
    print("3. Proses Aktivitas (Perlu Login)")
    print("4. Auto Logout")
    print("5. Clear Session Data (Cache/Cookies)")
    print("0. Exit")
    print("-"*40)
    
    choice = input(">>> Masukkan pilihan Anda: ")
    return choice.strip()

def display_activity_submenu() -> str:
    """Menampilkan sub-menu aktivitas dan mengembalikan pilihan pengguna."""
    print("\n" + "-"*40)
    print("        SUB-MENU PROSES AKTIVITAS")
    print("-"*40)
    print("1. Create Repository")
    print("2. Fork & Run Actions (Belum tersedia)")
    print("3. Contribution (Belum tersedia)")
    print("4. Jalankan 1 Random Task (Dipandu AI)")
    print("9. Kembali ke Menu Utama")
    print("-"*40)

    choice = input(">>> Masukkan pilihan aktivitas: ")
    return choice.strip()

def ask_headless_mode() -> bool:
    """Menanyakan kepada pengguna apakah ingin menjalankan dalam mode headless."""
    while True:
        choice = input(">>> Jalankan dalam mode Headless (tanpa UI Browser)? (y/n): ").lower().strip()
        if choice == 'y':
            print(">>> Mode Headless diaktifkan. Semua proses berjalan di latar belakang.")
            return True
        elif choice == 'n':
            print(">>> Mode UI diaktifkan. Browser akan ditampilkan.")
            return False
        else:
            print(">>> Pilihan tidak valid. Harap masukkan 'y' atau 'n'.")