const URL_PARAMS = {
  id: 'zfid',
  token: 'zftoken',
};

function getUrlParams(location) {
  const searchParams = new URLSearchParams(location.search);

  return {
    id: searchParams.get(URL_PARAMS.id) || null,
    token: searchParams.get(URL_PARAMS.token) || null,
  };
}

function removeUrlParams(originalUrl) {
  const url = new URL(originalUrl);
  const searchParams = new URLSearchParams(url.search);

  searchParams.delete(URL_PARAMS.token);
  url.search = searchParams.toString();
  return url.toString();
}

module.exports = {
  getUrlParams,
  removeUrlParams,
};
