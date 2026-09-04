/**
 * УЛЬТИМАТИВНЫЙ ПАРСЕР (2026)
 * Работает на странице оценок и в папках.
 */

(() => {
    console.log("%c🚀 Сбор данных начат...", "color: cyan; font-weight: bold;");

    // 1. Находим все ссылки на фильмы, у которых есть текст (названия)
    const allLinks = Array.from(document.querySelectorAll('a[href*="/film/"], a[href*="/series/"]'));
    const movieLinks = allLinks.filter(a => a.innerText.trim().length > 1 && !a.querySelector('img'));

    let results = [];

    movieLinks.forEach((link, index) => {
        const title = link.innerText.trim();

        // Ищем всю строку (обычно это tr или div с классом item)
        const row = link.closest('tr, .item, li');

        if (!row) return;

        // Пытаемся найти оценку (в классе myVote или просто число в конце строки)
        const myVoteEl = row.querySelector('.myVote, .vote');
        let myVote = myVoteEl ? myVoteEl.innerText.trim() : 'Нет оценки';

        // Если оценка всё еще не найдена, ищем в тексте строки (часто оценка идет после названия)
        if (myVote === 'Нет оценки' || myVote === '') {
            const text = row.innerText;
            const voteMatch = text.match(/(\d{1,2})\s+\d\.\d{3}/); // Ищет конструкцию типа "9 7.33"
            if (voteMatch) myVote = voteMatch[1];
        }

        // Дата
        const dateEl = row.querySelector('.date, .viewDate') || row.querySelector('span[style*="color: #777"]');
        const date = dateEl ? dateEl.innerText.trim() : '';

        results.push(`${title} | Оценка: ${myVote} | Дата: ${date}`);
    });

    // Убираем возможные дубликаты
    const uniqueResults = [...new Set(results)];

    console.log("%c🎯 ГОТОВО!", "color: l綠; font-weight: bold;");
    console.log("====================================");
    console.log(uniqueResults.join('\n'));
    console.log("====================================");
    console.log(`Собрано уникальных фильмов: ${uniqueResults.length}`);
    console.log("Если фильмов меньше 150 — прокрути страницу вниз и выбери 'показывать по 200'!");
})();
