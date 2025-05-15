import { mapGetters } from 'vuex'

export default {
    computed: {
        ...mapGetters('social', ['config']),

        routeFragments() {
            return this.config.routeFragments
        },
    },
}
