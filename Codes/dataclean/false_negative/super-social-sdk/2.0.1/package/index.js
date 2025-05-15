// import SDK components
import SuperSocialProfile from './src/components/v1/SocialProfile.vue'

// import Cognito Auth
import { CognitoAuth } from './src/auth/CognitoAuth'
// import SDK store
import SuperSocialStore from './src/store/index'
import { ADD_FEATURE_FLAG, SET_AUTH, SET_CONFIG } from './src/store/types'

// eslint-disable-next-line import/no-unresolved
const { version } = require('super-social-sdk/package.json')

// import component styling
// eslint-disable-next-line no-undef
require('./scss/main.scss')

// plugin init
export default {
    /**
     * @callback subscribeToFeatureChanges
     * @param {string} flagName - name of the flag
     * @param {Function} callback - function that is called when value changes
     * @param {T} defaultValue - default value if service is unavailable
     * @returns {Promise} unsubscribe - used for unsubscribing
     */

    /**
     * Superbet Social SDK
     * @param {Vue} Vue - Vue instance
     * @param {Object} options - External options passed into the SDK
     * @param {boolean} options.debug - Enables various console logs for dev/debug
     * @param {object} options.ctToken - Comtrade user session token
     * @param {string} options.variant - App variant (fallback to rosuperbetsport)
     * @param {string} options.language - SDK language (fallback to romanian)
     * @param {string} options.environment - stage | prod
     * @param {Object} options.cognito - cognito init params (country, useProduction)
     * @param {Vuex} options.store - vuex instance
     * @param {object} options.featureFlagService - service used for feature flags
     * @param {subscribeToFeatureChanges} options.featureFlagService.subscribeToFeatureChanges
     * @param {object} options.routeFragments - localised route fragments (user, feed, (my)Followers, profile, ticket)
     * @param {object} options.offerService - service used for subscribing to events
     * @param {function} options.setFullScreen - axilis helper that removes bottom nav on mobile and adds class 'full-screen'
     */
    // eslint-disable-next-line sonarjs/cognitive-complexity
    install(Vue, options) {
        Vue.prototype.$offerService = options.offerService

        Vue.prototype.$setFullScreen = options.setFullScreen

        const supportedLanguages = ['en', 'ro', 'pl', 'hr', 'rs']
        const supportedVariants = ['rosuperbetsport', 'plsuperbetsport', 'rssuperbetsport']

        // fallback to RO localization
        const language = options?.language && supportedLanguages.includes(options.language) ? options.language : 'ro'
        const variant =
            options?.variant && supportedVariants.includes(options.variant) ? options.variant : 'rosuperbetsport'

        const apiEndpoints = {
            dev: {
                baseUrl: `https://social-front-${variant}-staging.freetls.fastly.net/${variant}`,
                imgBaseUrl: `https://social-front-${variant}-staging.freetls.fastly.net`,
                analyticsBaseUrl: 'https://frontstagingstatssuperbetcom.freetls.fastly.net',
            },
            prod: {
                baseUrl: `https://social-front-${variant}-production.freetls.fastly.net/${variant}`,
                imgBaseUrl: `https://social-front-${variant}-production.freetls.fastly.net`,
                analyticsBaseUrl: 'https://scorealarm-stats.freetls.fastly.net',
            },
        }

        const initStore = () => {
            SuperSocialStore.mutations[SET_CONFIG](SuperSocialStore.state, {
                // enables various console logs
                debug: !!options?.debug,
                // SDK endpoints
                api: options?.debug ? apiEndpoints.dev : apiEndpoints.prod,
                // fallback to RO variant
                variant,
                // fallback to RO localization
                language,
                localStorageKeyName: 'superSocialUserToken',
                // Superbet web app version
                appVersion: options.appVersion,
                // social sdk version
                socialVersion: version,
                // stage | prod
                environment: options.environment,
                // ro | pl | hr | rs
                country: options.cognito.country,
                // user, feed, (my)Followers, profile, ticket
                routeFragments: options.routeFragments,
            })

            SuperSocialStore.mutations[SET_AUTH](
                SuperSocialStore.state,
                new CognitoAuth(options?.cognito || { useProduction: false, country: 'ro' })
            )
        }

        initStore()

        if (!options.featureFlagService) {
            throw Error('Missing FeatureFlagService instance in SuperSocialConfig')
        }

        const initFeatureFlags = () => {
            options.featureFlagService.subscribeToFeatureChanges(
                'super-social.split_chat',
                value => {
                    SuperSocialStore.mutations[ADD_FEATURE_FLAG](SuperSocialStore.state, value)
                },
                {
                    split_chat: [
                        {
                            suffix: '',
                            type: 'all_matches',
                        },
                    ],
                }
            )

            options.featureFlagService.subscribeToFeatureChanges(
                'super-social.chat-banner-v2',
                value => {
                    SuperSocialStore.mutations[ADD_FEATURE_FLAG](SuperSocialStore.state, { showNewChatBanner: value })
                },
                { showNewChatBanner: false }
            )
        }

        initFeatureFlags()

        if (!options.store) {
            throw Error('Missing Vuex instance in SuperSocialConfig')
        }

        options.store.registerModule('social', SuperSocialStore)
    },
}

export { SuperSocialProfile }
