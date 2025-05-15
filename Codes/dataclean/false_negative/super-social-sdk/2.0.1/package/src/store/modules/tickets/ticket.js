export const ADD_TICKET = 'ADD_TICKET'

export default {
    namespaced: true,

    state: {
        tickets: [],
    },

    mutations: {
        [ADD_TICKET]: (state, ticket) => {
            const isTicketCached = state.tickets.some(ticketItem => ticketItem.ticketId === ticket.ticketId)

            if (!isTicketCached) {
                state.tickets.push(ticket)
            }
        },
    },

    getters: {
        tickets(state) {
            return state.tickets
        },
    },

    actions: {
        addTicket({ commit }, ticket) {
            commit(ADD_TICKET, ticket)
        },
    },
}
