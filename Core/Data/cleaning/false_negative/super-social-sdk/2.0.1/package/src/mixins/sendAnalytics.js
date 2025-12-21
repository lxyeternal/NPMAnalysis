import { mapActions, mapGetters } from 'vuex'
import axios from 'axios'

import { isMobileUserAgent } from '../utils/Helpers'

export default {
    computed: {
        ...mapGetters('social', ['config', 'ctSessionToken']),
    },
    methods: {
        ...mapActions('social', ['debugLog']),
        sendEvent(event, params) {
            const url = `${this.config.api.analyticsBaseUrl}/analytics/send`
            const timestamp = new Date().toISOString().replace(/\.[0-9]{3}/, '')

            const request = {
                url,
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                data: {
                    event,
                    params: params ?? {},
                    app: {
                        bundle_id: `${this.config.country}.superbet.sport${
                            this.config.environment === 'stage' ? '.stage' : ''
                        }`,
                        key: this.config.variant,
                        version: this.config.appVersion,
                        social_version: this.config.socialVersion,
                        platform: isMobileUserAgent() ? 'mobile_web' : 'web',
                    },
                    user: {
                        user_id: this.ctSessionToken?.userId.toString(),
                    },
                    timestamp,
                },
            }

            axios(request).catch(error => {
                this.debugLog([`Error sending analytics for ${event}`, error])
            })
        },
    },
}
