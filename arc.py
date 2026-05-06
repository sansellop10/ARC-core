"""

ARC: Adaptive Resource Controller


"""


import time
import subprocess
import notify2

BAT = "/sys/class/power_supply/BAT0/capacity"
STATUS = "/sys/class/power_supply/BAT0/status"

last_status = None
high_sent = False
low_sent = False

notify2.init("ARC")

def read(path):
    try:
        with open(path) as f:
            return f.read().strip()
    except:
        return None

def notify(title, msg, type):
    n = notify2.Notification(
        title,
        msg,
        type
    )
    n.show()
    subprocess.run(["paplay", "/usr/share/sounds/freedesktop/stereo/window-question.oga"])

while True:
    level = int(read(BAT))
    status = read(STATUS)

    # avisos por porcentaje
    if level >= 80 and not high_sent:
        notify("Batería alta", f"Bateria: {level}% - Desconecta el cargador", "battery-full")
        high_sent = True
        low_sent = False

    elif level <= 30 and not low_sent:
        notify("Batería baja", f"Bateria: {level}% - Conecta el cargador", "dialog-warning")
        low_sent = True
        high_sent = False

    elif 30 < level < 80:
        high_sent = False
        low_sent = False

    # cambios de estado (Charging / Discharging)
    if status != last_status:
        last_status = status

        if status == "Charging":
            notify("⚡ Cargando", f"Bateria: {level}%", "dialog-information")
        elif status == "Discharging":
            notify("🔋 Desconectado", f"Bateria: {level}%", "dialog-information")

    time.sleep(30)
