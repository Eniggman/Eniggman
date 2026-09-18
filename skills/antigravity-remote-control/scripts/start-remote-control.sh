#!/usr/bin/env bash
# ==============================================================================
# Antigravity Remote Control Launcher for Termux & Linux
# ==============================================================================
# Автоматический запуск Antigravity CLI (v1.2.6+) с перехватом сессии Remote Control,
# извлечением Session ID и открытием веб-интерфейса через termux-open-url / xdg-open.
# ==============================================================================

set -eo pipefail

GEMINI_DIR="${HOME}/.gemini/antigravity-cli"
LOG_DIR="${GEMINI_DIR}/log"
CLI_LOG="${GEMINI_DIR}/cli.log"
TIMEOUT=35

# Проверка режима установки в Termux:Widget
if [ "$1" = "--install-widget" ]; then
    SHORTCUTS_DIR="${HOME}/.shortcuts"
    mkdir -p "${SHORTCUTS_DIR}"
    SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/$(basename "${BASH_SOURCE[0]}")"
    TARGET_WIDGET="${SHORTCUTS_DIR}/Antigravity-Remote.sh"
    
    cat > "${TARGET_WIDGET}" <<EOF
#!/usr/bin/env bash
# Termux:Widget launcher for Antigravity Remote Control
bash "${SCRIPT_PATH}"
EOF
    chmod +x "${TARGET_WIDGET}"
    echo "✅ Виджет успешно установлен в: ${TARGET_WIDGET}"
    echo "📱 Добавьте виджет 'Termux:Widget' на рабочий стол Android и выберите 'Antigravity-Remote.sh'."
    exit 0
fi

# Проверка наличия agy
if ! command -v agy >/dev/null 2>&1; then
    echo "❌ Ошибка: исполняемый файл 'agy' не найден в PATH." >&2
    echo "Убедитесь, что Antigravity CLI установлен и настроен." >&2
    exit 1
fi

mkdir -p "${LOG_DIR}"

# Функция открытия URL на Android / Linux
open_remote_url() {
    local target_url="$1"
    
    # 1. Android Termux
    if command -v termux-open-url >/dev/null 2>&1; then
        termux-open-url "${target_url}"
        return 0
    fi
    
    # 2. Linux xdg-open
    if command -v xdg-open >/dev/null 2>&1; then
        xdg-open "${target_url}" >/dev/null 2>&1 &
        return 0
    fi

    # 3. Termux API буфер обмена
    if command -v termux-clipboard-set >/dev/null 2>&1; then
        termux-clipboard-set "${target_url}"
    fi

    return 1
}

# Функция всплывающего уведомления в Android (если есть Termux:API)
send_android_notify() {
    local session_id="$1"
    local session_url="$2"

    if command -v termux-notification >/dev/null 2>&1; then
        termux-notification \
            --id 9921 \
            --title "🛰️ Antigravity Remote Control" \
            --content "Сессия активна: ${session_id:0:8}..." \
            --action "termux-open-url ${session_url}" \
            --priority high \
            --vibrate 200,100,200 \
            >/dev/null 2>&1 || true
    fi

    if command -v termux-toast >/dev/null 2>&1; then
        termux-toast -b green -c white "Antigravity Remote Control: открываем сессию..." >/dev/null 2>&1 || true
    fi
}

echo "=========================================================="
echo "  🛰️  Antigravity Remote Control Launcher v1.2.6+       "
echo "=========================================================="
echo "  Каталог : $(pwd)"
echo "  Команда : agy --remote-control $*"
echo "----------------------------------------------------------"

START_TIME=$(date +%s)

# Запуск фонового наблюдателя за логами
(
    elapsed=0
    found=0

    while [ "$elapsed" -lt "$TIMEOUT" ]; do
        sleep 1
        elapsed=$((elapsed + 1))

        # Находим самый свежий файл лога
        latest_log=$(ls -t "${LOG_DIR}"/cli-*.log 2>/dev/null | head -n 1 || true)
        
        session_id=""

        # Проверяем последний файл лога сессии
        if [ -n "$latest_log" ] && [ -r "$latest_log" ]; then
            # Ищем ID сессии
            session_id=$(grep -oE '\[remote-control-[0-9a-fA-F-]+-v2\]' "$latest_log" 2>/dev/null | tail -n 1 | sed -e 's/\[remote-control-//' -e 's/-v2\]//' || true)
        fi

        # Если не найден в файле сессии, проверяем cli.log
        if [ -z "$session_id" ] && [ -r "${CLI_LOG}" ]; then
            session_id=$(grep -oE '\[remote-control-[0-9a-fA-F-]+-v2\]' "${CLI_LOG}" 2>/dev/null | tail -n 1 | sed -e 's/\[remote-control-//' -e 's/-v2\]//' || true)
        fi

        if [ -n "$session_id" ]; then
            session_url="https://antigravity.google.com/r/${session_id}"
            
            echo ""
            echo "=========================================================="
            echo "  ✅ СЕССИЯ REMOTE CONTROL ПОДКЛЮЧЕНА!"
            echo "=========================================================="
            echo "  Session ID : ${session_id}"
            echo "  Web UI URL : ${session_url}"
            echo "----------------------------------------------------------"

            # Копирование в буфер Termux
            if command -v termux-clipboard-set >/dev/null 2>&1; then
                echo "${session_url}" | termux-clipboard-set
                echo "  📋 Ссылка скопирована в буфер обмена Android."
            fi

            # Уведомление в шторку Android
            send_android_notify "${session_id}" "${session_url}"

            # Открытие в браузере
            if open_remote_url "${session_url}"; then
                echo "  🌐 Веб-интерфейс открыт в браузере."
            else
                echo "  ⚠️ Не удалось автоматически открыть браузер. Скопируйте ссылку вручную."
            fi
            echo "=========================================================="
            echo ""
            found=1
            break
        fi
    done

    if [ "$found" -eq 0 ]; then
        echo "⚠️ Таймаут ожидания Remote Control session-id (${TIMEOUT}s)." >&2
    fi
) &

WATCHER_PID=$!

# Запуск основной сессии Antigravity CLI в текущем терминале
exec agy --remote-control "$@"
