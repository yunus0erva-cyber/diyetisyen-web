"""
Florya MEV Koleji - Port Temizleme ve Başlatma Yardımcısı
Port 8501'i meşgul eden eski veya donmuş işlemleri temizler.
"""
import os
import subprocess

def clear_port_8501():
    try:
        output = subprocess.check_output("netstat -ano", shell=True, text=True)
        my_pid = str(os.getpid())
        for line in output.splitlines():
            if ":8501" in line:
                parts = line.strip().split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    if pid.isdigit() and pid != my_pid and pid != "0":
                        subprocess.run(f"taskkill /F /PID {pid}", shell=True, capture_output=True)
    except Exception:
        pass

if __name__ == "__main__":
    clear_port_8501()
    print("Port kontrolü tamamlandı.")
