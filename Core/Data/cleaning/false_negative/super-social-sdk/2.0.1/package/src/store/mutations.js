import Vue from 'vue'

import {
    ADD_ATTACHED_TICKET,
    ADD_FEATURE_FLAG,
    DEBUG_LOG,
    LOGOUT,
    REMOVE_ATTACHED_TICKET,
    REMOVE_FEATURE_FLAG,
    REMOVE_SCROLL_TO_REF,
    SET_ACTIVE_MOBILE_TAB,
    SET_AUTH,
    SET_CHAT_EVENT,
    SET_CONFIG,
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

export default {
    [SET_CT_TOKEN]: (state, ctToken) => {
        state.ctSessionToken = ctToken
    },

    [SET_SOCIAL_TOKEN]: (state, socialToken) => {
        state.socialSessionToken = socialToken
    },

    [SET_RETRY_LOGIN]: (state, retryLogin) => {
        state.retryLogin = retryLogin
    },

    [SET_NOTIFICATIONS_COUNT]: (state, notificationsCount) => {
        state.notificationsCount = notificationsCount
    },

    [SET_IS_CHAT_OPEN]: (state, isChatOpen) => {
        state.isChatOpen = isChatOpen
    },

    [SET_CHAT_EVENT]: (state, chatEvent) => {
        state.chatEvent = chatEvent
    },

    [ADD_ATTACHED_TICKET]: (state, { ticket, entityId }) => {
        Vue.set(state.attachedTickets, entityId, ticket)
    },

    [REMOVE_ATTACHED_TICKET]: (state, entityId) => {
        Vue.delete(state.attachedTickets, entityId)
    },

    [SET_IS_LOADING_TOKENS]: (state, isLoadingTokens) => {
        state.isLoadingTokens = isLoadingTokens
    },

    [SET_USER_ID]: (state, userId) => {
        state.userId = userId
    },

    [SET_CONFIG]: (state, config) => {
        state.config = { ...config }
    },

    [SET_AUTH]: (state, auth) => {
        state.auth = auth
    },

    [DEBUG_LOG]: (state, messages) => {
        if (state.config.debug) {
            messages.forEach(msg => console.log(msg))
        }
    },

    [SET_LOCALISATIONS]: (state, localisations) => {
        state.localisations = localisations
    },

    [LOGOUT]: state => {
        state.ctSessionToken = null

        state.socialSessionToken = null

        state.notificationsCount = null

        state.user = null

        state.userConfig = null

        localStorage.removeItem(state.config.localStorageKeyName)
    },

    [REMOVE_SCROLL_TO_REF]: state => {
        delete state.chatEvent.scrollToComment
    },

    [ADD_FEATURE_FLAG]: (state, featureFlag) => {
        state.featureFlags = {
            ...state.featureFlags,
            ...featureFlag,
        }
    },

    [REMOVE_FEATURE_FLAG]: (state, featureFlag) => {
        delete state.featureFlags[featureFlag]
    },

    [SET_TICKET_DETAILS_DATA]: (state, ticketDetailsData) => {
        state.ticketDetailsData = JSON.parse(JSON.stringify(ticketDetailsData))
    },

    [SET_ACTIVE_MOBILE_TAB]: (state, activeMobileTab) => {
        state.activeMobileTab = activeMobileTab
    },
}
