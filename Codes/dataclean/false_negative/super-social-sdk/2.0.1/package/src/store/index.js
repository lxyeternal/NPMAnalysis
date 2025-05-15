import actions from './actions'
import getters from './getters'
import mutations from './mutations'
import state from './state'

import ticket from './modules/tickets/ticket'
import user from './modules/user/userIndex'

export default {
    namespaced: true,

    state,

    mutations,

    actions,

    getters,

    modules: {
        user,
        ticket,
    },
}
