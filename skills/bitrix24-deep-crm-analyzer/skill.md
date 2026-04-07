# Bitrix24 Deep CRM Analyzer

**Метод получения данных**: Webhook (REST API)  
**URL Webhook**: `https://altaircom.bitrix24.ru/rest/276/nxv29r67o1qp5hd3/`

**Инструкции (выполняй строго):**

## Базовые вызовы

1. **Карточка сделки**: вызови MCP `b24-dev-mcp` → `crm.deal.get` с параметром `{id: DEAL_ID}`
2. **Карточка компании**: `crm.company.get` → `{id: COMPANY_ID}` (из поля `COMPANY_ID` сделки)
3. **Карточка контакта**: `crm.contact.get` → `{id: CONTACT_ID}` (из поля `CONTACT_ID` сделки)

## Расширенные вызовы

4. **Timeline сделки**: `crm.timeline.list` → `{entityTypeId: 2, entityId: DEAL_ID}`
5. **Активности**: `crm.activity.list` → `{filter: {OWNER_TYPE_ID: 2, OWNER_ID: DEAL_ID}}`
6. **Задачи**: `tasks.task.list` → `{filter: {UF_CRM_TASK: ["D_" + DEAL_ID]}}`

## Транскрипты и переписки

7. Из активностей типа `CALL` — извлекай транскрипты CoPilot
8. Из активностей типа `EMAIL` — извлекай текст писем
9. Из Open Lines — извлекай историю чатов

## Правила
- Делай параллельные запросы (1-3 можно параллельно, 4-6 можно параллельно)
- Все кастомные поля (UF_*) ОБЯЗАТЕЛЬНО собирай
- Если данных не хватает — делай повторные запросы с расширенными фильтрами
- Сохраняй весь контекст — ничего не пропускай
- При ошибке API — повтори 1 раз, затем сообщи координатору