export default {
    localisations(state) {
        return state.localisations
    },

    ctSessionToken(state) {
        return state.ctSessionToken
    },

    socialSessionToken(state) {
        return state.socialSessionToken
    },

    retryLogin(state) {
        return state.retryLogin
    },

    notificationsCount(state) {
        return state.notificationsCount
    },

    isChatOpen(state) {
        return state.isChatOpen
    },

    chatEvent(state) {
        return state.chatEvent
    },

    attachedTickets(state) {
        return state.attachedTickets
    },

    isLoadingTokens(state) {
        return state.isLoadingTokens
    },

    config(state) {
        return state.config
    },

    auth(state) {
        return state.auth
    },

    featureFlags(state) {
        return state.featureFlags
    },

    ticketDetailsData(state) {
        return state.ticketDetailsData
    },

    activeMobileTab(state) {
        return state.activeMobileTab
    },
}
