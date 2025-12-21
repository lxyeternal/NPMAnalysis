const nock = require('nock');
const fetchPolyfill = require('node-fetch');
const requests = require('./mocks/requests');
const { fetchLeadInfo, trackEvent } = require('../fetcher');

const API_HOST = 'https://api.zenfi.mx';
const TOKEN = 'SAMPLE_TOKEN';

if (!global.fetch) global.fetch = fetchPolyfill;

describe('fetcher', () => {
  describe('.fetchLeadInfo', () => {
    const mockRequest = ({ status, body }) => nock(API_HOST)
      .get('/products/leads/info')
      .query({ token: TOKEN })
      .reply(status, body);

    describe('when the lead returns information', () => {
      beforeEach(() => mockRequest(requests.leadsInfo.success));

      it('returns the info as object', async () => {
        const results = await fetchLeadInfo(TOKEN);
        expect(results).toEqual({
          name: 'Guillermo',
          lastName: 'Del Toro',
          email: 'user1@zenfi.mx',
        });
      });
    });

    describe('when the lead returns empty', () => {
      beforeEach(() => mockRequest(requests.leadsInfo.blank));

      it('returns an empty object', async () => {
        const results = await fetchLeadInfo(TOKEN);
        expect(results).toEqual({});
      });
    });

    describe('when token is not valid anymore', () => {
      beforeEach(() => mockRequest(requests.leadsInfo.unauthorized));

      it('raises an error', async () => {
        await expect(async () => {
          await fetchLeadInfo(TOKEN);
        })
          .rejects
          .toThrow(new Error('UNAUTHORIZED'));
      });
    });
  });

  describe('.trackEvent', () => {
    const partner = 'yotepresto';
    const eventType = 'converted';
    const eventData = {
      zenfiId: 'ZENFI_ID',
      event: 'EVENT_NAME',
      meta: {
        foo: 'bar',
      },
    };

    const mockRequest = ({ status, body }) => nock(API_HOST)
      .post(`/webhooks/leads/${partner}/${eventType}`, eventData)
      .reply(status, body);

    beforeEach(() => mockRequest({ status: 200, body: { partner, ...eventData } }));

    it('returns the created event', async () => {
      const results = await trackEvent({
        partner,
        type: eventType,
        zenfiId: eventData.zenfiId,
        event: eventData.event,
        meta: eventData.meta,
      });
      expect(results).toEqual({
        partner,
        ...eventData,
      });
    });
  });
});
