import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_TOKEN = "WDTHx2vqZGE38gchBe7oAewzB9ZPNpxU"
API_BASE_URL = "https://api.depsearch.sbs/quest="

# ==================== HTML-интерфейс (встроен прямо в код) ====================
HTML_PAGE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fackripper | OSINT поиск по базам данных</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background-color: #0a0a0a;
            font-family: 'Segoe UI', 'Inter', 'Roboto', monospace;
            color: #e0e0e0;
            line-height: 1.5;
            padding: 2rem 1.5rem;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        .logo {
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #ff3a3a, #b91c1c);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            margin-bottom: 0.25rem;
        }
        .tagline {
            color: #888;
            margin-bottom: 2rem;
            border-left: 2px solid #ff3a3a;
            padding-left: 1rem;
            font-size: 0.9rem;
        }
        .tabs {
            display: flex;
            gap: 0.5rem;
            border-bottom: 1px solid #2a2a2a;
            margin-bottom: 2rem;
            flex-wrap: wrap;
        }
        .tab-btn {
            background: transparent;
            border: none;
            padding: 0.75rem 1.8rem;
            font-size: 1rem;
            font-weight: 600;
            color: #aaa;
            cursor: pointer;
            border-radius: 12px 12px 0 0;
            font-family: inherit;
        }
        .tab-btn.active { color: #ff3a3a; background: #151515; border-bottom: 2px solid #ff3a3a; }
        .tab-content { display: none; animation: fade 0.2s ease; }
        .tab-content.active { display: block; }
        @keyframes fade { from { opacity: 0; transform: translateY(5px);} to { opacity: 1; transform: translateY(0);} }
        .examples-section {
            background: #0f0f0f;
            border-radius: 24px;
            padding: 1.2rem 1.5rem;
            margin-bottom: 2rem;
            border: 1px solid #222;
        }
        .examples-title {
            font-size: 0.85rem;
            text-transform: uppercase;
            color: #ff5e5e;
            margin-bottom: 1rem;
            font-weight: 600;
        }
        .examples-grid { display: flex; flex-wrap: wrap; gap: 0.7rem; }
        .example-badge {
            background: #1a1a1a;
            border: 1px solid #2c2c2c;
            color: #ffa0a0;
            padding: 0.45rem 1rem;
            border-radius: 40px;
            font-size: 0.8rem;
            font-family: monospace;
            cursor: pointer;
            transition: 0.2s;
        }
        .example-badge:hover { background: #2a1a1a; border-color: #ff5e5e; }
        .search-area {
            background: #0f0f0f;
            border-radius: 24px;
            padding: 1.5rem;
            border: 1px solid #222;
            margin-bottom: 2rem;
        }
        .search-wrapper { display: flex; flex-direction: column; gap: 1rem; }
        .search-input-group { display: flex; flex-wrap: wrap; gap: 1rem; }
        #queryInput {
            flex: 1;
            background: #050505;
            border: 1px solid #2c2c2c;
            padding: 1rem 1.2rem;
            border-radius: 60px;
            font-size: 1rem;
            color: #ffcfcf;
            font-family: monospace;
            outline: none;
        }
        #queryInput:focus { border-color: #ff3a3a; box-shadow: 0 0 0 2px rgba(255,58,58,0.2); }
        .search-btn {
            background: #c62828;
            border: none;
            padding: 0 2rem;
            border-radius: 60px;
            font-weight: bold;
            font-size: 1rem;
            color: white;
            cursor: pointer;
            font-family: inherit;
        }
        .search-btn:hover { background: #b71c1c; transform: scale(0.98); }
        .result-container {
            background: #0c0c0c;
            border-radius: 24px;
            border: 1px solid #222;
            overflow: hidden;
        }
        .result-header {
            background: #111;
            padding: 1rem 1.5rem;
            border-bottom: 1px solid #222;
            font-weight: 600;
            color: #ff5e5e;
        }
        .result-content { padding: 1.5rem; font-family: monospace; font-size: 0.85rem; max-height: 550px; overflow-y: auto; }
        .result-key { color: #b0b0b0; font-weight: 500; }
        .result-value { color: #ff5e5e; font-weight: 500; word-break: break-word; }
        .error-message { background: #1f1212; border-left: 4px solid #ff3a3a; padding: 1rem; border-radius: 12px; color: #ffb3b3; }
        .card-item { background: #111; margin-bottom: 1rem; padding: 1rem; border-radius: 16px; border-left: 3px solid #ff3a3a; }
        .owner-text { background: #111; display: inline-block; padding: 0.5rem 1rem; border-radius: 40px; margin-top: 1rem; }
        .support-text { background: #111; padding: 1.5rem; border-radius: 24px; text-align: center; }
        footer { margin-top: 3rem; text-align: center; font-size: 0.7rem; color: #3a3a3a; }
        @media (max-width: 680px) {
            body { padding: 1rem; }
            .search-btn { width: 100%; justify-content: center; }
            .search-input-group { flex-direction: column; }
        }
        .loading { display: inline-block; width: 20px; height: 20px; border: 2px solid #2a2a2a; border-top: 2px solid #ff3a3a; border-radius: 50%; animation: spin 0.6s linear infinite; margin-right: 8px; vertical-align: middle; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>
<div class="container">
    <div class="logo">FACKRIPPER<span>.COM</span></div>
    <div class="tagline">поиск по федеральным базам данных & OSINT</div>
    <div class="tabs">
        <button class="tab-btn active" data-tab="search">🔍 Поиск информации</button>
        <button class="tab-btn" data-tab="about">📄 Описание</button>
        <button class="tab-btn" data-tab="support">🛟 Поддержка</button>
    </div>

    <div id="searchTab" class="tab-content active">
        <div class="examples-section">
            <div class="examples-title">📌 ТИПЫ ЗАПРОСОВ (нажмите для вставки)</div>
            <div class="examples-grid" id="examplesGrid"></div>
        </div>
        <div class="search-area">
            <div class="search-wrapper">
                <div class="search-input-group">
                    <input type="text" id="queryInput" placeholder="Введите ФИО, телефон, email, IP, VIN, СНИЛС, адрес...">
                    <button class="search-btn" id="searchBtn">🔎 Выполнить поиск</button>
                </div>
                <div class="info-note">⚡ Все форматы: ФИО, телефон, email, nick:, pass:, snils, inn, VIN, IP, VK, tt:, addr:</div>
            </div>
        </div>
        <div id="resultArea" class="result-container" style="display: none;">
            <div class="result-header">📡 РЕЗУЛЬТАТЫ ПОИСКА (Database)</div>
            <div class="result-content" id="resultContent"></div>
        </div>
        <div id="loadingIndicator" style="display: none; text-align: center; margin: 2rem;">
            <div class="loading"></div>
            <p style="margin-top: 1rem; color: #aaa;">обработка запроса к Database API...</p>
        </div>
    </div>

    <div id="aboutTab" class="tab-content">
        <div style="background: #0f0f0f; border-radius: 24px; padding: 2rem; border: 1px solid #222;">
            <h2 style="color:#ff5e5e; margin-bottom: 1rem;">Fackripper — профессиональный инструмент</h2>
            <p>Доступ к агрегированной информации из открытых источников (Database). Поиск по ФИО, телефонам, email, IP, VIN, госномерам, аккаунтам соцсетей и другим параметрам.</p>
            <div class="owner-text">👑 Owner: @attackxanax</div>
            <p style="margin-top: 1.5rem; font-size:0.8rem;">® 2026 Fackripper</p>
        </div>
    </div>

    <div id="supportTab" class="tab-content">
        <div class="support-text">
            🧩 <strong>Возникли сложности?</strong><br><br>
            Telegram: <span style="color:#ff5e5e;">@attackxanax</span><br>
            Лимит 70 запросов/мин.
        </div>
    </div>
    <footer>Fackripper.com — поиск по надёжным источникам</footer>
</div>

<script>
    const examples = [
        { label: "ФИО + год", value: "Иванов Иван Иванович 1985" },
        { label: "Телефон", value: "+7 (927) 723-13-70" },
        { label: "Email", value: "user@gmail.com" },
        { label: "Никнейм", value: "nick:username123" },
        { label: "СНИЛС", value: "snils12345678901" },
        { label: "ИНН", value: "inn582801503237" },
        { label: "ГРЗ", value: "A123BC77" },
        { label: "VIN", value: "1HGBH41JXMN109186" },
        { label: "IP", value: "8.8.8.8" },
        { label: "VK", value: "vk.com/id123456789" },
        { label: "TikTok", value: "tt:alexrybakofficial" },
        { label: "Адрес", value: "г. Москва, ул. Тверская, д. 10" }
    ];
    function buildExamples() {
        const grid = document.getElementById('examplesGrid');
        if (!grid) return;
        examples.forEach(ex => {
            const badge = document.createElement('div');
            badge.className = 'example-badge';
            badge.textContent = ex.label;
            badge.onclick = () => document.getElementById('queryInput').value = ex.value;
            grid.appendChild(badge);
        });
    }
    function initTabs() {
        const btns = document.querySelectorAll('.tab-btn');
        const tabs = { search: document.getElementById('searchTab'), about: document.getElementById('aboutTab'), support: document.getElementById('supportTab') };
        btns.forEach(btn => {
            btn.onclick = () => {
                btns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                Object.values(tabs).forEach(t => t.classList.remove('active'));
                tabs[btn.dataset.tab].classList.add('active');
            };
        });
    }
    function escapeHtml(str) {
        if (typeof str !== 'string') return str;
        return str.replace(/[&<>]/g, function(m) {
            if (m === '&') return '&amp;';
            if (m === '<') return '&lt;';
            if (m === '>') return '&gt;';
            return m;
        });
    }
    function renderJSONToHTML(obj) {
        if (obj === null) return '<span class="result-value">null</span>';
        if (typeof obj === 'string') return `<span class="result-value">"${escapeHtml(obj)}"</span>`;
        if (typeof obj === 'number' || typeof obj === 'boolean') return `<span class="result-value">${obj}</span>`;
        if (Array.isArray(obj)) {
            if (obj.length === 0) return '<span class="result-value">[]</span>';
            let items = '';
            obj.forEach((item, idx) => {
                items += `<div style="margin-left: 20px;">${renderJSONToHTML(item)}${idx < obj.length-1 ? ',' : ''}</div>`;
            });
            return `<div>[</div>${items}<div>]</div>`;
        }
        const keys = Object.keys(obj);
        if (keys.length === 0) return '<span class="result-value">{}</span>';
        let html = '<div>{</div>';
        keys.forEach((key, idx) => {
            const val = obj[key];
            html += `<div style="margin-left: 20px;"><span class="result-key">${escapeHtml(key)}</span>: ${renderJSONToHTML(val)}${idx < keys.length-1 ? ',' : ''}</div>`;
        });
        html += '<div>}</div>';
        return html;
    }
    function formatResponse(data) {
        if (!data) return '<div class="error-message">Пустой ответ</div>';
        if (data.error) return `<div class="error-message">⚠️ ${escapeHtml(data.error)}</div>`;
        let html = '';
        if (data.phone_info) {
            html += `<div class="card-item"><span class="result-key">📞 ТЕЛЕФОН</span><br>${renderJSONToHTML(data.phone_info)}</div>`;
        }
        if (data.ip_info) {
            html += `<div class="card-item"><span class="result-key">🌐 IP</span><br>${renderJSONToHTML(data.ip_info)}</div>`;
        }
        if (data.results) {
            const resultsArray = Array.isArray(data.results) ? data.results : [data.results];
            html += `<div class="card-item"><span class="result-key">📚 НАЙДЕНО ЗАПИСЕЙ: ${resultsArray.length}</span><br>`;
            resultsArray.forEach((rec, idx) => {
                html += `<div style="border-top:1px solid #2a2a2a; margin-top:12px; padding-top:12px;"><span class="result-key">#${idx+1}</span><br>${renderJSONToHTML(rec)}</div>`;
            });
            html += `</div>`;
        }
        const otherKeys = Object.keys(data).filter(k => !['phone_info','ip_info','results'].includes(k));
        if (otherKeys.length) {
            let other = {};
            otherKeys.forEach(k => other[k] = data[k]);
            html += `<div class="card-item"><span class="result-key">🔍 ДОПОЛНИТЕЛЬНО</span><br>${renderJSONToHTML(other)}</div>`;
        }
        if (html === '') html = `<div>${renderJSONToHTML(data)}</div>`;
        return html;
    }
    async function search(query) {
        if (!query.trim()) {
            showError("Введите запрос");
            return;
        }
        const loader = document.getElementById('loadingIndicator');
        const resultContainer = document.getElementById('resultArea');
        resultContainer.style.display = 'none';
        loader.style.display = 'block';
        try {
            const response = await fetch('/api/search', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: query.trim() })
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || "Ошибка сервера");
            document.getElementById('resultContent').innerHTML = formatResponse(data);
            resultContainer.style.display = 'block';
        } catch (err) {
            showError(err.message);
        } finally {
            loader.style.display = 'none';
        }
    }
    function showError(msg) {
        const container = document.getElementById('resultArea');
        const content = document.getElementById('resultContent');
        content.innerHTML = `<div class="error-message">❌ ${escapeHtml(msg)}</div>`;
        container.style.display = 'block';
        document.getElementById('loadingIndicator').style.display = 'none';
    }
    window.onload = () => {
        buildExamples();
        initTabs();
        document.getElementById('searchBtn').onclick = () => search(document.getElementById('queryInput').value);
        document.getElementById('queryInput').onkeypress = (e) => { if (e.key === 'Enter') search(e.target.value); };
    };
</script>
</body>
</html>
'''

@app.route('/')
def index():
    return HTML_PAGE

@app.route('/api/search', methods=['POST'])
def search_api():
    data = request.get_json()
    query = data.get('query', '').strip()
    if not query:
        return jsonify({"error": "Пустой запрос"}), 400
    
    url = f"{API_BASE_URL}{requests.utils.quote(query)}&token={API_TOKEN}&lang=ru"
    try:
        resp = requests.get(url, timeout=25)
        resp.raise_for_status()
        return jsonify(resp.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Ошибка API: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)