# ARC – Adaptive Resource Controller


## Descripción

ARC es un pequeño sistema en Python que monitoriza el estado de la batería del ordenador en segundo plano.

Su función principal es avisar al usuario mediante notificaciones y sonidos cuando:

-  La batería está alta (≥ 80%)
-  La batería está baja (≤ 30%)
-  Cambia el estado de carga (cargando / descargando)

Es un sistema ligero que se ejecuta continuamente como proceso en segundo plano, pensado como un asistente básico de energía del sistema.


## Requisitos

Antes de instalar ARC, asegúrate de tener:

- Python 3 instalado
- Sistema Linux con entorno gráfico
- `notify-send` instalado


## Instalar dependencias:

```bash id="dep1"
sudo apt update
sudo apt install libnotify-bin
sudo apt install pulseaudio-utils
```


##  Configuración de systemd


- Creación del directorio y del .service

```bash id="dep1"
mkdir -p ~/.config/systemd/user
nano ~/.config/systemd/user/arc.service
```

- Contenido del .service

```bash id="dep1"
[Unit]
Description=ARC - Adaptive Resource Controller
After=graphical-session.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/usuario/ruta/arc.py
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
```

- Configuración

```bash id="dep1"
systemctl --user daemon-reload
systemctl --user enable arc.service
systemctl --user start arc.service
```

- Comprovación

```bash id="dep1"
systemctl --user status arc.service
pgrep -af arc
```
## Actualizar ARC

- Parar el servicio
```bash id="dep1"
systemctl --user stop arc.service
```
- (Opcional) recargar systemd si cambiaste el .service
```bash id="dep1"
systemctl --user daemon-reload
```
- Volver a iniciar
```bash id="dep1"
systemctl --user start arc.service
```
- Verificar
```bash id="dep1"
systemctl --user status arc.service
```

## Detener o desinstalar ARC

- Detener servicio:

```bash id="dep1"
systemctl --user stop arc.service
```
- Desactivar inicio automático:

```bash id="dep1"
systemctl --user disable arc.service
```

- Eliminar completamente:

```bash id="dep1"
rm ~/.config/systemd/user/arc.service
systemctl --user daemon-reload
```

---

![ARC Banner](img/arc-banner.jpeg)