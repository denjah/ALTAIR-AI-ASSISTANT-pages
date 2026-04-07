const fs = require('fs');
const https = require('https');

const fetchUrl = (url) => {
    return new Promise((resolve, reject) => {
        https.get(url, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => resolve(data));
        }).on('error', reject);
    });
};

async function main() {
    const compId = '43504';
    const url = `https://altaircom.bitrix24.ru/rest/276/nxv29r67o1qp5hd3/crm.company.get.json?id=${compId}`;

    try {
        const data = await fetchUrl(url);
        fs.writeFileSync('company_43504.json', JSON.stringify(JSON.parse(data), null, 2));

        // Also let's try to get activities or deals for this company
        const list_deals_url = `https://altaircom.bitrix24.ru/rest/276/nxv29r67o1qp5hd3/crm.deal.list.json?filter[COMPANY_ID]=${compId}`;
        const d_data = await fetchUrl(list_deals_url);
        fs.writeFileSync('company_43504_deals.json', JSON.stringify(JSON.parse(d_data), null, 2));

        const acts = await fetchUrl(`https://altaircom.bitrix24.ru/rest/276/nxv29r67o1qp5hd3/crm.activity.list.json?filter[OWNER_TYPE_ID]=4&filter[OWNER_ID]=${compId}`);
        fs.writeFileSync('company_43504_activities.json', JSON.stringify(JSON.parse(acts), null, 2));

    } catch (e) {
        console.error(e);
    }
}

main();
