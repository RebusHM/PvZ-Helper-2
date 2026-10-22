#!/usr/bin/env bash
set -e

echo "=========================================================="
echo "🌸 Установка PvZ Helper Bot как системной службы systemd 🍀"
echo "=========================================================="

BOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_NAME="pvzbot.service"
TARGET_SERVICE="/etc/systemd/system/${SERVICE_NAME}"

# Определяем путь к Python (с приоритетом virtualenv)
PYTHON_BIN="$(which python3)"
if [ -f "${BOT_DIR}/venv/bin/python" ]; then
    PYTHON_BIN="${BOT_DIR}/venv/bin/python"
elif [ -f "${BOT_DIR}/.venv/bin/python" ]; then
    PYTHON_BIN="${BOT_DIR}/.venv/bin/python"
fi

sed -i "s|WorkingDirectory=.*|WorkingDirectory=${BOT_DIR}|g" "${BOT_DIR}/pvzbot.service"
sed -i "s|ExecStart=.*|ExecStart=${PYTHON_BIN} ${BOT_DIR}/main.py|g" "${BOT_DIR}/pvzbot.service"

echo "Копирование службы в ${TARGET_SERVICE}..."
cp "${BOT_DIR}/pvzbot.service" "${TARGET_SERVICE}"

echo "Перезагрузка демона systemd..."
systemctl daemon-reload

echo "Включение автозагрузки и запуск службы..."
systemctl enable "${SERVICE_NAME}"
systemctl restart "${SERVICE_NAME}"

echo ""
echo "✅ Служба успешно установлена и запущена!"
echo "Статус: systemctl status ${SERVICE_NAME}"
echo "Логи:   journalctl -u ${SERVICE_NAME} -f"
