import { MobileSocialTabs } from '../utils/Enums'

export default {
    config: null,
    auth: null,
    localisations: null,
    ctSessionToken: null,
    socialSessionToken: null,
    cognitoRelogCount: 0,
    retryLogin: false,
    notificationsCount: null,
    isChatOpen: null,
    chatEvent: null,
    attachedTickets: {},
    isLoadingTokens: false,
    userId: '',
    featureFlags: {},
    ticketDetailsData: null,
    activeMobileTab: MobileSocialTabs.superSocial,
}
