# CuotaPro-DataCollector 🧠⚽
Sistema de recolección automática de información deportiva (versión Termux/Linux).

## 🚀 Instalación rápida en Termux
```bash
pkg update -y && pkg install -y python git
git clone https://github.com/<TU_USUARIO>/CuotaPro-DataCollector.git
cd CuotaPro-DataCollector
pip install -r requirements.txt
python helpers/create_master_if_missing.py
python main.py
```

## ⚙️ Funcionalidad
- Extrae automáticamente fixtures, horarios y equipos desde múltiples páginas deportivas.
- Soporta reintentos automáticos (5 intentos con backoff exponencial).
- Recorre las URLs en orden y omite solo tras agotar todos los métodos.
- Genera archivo maestro: `storage/cuotapro_historial_master.csv`
- Guarda logs en `logs/scraper.log`.

## 🌐 Fuentes integradas (primarias y secundarias)
- ESPN, OneFootball, El Universo, La Pelotona, etc.
- SportyTrader, Oddspedia, BetMines, Scores24, APWin, etc.

## 🧩 Archivos principales
- `main.py` → ejecutor automático.
- `scraper/` → librerías internas.
- `helpers/create_master_if_missing.py` → crea base CSV inicial.
- `urls_list.txt` → todas las fuentes cargadas.
- `config.yml` → parámetros ajustables.

## 📆 Automatización
Ejemplo cron (cada 30 min):
```bash
*/30 * * * * cd /data/data/com.termux/files/home/CuotaPro-DataCollector && python main.py >> logs/cron.log 2>&1
```

---
© 2025 CuotaPro Systems – versión requests-only optimizada para Termux.
