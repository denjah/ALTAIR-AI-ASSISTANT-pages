---
description: Deep Client Analysis
---

# Deep Client Analysis

**Описание:**  
Запускает полный Deep Client Analysis по ID сделки или контакта. Использует все подключённые skills и multi-agent оркестрацию.

**Как запускать:**  
/deal 12345  
или  
/analyze 12345

**Шаги workflow (агент выполняет автоматически):**
1. Coordinator получает ID и запускает DataCollector (bitrix24-deep-crm-analyzer).
2. Researcher анализирует сайт клиента.
3. Analyst извлекает боли, пожелания, цитаты (call-transcript-analyzer + pain-point-extractor).
4. Strategist формирует финальное резюме (sales-strategist).
5. Выводит результат строго в заданном Markdown-формате.

После формирования текстового резюме обязательно вызови skill "report-landing-generator" и сгенерируй полный HTML-лендинг в стиле ALTAIR.
В финальном выводе добавь строку:

**Отчёт-лендинг (HTML):** [ссылка на сгенерированный файл или содержимое]

**Ограничения:**  
Только факты из данных сделки. Авторитетный тон. Готово к копипасту менеджеру.