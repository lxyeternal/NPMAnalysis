// TYPES
import axios from 'axios'

import protify from '../../../utils/Protify'

import { DEBUG_LOG, SET_IS_LOADING_TOKENS } from '../../types'

const acceptHeader = 'application/protobuf'
const verifyTokenAction = 'social/verifyToken'
const debugLogMutation = `social/${DEBUG_LOG}`

export const SET_USER = 'SET_USER'
export const SET_USER_CONFIG = 'SET_USER_CONFIG'
export const SET_USER_DATA = 'SET_USER_DATA'
export const SET_USER_PROFILE = 'SET_USER_PROFILE'
export const SET_USER_FOLLOWS = 'SET_USER_FOLLOWS'
export const CLEAR_USER_FOLLOWS = 'CLEAR_USER_FOLLOWS'

export default {
    namespaced: true,

    state: {
        user: null,
        userConfig: null,
        userData: null,
        userProfile: null,
        userFollows: null,
    },

    mutations: {
        [SET_USER]: (state, user) => {
            state.user = user
        },

        [SET_USER_CONFIG]: (state, userConfig) => {
            state.userConfig = userConfig
        },

        [SET_USER_DATA]: (state, userData) => {
            state.userData = userData
        },

        [SET_USER_PROFILE]: (state, userProfile) => {
            state.userProfile = userProfile
        },

        [SET_USER_FOLLOWS]: (state, userFollows) => {
            if (state.userFollows) {
                state.userFollows.pendingRequests = [
                    ...new Set([...state.userFollows.pendingRequests, ...userFollows.pendingRequests]),
                ]

                state.userFollows.followRequests = [
                    ...new Set([...userFollows.followRequests, ...state.userFollows.followRequests]),
                ]

                state.userFollows.followers = [...new Set([...state.userFollows.followers, ...userFollows.followers])]

                state.userFollows.following = [...new Set([...state.userFollows.following, ...userFollows.following])]
            } else {
                state.userFollows = userFollows
            }
        },

        [CLEAR_USER_FOLLOWS]: state => {
            state.userFollows = null
        },
    },

    getters: {
        user(state) {
            return state.user
        },

        userConfig(state) {
            return state.userConfig
        },

        userData(state) {
            return state.userData
        },

        userProfile(state) {
            return state.userProfile ?? state.user
        },

        userFollows(state) {
            return state.userFollows
        },
    },

    actions: {
        setUserProfile({ commit }, user) {
            commit(SET_USER_PROFILE, user)
        },

        incrementUserFollowers({ state }) {
            state.user.followers += 1
        },

        decrementUserFollowers({ state }) {
            state.user.followers -= 1
        },

        incrementUserFollowings({ state }) {
            state.user.following += 1
        },

        decrementUserFollowings({ state }) {
            state.user.following -= 1
        },

        setUserFollows({ commit }, userFollows) {
            commit(SET_USER_FOLLOWS, userFollows)
        },

        fetchUser({ commit, dispatch, rootState }) {
            const url = `${rootState.social.config.api.baseUrl}/user/profile`

            return dispatch(verifyTokenAction, null, { root: true }).then(() =>
                axios
                    .get(url, {
                        headers: {
                            Accept: acceptHeader,
                            authentication: rootState.social.socialSessionToken.AccessToken,
                            'sa-client-id': rootState.social.ctSessionToken.userId,
                        },
                        responseType: 'arraybuffer',
                    })
                    .then(response => {
                        commit(SET_USER, protify('User', response.data))

                        commit(`social/${SET_IS_LOADING_TOKENS}`, false, { root: true })
                    })
                    .catch(error => {
                        commit(debugLogMutation, ['Error fetching user info', error], { root: true })

                        throw error
                    })
            )
        },

        fetchUserConfig({ rootState, commit, dispatch }) {
            const url = `${rootState.social.config.api.baseUrl}/config/default`

            // eslint-disable-next-line promise/catch-or-return
            dispatch(verifyTokenAction, null, { root: true }).then(() => {
                axios
                    .get(url, {
                        headers: {
                            Accept: acceptHeader,
                            authentication: rootState.social.socialSessionToken.AccessToken,
                            'sa-client-id': rootState.social.ctSessionToken.userId,
                        },
                        responseType: 'arraybuffer',
                    })
                    .then(response => {
                        commit(SET_USER_CONFIG, protify('UserConfig', response.data))
                    })
                    .catch(error => {
                        commit(debugLogMutation, ['Error fetching user config', error], { root: true })
                    })
            })
        },

        setUser({ commit }, user) {
            commit(SET_USER, user)
        },

        setUserData({ commit }, userData) {
            commit(SET_USER_DATA, userData)
        },

        removeUserData({ commit }) {
            commit(SET_USER_DATA, null)
        },
    },
}
