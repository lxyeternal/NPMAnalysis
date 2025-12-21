import { mapActions } from 'vuex'
import axios from 'axios'

import protify from '../utils/Protify'

const TEN_SECONDS = 10_000

export default {
    ...mapActions('social', ['verifyToken', 'debugLog']),

    // defaults to null, so it can be checked
    // because this mixin is used also in the provider, so it won't work there otherwise
    inject: {
        addTicket: {
            default: null,
        },
        ticketsOnSocial: {
            default: null,
        },
    },

    methods: {
        async checkTicketOnSocial(ticket) {
            const ticketDate = ticket.dateReceived ?? ticket.dateShared?.seconds
            // we assume user hasn't shared ticket to social in the first 10 seconds
            if (new Date() - ticketDate < TEN_SECONDS) {
                return false
            }

            const ticketId = ticket.id ?? ticket.ticketId ?? ticket.code

            // ticketsOnSocial is the name of injected property ticketsCache, and it is used in children, while the latter is used in the provider
            if (Object.keys(this.ticketsOnSocial ?? this.ticketsCache ?? {}).includes(ticketId)) {
                return this.ticketsOnSocial[ticketId].sharedToFeed
            }

            return this.verifyToken().then(() =>
                axios
                    .get(`${this.endpoints.baseUrl}/tickets/ticket?ticket_id=${ticketId}`, this.requestOptions.get)
                    .then(ticketProto => {
                        const protifiedTicket = protify('Ticket', ticketProto.data)

                        if (this.addTicket) {
                            this.addTicket(protifiedTicket)
                        } else if (this.addTicketToCache) {
                            this.addTicketToCache(protifiedTicket)
                        }

                        return protifiedTicket.sharedToFeed
                    })
                    // eslint-disable-next-line consistent-return
                    .catch(error => {
                        if (error.response.status === 400) {
                            return false
                        }

                        this.debugLog(['Error checking if ticket is on social', error])
                    })
            )
        },
    },
}
