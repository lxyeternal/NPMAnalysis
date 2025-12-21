import { mapGetters } from 'vuex'

export default {
    computed: {
        ...mapGetters('social', ['ctSessionToken', 'socialSessionToken', 'config']),
        sessionTokens() {
            return {
                ct: this.ctSessionToken,
                social: this.socialSessionToken,
            }
        },

        endpoints() {
            return this.config.api
        },

        requestOptions() {
            const defaultHeaders = {
                Accept: 'application/protobuf',
                authentication: this.sessionTokens.social.AccessToken,
                'sa-client-id': this.sessionTokens.ct.userId,
            }

            return {
                get: {
                    headers: defaultHeaders,
                    responseType: 'arraybuffer',
                },

                post: {
                    ...defaultHeaders,
                    'Content-Type': 'application/json',
                },

                register: {
                    headers: {
                        ...defaultHeaders,
                        'Content-Type': 'multipart/form-data',
                    },
                    responseType: 'arraybuffer',
                },
            }
        },
    },
}
