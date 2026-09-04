// ==UserScript==
// @name         IMDb Watchlist Importer (V11 - ULTIMATE)
// @namespace    http://tampermonkey.net/
// @version      11.0
// @description  Dual-mode importer (GraphQL + Classic Fallback).
// @author       Your Name
// @match        https://www.imdb.com/user/*/watchlist*
// @match        https://www.imdb.com/watchlist*
// @grant        none
// ==/UserScript==

(function () {
    'use strict';

    // Вставьте сюда свой список фильмов из data/imdb_import_clean.json
    // Формат: { "name": "Movie Title", "imdb": "tt1234567" }
    const HARDCODED_MOVIES = [
        // { "name": "Example Movie", "imdb": "tt0000001" },
    ];

    const GRAPHQL_ENDPOINT = 'https://api.graphql.imdb.com/';
    const MUTATION = `mutation UpdateTitleInterest($input: UpdateTitleInterestInput!) { updateTitleInterest(input: $input) { __typename } }`;

    const interval = setInterval(() => {
        const container = document.querySelector('.ipc-page-section--base, .watchlist-index-page');
        if (container) { clearInterval(interval); setupUI(container); }
    }, 1000);

    function setupUI(container) {
        if (document.getElementById('imdb-importer-v11')) return;
        const root = document.createElement('div');
        root.id = 'imdb-importer-v11';
        root.style = `margin: 20px 0; padding: 24px; background: #000; border: 3px solid #f5c518; border-radius: 12px; font-family: Roboto, sans-serif; box-shadow: 0 8px 32px rgba(245, 197, 24, 0.3); color: #fff;`;
        root.innerHTML = `
            <h3 style="margin-top: 0; color: #f5c518; display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 24px;">🚀</span> IMDb Importer v11.0 (ULTIMATE)
            </h3>
            <div style="display: flex; align-items: center; gap: 20px;">
                <button id="start-btn" style="padding: 14px 40px; background: #f5c518; color: #000; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 16px;">
                    START DUAL-MODE IMPORT
                </button>
                <div id="status-text" style="font-weight: bold; font-size: 16px; color: #f5c518;">Ready</div>
            </div>
            <div id="log-box" style="margin-top: 20px; max-height: 300px; overflow-y: auto; background: #111; color: #00ff00; padding: 15px; font-size: 12px; font-family: monospace; border-radius: 6px; border: 1px solid #333;"></div>
        `;
        container.insertBefore(root, container.firstChild);

        const btn = root.querySelector('#start-btn');
        const status = root.querySelector('#status-text');
        const log = root.querySelector('#log-box');

        const addLog = (msg, color = '#00ff00') => {
            const line = document.createElement('div');
            line.style.color = color;
            line.innerText = `[${new Date().toLocaleTimeString()}] ${msg}`;
            log.prepend(line);
        };

        btn.onclick = async () => {
            btn.disabled = true;
            for (let i = 0; i < HARDCODED_MOVIES.length; i++) {
                const m = HARDCODED_MOVIES[i];
                status.innerText = `Processing (${i + 1}/${HARDCODED_MOVIES.length}): ${m.name}`;
                
                let success = false;
                
                // --- МЕТОД 1: GraphQL ---
                try {
                    const response = await fetch(GRAPHQL_ENDPOINT, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json', 'x-imdb-client-name': 'imdb-web-next' },
                        body: JSON.stringify({
                            query: MUTATION,
                            operationName: 'UpdateTitleInterest',
                            variables: { input: { titleId: m.imdb, interestStatus: "INTERESTED" } } // interestLevel убран для совместимости
                        }),
                        credentials: 'include'
                    });
                    const res = await response.json();
                    if (!res.errors) { success = true; addLog(`[GQL SUCCESS] ${m.name}`); }
                } catch (e) {}

                // --- МЕТОД 2: Classic POST (Fallback) ---
                if (!success) {
                    try {
                        const response = await fetch(`https://www.imdb.com/watchlist/${m.imdb}/add`, {
                            method: 'POST',
                            credentials: 'include'
                        });
                        if (response.ok) { success = true; addLog(`[CLASSIC SUCCESS] ${m.name}`, '#44ff44'); }
                        else { throw new Error(`Status ${response.status}`); }
                    } catch (e) {
                        addLog(`[FATAL FAIL] ${m.name}: ${e.message}`, '#ff4444');
                    }
                }

                await new Promise(r => setTimeout(r, 1200));
            }
            status.innerText = '🎯 MISSION ACCOMPLISHED!';
            btn.disabled = false;
        };
    }
})();
