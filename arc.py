"""
ARC: Adaptive Resource Controller
"""

import time
import subprocess
import notify2

BAT = "/sys/class/power_supply/BAT0/capacity"
STATUS = "/sys/class/power_supply/BAT0/status"


def read(path):
    try:
        with open(path) as f:
            return f.read().strip()
    except:
        return None


def notify(title, msg, icon):
    try:
        n = notify2.Notification(title, msg, icon)
        n.show()
    except Exception as e:
        print("Notify error:", e)

    subprocess.run([
        "paplay",
        "/usr/share/sounds/freedesktop/stereo/window-question.oga"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    notify2.init("ARC")

    last_status = read(STATUS)
    high_sent = False
    low_sent = False

    while True:
        level_raw = read(BAT)
        status = read(STATUS)

        if level_raw is None or status is None:
            time.sleep(30)
            continue

        try:
            level = int(level_raw)
        except:
            time.sleep(30)
            continue

        # batería alta
        if level >= 80 and not high_sent:
            notify(
                "Batería alta",
                f"{level}% - Desconecta el cargador",
                "battery-full"
            )
            high_sent = True
            low_sent = False

        # batería baja
        elif level <= 30 and not low_sent:
            notify(
                "Batería baja",
                f"{level}% - Conecta el cargador",
                "dialog-warning"
            )
            low_sent = True
            high_sent = False

        # rango normal
        elif 30 < level < 80:
            high_sent = False
            low_sent = False

        # cambio de estado
        if status != last_status:
            last_status = status

            if status == "Charging":
                notify("⚡ Cargando", f"{level}%", "dialog-information")
            elif status == "Discharging":
                notify("🔋 En batería", f"{level}%", "dialog-information")

        time.sleep(30)


if __name__ == "__main__":
    main()