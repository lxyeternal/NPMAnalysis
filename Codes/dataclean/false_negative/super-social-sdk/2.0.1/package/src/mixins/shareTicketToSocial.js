import { mapActions } from 'vuex'
import axios from 'axios'

import { isMobileUserAgent } from '../utils/Helpers'

import checkTicketOnSocial from './checkTicketOnSocial'
import requestOptions from './requestOptions'

export default {
    ...mapActions('social', ['verifyToken', 'debugLog']),

    mixins: [requestOptions, checkTicketOnSocial],

    methods: {
        async shareTicketToSocial(ticket) {
            const isOnSocial = await this.checkTicketOnSocial(ticket)

            // if ticket is already on social, do nothing
            if (isOnSocial) {
                return
            }

            const request = {
                url: `${this.endpoints.baseUrl}/tickets/ticket`,
                method: 'POST',
                headers: this.requestOptions.post,
                data: {
                    ...ticket,
                    client_platform: isMobileUserAgent() ? 'mobile_web' : 'web',
                },
            }

            // eslint-disable-next-line consistent-return
            return this.verifyToken().then(async () =>
                axios(request).catch(error => {
                    this.debugLog(['Error sharing ticket to SuperSocial', error])

                    throw error
                })
            )
        },
    },
}
