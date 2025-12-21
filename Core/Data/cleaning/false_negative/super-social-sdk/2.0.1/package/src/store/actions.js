import axios from 'axios'
import jwtDecode from 'jwt-decode'

import { isMobileUserAgent } from '../utils/Helpers'
import protify from '../utils/Protify'

import {
    ADD_ATTACHED_TICKET,
    DEBUG_LOG,
    LOGOUT,
    REMOVE_ATTACHED_TICKET,
    REMOVE_SCROLL_TO_REF,
    SET_ACTIVE_MOBILE_TAB,
    SET_CHAT_EVENT,
    SET_CT_TOKEN,
    SET_IS_CHAT_OPEN,
    SET_IS_LOADING_TOKENS,
    SET_LOCALISATIONS,
    SET_NOTIFICATIONS_COUNT,
    SET_RETRY_LOGIN,
    SET_SOCIAL_TOKEN,
    SET_TICKET_DETAILS_DATA,
    SET_USER_ID,
} from './types'

import { CLEAR_USER_FOLLOWS, SET_USER, SET_USER_CONFIG, SET_USER_PROFILE } from './modules/user/userIndex'

const acceptHeader = 'application/protobuf'

export default {
    debugLog({ commit }, messages) {
        commit(DEBUG_LOG, messages)
    },

    fetchNotificationsCount({ state, commit, dispatch }) {
        const url = `${state.config.api.baseUrl}/notifications/new/count`

        // eslint-disable-next-line promise/catch-or-return
        dispatch('verifyToken').then(() => {
            axios
                .get(url, {
                    headers: {
                        Accept: acceptHeader,
                        authentication: state.socialSessionToken.AccessToken,
                        'sa-client-id': state.ctSessionToken.userId,
                    },
                    responseType: 'arraybuffer',
                    timeout: 5000,
                })
                .then(response => {
                    const protoObject = protify('NotificationsCount', response.data)

                    commit(SET_NOTIFICATIONS_COUNT, protoObject.count)
                })
                .catch(error => {
                    commit(DEBUG_LOG, ['Error fetching new notifications count', error])
                })
        })
    },

    // verifies Social Token via Cognito
    verifyToken({ state, commit, dispatch }, token) {
        const tokenToVerify = token ?? state.socialSessionToken

        // eslint-disable-next-line compat/compat
        return new Promise(resolve => {
            const now = Math.floor(Date.now() / 1000)

            // Very verbose for readability, also parseInt to future proof it to be sure, just in case AWS returns numbers as strings
            const expiresIn = parseInt(tokenToVerify.ExpiresIn || 0, 10)
            const requestedAt = parseInt(tokenToVerify.RequestedAt || 0, 10)
            const expiresAt = expiresIn + requestedAt

            const isTokenValid = now < expiresAt

            if (!isTokenValid) {
                // eslint-disable-next-line camelcase
                const { event_id, exp, iat, client_id, username } = jwtDecode(tokenToVerify.AccessToken)

                dispatch('sendCognitoAnalytics', {
                    params: {
                        action: 'token_refresh',
                        requested_at: now,
                        // eslint-disable-next-line camelcase
                        token_to_verify: { event_id, exp, iat, client_id, username },
                    },
                    userId: state.ctSessionToken?.userId,
                })

                // start cognito refresh token procedure
                state.auth
                    .refreshCredentials(tokenToVerify.RefreshToken)
                    .then(refreshedTokens => {
                        dispatch('setSocialSession', {
                            ...refreshedTokens.AuthenticationResult,
                            RequestedAt: now,
                        })

                        resolve()
                    })
                    .catch(() => {
                        // cannot autorefresh cognito token with the currently saved refresh token, try relogging with CT

                        // attempting new login with the currently available CT token
                        // eslint-disable-next-line promise/catch-or-return
                        dispatch('cognitoLogin', state.ctSessionToken).then(() => {
                            resolve()
                        })
                    })
            } else {
                // save the new token only if we were actually checking the new token and not the one that was in the store already
                if (token) {
                    dispatch('setSocialSession', tokenToVerify)
                }

                resolve()
            }
        })
    },

    cognitoLogin({ state, commit, dispatch }, token) {
        const now = Math.round(Date.now() / 1000)

        dispatch('sendCognitoAnalytics', {
            params: {
                action: 'login',
                requested_at: now,
            },
            userId: state.ctSessionToken?.userId,
        })

        return state.auth
            .login({
                userId: token.userId,
                sessionId: token.sessionId,
            })
            .then(response => {
                dispatch('setSocialSession', {
                    ...response.AuthenticationResult,
                    RequestedAt: Math.floor(Date.now() / 1000),
                })
            })
            .catch(error => {
                // raise the retry flag so users can try and reconnect. error 400 will show the default onboarding
                if (error.response.status !== 400) {
                    commit(SET_RETRY_LOGIN, true)
                }

                commit(SET_IS_LOADING_TOKENS, false)
            })
    },

    // eslint-disable-next-line sonarjs/cognitive-complexity
    async setCtSession({ state, commit, dispatch }, { token, isSocialEnabled }) {
        if (isSocialEnabled) {
            dispatch('fetchLocalisations')
        }

        if (token && isSocialEnabled) {
            commit(SET_IS_LOADING_TOKENS, true)

            commit(SET_CT_TOKEN, token)

            commit(SET_USER_ID, `${token.userId}`)

            // verify cognito token if it's already here while CT session changes
            if (state.socialSessionToken) {
                await dispatch('verifyToken')
            }
            // check if there are existing cognito tokens saved (initial load)
            else {
                const existingSocialSessionToken = localStorage.getItem(state.config.localStorageKeyName)

                if (existingSocialSessionToken) {
                    const decodedToken = jwtDecode(JSON.parse(existingSocialSessionToken).AccessToken)
                    if (decodedToken.username === token.userId.toString()) {
                        await dispatch('verifyToken', JSON.parse(existingSocialSessionToken))
                    } else {
                        commit(LOGOUT)

                        dispatch('cognitoLogin', token)
                    }
                } else {
                    dispatch('cognitoLogin', token)
                }
            }
        } else if (!token) {
            dispatch('logout')
        }
    },

    setSocialSession({ state, commit, dispatch }, token) {
        // obscure async race condition fix, DO NOT REMOVE
        if (!state.ctSessionToken) {
            return
        }

        commit(SET_SOCIAL_TOKEN, token)

        localStorage.setItem(state.config.localStorageKeyName, JSON.stringify(token))

        if (!state.user.user) {
            dispatch('fetchNotificationsCount')

            dispatch('user/fetchUser').finally(() => commit(SET_IS_LOADING_TOKENS, false))
        }
    },

    /**
     * Action for fetching frontend localisations
     */
    fetchLocalisations({ state, commit }) {
        if (state.localisations) {
            return
        }

        const configLanguage = state.config.language === 'rs' ? 'sr_Latn' : state.config.language

        const url = `https://scorealarm-stats.freetls.fastly.net/localization/superbet/social/${configLanguage}.json`

        axios
            .get(url)
            .then(response => {
                commit(SET_LOCALISATIONS, response.data)
            })
            .catch(error => {
                commit(DEBUG_LOG, ['Error fetching localisations', error])
            })
    },

    removeScrollToCommentReference({ commit }) {
        commit(REMOVE_SCROLL_TO_REF)
    },

    setAttachedTicket({ commit }, { ticket, entityId }) {
        commit(ADD_ATTACHED_TICKET, { ticket, entityId })
    },

    removeAttachedTicket({ commit }, entityId) {
        commit(REMOVE_ATTACHED_TICKET, entityId)
    },

    setChatEvent({ commit }, event) {
        commit(SET_CHAT_EVENT, event)
    },

    openEventChat({ commit }, event) {
        if (event) {
            commit(SET_CHAT_EVENT, event)
        }

        commit(SET_IS_CHAT_OPEN, true)
    },

    closeEventChat({ commit }) {
        commit(SET_IS_CHAT_OPEN, false)
    },

    sendTicketCopyAnalytics({ state, commit }, { isOnline, params }) {
        const url = `${state.config.api.analyticsBaseUrl}/analytics/send`
        const event = isOnline ? 'social_ticket_referral' : 'social_ticket_referral_prepared'
        const timestamp = new Date().toISOString().replace(/\.[0-9]{3}/, '')
        const userId = `${state.ctSessionToken.userId}`

        const request = {
            url,
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            data: {
                event,
                params: {
                    ...params,
                    user_id: userId,
                },
                app: {
                    bundle_id: `${state.config.country}.superbet.sport${
                        state.config.environment === 'stage' ? '.stage' : ''
                    }`,
                    key: state.config.variant,
                    version: state.config.appVersion,
                    social_version: state.config.socialVersion,
                    platform: isMobileUserAgent() ? 'mobile_web' : 'web',
                },
                user: {
                    user_id: userId,
                },
                timestamp,
            },
        }

        axios(request).catch(error => {
            commit(DEBUG_LOG, [`Error sending analytics for ${event}`, error])
        })
    },

    removeSocialSessionToken({ commit }) {
        commit(SET_SOCIAL_TOKEN, null)
    },

    logout({ state, commit }) {
        commit(SET_CT_TOKEN, null)

        commit(SET_SOCIAL_TOKEN, null)

        commit(SET_NOTIFICATIONS_COUNT, null)

        commit(`user/${SET_USER}`, null)

        commit(`user/${SET_USER_CONFIG}`, null)

        commit(`user/${SET_USER_PROFILE}`, null)

        commit(`user/${CLEAR_USER_FOLLOWS}`)

        localStorage.removeItem(state.config.localStorageKeyName)
    },

    /**
     * sends analytics on every cognito login/token refresh
     *
     * @param {Object} options
     * @param {Object} options.params
     * @param {String} options.params.action - login | token_refresh
     * @param {Date} options.params.requested_at - Date.now()
     * @param {String} options.params.token_to_verify - Token to be refreshed / verified
     * @param {String} options.userId - CT user ID
     *
     * TODO: refactor this as well as the sendAnalytics.js mixing into proper analytics once we implement v2
     */
    sendCognitoAnalytics({ state, commit }, options) {
        const { config } = state

        const url = `${config.api.analyticsBaseUrl}/analytics/send`
        const timestamp = new Date().toISOString().replace(/\.[0-9]{3}/, '')

        const data = {
            event: 'cognito_request',
            params: options.params,
            app: {
                bundle_id: `${config.country}.superbet.sport${config.environment === 'stage' ? '.stage' : ''}`,
                key: config.variant,
                version: config.appVersion,
                social_version: config.socialVersion,
                platform: isMobileUserAgent() ? 'mobile_web' : 'web',
            },
            user: {
                user_id: options.userId,
            },
            timestamp,
        }

        // eslint-disable-next-line compat/compat
        window.navigator.sendBeacon(url, JSON.stringify(data))
    },

    setTicketDetailsData({ commit }, ticketDetailsData) {
        commit(SET_TICKET_DETAILS_DATA, ticketDetailsData)
    },

    setActiveMobileTab({ commit }, activeMobileTab) {
        commit(SET_ACTIVE_MOBILE_TAB, activeMobileTab)
    },

    reportProfile({ state, dispatch, commit }, userId) {
        const url = `${state.config.api.baseUrl}/friends/user/report`

        // eslint-disable-next-line promise/catch-or-return
        dispatch('verifyToken').then(() => {
            axios
                .post(
                    url,
                    {
                        user_id: userId,
                    },
                    {
                        headers: {
                            Accept: acceptHeader,
                            authentication: state.socialSessionToken.AccessToken,
                            'sa-client-id': state.ctSessionToken.userId,
                        },
                        responseType: 'arraybuffer',
                        timeout: 5000,
                    }
                )
                .catch(error => {
                    commit(DEBUG_LOG, ['Error reporting user', error])
                })
        })
    },
}
