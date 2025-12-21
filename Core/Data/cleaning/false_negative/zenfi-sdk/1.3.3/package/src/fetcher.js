const ENDPOINTS = {
  leadsInfo: {
    url: 'https://api.zenfi.mx/products/leads/info',
    method: 'GET',
  },
  trackEvent: {
    url: 'https://api.zenfi.mx/webhooks/leads/:partner/:type',
    method: 'POST',
  },
};

const DEFAULT_HEADERS = {
  Accept: 'application/json',
  'Content-Type': 'application/json',
};

async function fetchLeadInfo(token) {
  const { url: baseUrl, method } = ENDPOINTS.leadsInfo;
  const url = `${baseUrl}?token=${token}`;

  const response = await fetch(url, {
    method,
    headers: DEFAULT_HEADERS,
  });
  const data = await response.json();
  if (response.ok) return data.info || {};
  if (response.status === 401) throw new Error('UNAUTHORIZED');
  throw new Error(data.code);
}

function trackEvent({
  meta,
  type,
  event,
  partner,
  zenfiId,
}) {
  const { url: baseUrl, method } = ENDPOINTS.trackEvent;
  const url = baseUrl
    .replace(':type', type)
    .replace(':partner', partner);

  const body = {
    zenfiId,
    event,
    meta,
  };

  return fetch(url, {
    method,
    headers: DEFAULT_HEADERS,
    body: JSON.stringify(body),
  })
    .then((response) => response.json());
}

module.exports = {
  fetchLeadInfo,
  trackEvent,
};
