addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

/**
 * Respond to the request
 * @param {Request} request
 */
async function handleRequest(request) {
  const duration = request.url.split('?q=').slice(-1),
    url = `https://api.cloudflare.com/client/v4/zones/${ZONE}/analytics/dashboard?since=-${duration}`,
    respData = await fetch(url, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${KEY}`,
      },
    })
    .then(resp => resp.json())
    .then(json => json.result.totals.uniques.all);

  const resp = new Response(JSON.stringify({cnt: respData}))
  resp.headers.set('Content-Type', 'application/json');
  return resp;
}