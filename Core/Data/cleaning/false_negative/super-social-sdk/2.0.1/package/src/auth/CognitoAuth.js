import axios from 'axios'

const cognitoConfig = {
    ro: {
        dev: {
            api: 'https://social-rosuperbetsport-staging.auth.eu-west-1.amazoncognito.com/oauth2/',
            clientId: '5rfd13om2b4jv6an51avd46vt6',
            region: 'eu-west-1',
            userPoolId: 'eu-west-1_AOgsNIDwI',
        },
        prod: {
            api: 'https://social-rosuperbetsport-production.auth.eu-west-1.amazoncognito.com/oauth2/',
            clientId: '74a78ae5tgt4d5qq652msu4845',
            region: 'eu-west-1',
            userPoolId: 'eu-west-1_cofL9x3sF',
        },
    },
    pl: {
        dev: {
            api: 'https://social-plsuperbetsport-staging.auth.eu-west-1.amazoncognito.com/oauth2/',
            clientId: '28rdecv30ru159vv1q197jus6q',
            region: 'eu-west-1',
            userPoolId: 'eu-west-1_x6i0pzUt6',
        },
        prod: {
            api: 'https://social-plsuperbetsport-production.auth.eu-west-1.amazoncognito.com/oauth2/',
            clientId: 'vcq788f2hfck3f0jbuchg4toq',
            region: 'eu-west-1',
            userPoolId: 'eu-west-1_a7w3bBAaU',
        },
    },
    rs: {
        dev: {
            api: 'https://social-rssuperbetsport-staging.auth.eu-west-1.amazoncognito.com/oauth2/',
            clientId: '51pj0ee41fg6v0a2gbuo0kj6p2',
            region: 'eu-west-1',
            userPoolId: 'eu-west-1_vxPboYkJ2',
        },
        prod: {
            api: 'https://social-rssuperbetsport-production.auth.eu-west-1.amazoncognito.com/oauth2/',
            clientId: '51pj0ee41fg6v0a2gbuo0kj6p2',
            region: 'eu-west-1',
            userPoolId: 'eu-west-1_vxPboYkJ2',
        },
    },
}

function defer() {
    const deferred = {}
    // eslint-disable-next-line compat/compat
    const promise = new Promise((resolve, reject) => {
        deferred.resolve = resolve

        deferred.reject = reject
    })

    deferred.promise = promise

    return deferred
}

export const initialization = defer()

const supportedCountries = ['ro', 'pl', 'rs']

export class CognitoAuth {
    constructor(options) {
        this.localStorageKeyName = 'superSocialUserToken'

        const countryConfig =
            cognitoConfig[options?.country && supportedCountries.includes(options.country) ? options.country : 'ro']

        this.config = countryConfig[options?.useProduction ? 'prod' : 'dev']
    }

    /* ===== Cognito ===== */
    // main call for cognito auth requests
    call(action, body) {
        const request = {
            url: 'https://cognito-idp.eu-west-1.amazonaws.com',
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-amz-json-1.1',
                'X-Amz-Target': action,
            },
            data: JSON.stringify(body),
            transformResponse: data => data,
        }

        return (
            axios(request)
                .then(result => JSON.parse(result.data))
                // eslint-disable-next-line promise/no-return-wrap,compat/compat
                .catch(error => Promise.reject(error))
        )
    }

    // user login to cognito
    login(user) {
        const cognitoClientId = this.config.clientId

        // try to auth the user via cognito
        return this.call('AWSCognitoIdentityProviderService.InitiateAuth', {
            ClientId: cognitoClientId,
            AuthFlow: 'CUSTOM_AUTH',
            AuthParameters: {
                USERNAME: user.userId.toString(),
            },
        }).then(response => {
            if (response.ChallengeName === 'CUSTOM_CHALLENGE') {
                return this.call('AWSCognitoIdentityProviderService.RespondToAuthChallenge', {
                    ClientId: cognitoClientId,
                    ChallengeName: response.ChallengeName,
                    ChallengeResponses: {
                        ANSWER: user.sessionId,
                        USERNAME: user.userId.toString(),
                    },
                    Session: response.Session,
                }).then(newResponse => newResponse)
            }

            return response
        })
    }

    // new user registartion
    register(user) {
        return this.call('AWSCognitoIdentityProviderService.SignUp', {
            ClientId: this.config.clientId,
            Username: user.username.toString(),
            Password: user.password,
            ValidationData: [
                {
                    Name: 'token',
                    Value: user.token,
                },
            ],
            // Not using any custom attributes at the moment
            // UserAttributes: Object.keys(AttributeList).map((key) => ({ Name: key, Value: AttributeList[key] }))
        })
    }

    refreshCredentials(refreshToken) {
        return this.call('AWSCognitoIdentityProviderService.InitiateAuth', {
            ClientId: this.config.clientId,
            AuthFlow: 'REFRESH_TOKEN_AUTH',
            AuthParameters: {
                REFRESH_TOKEN: refreshToken,
            },
        }).then(async ({ AuthenticationResult }) => ({
            AuthenticationResult: {
                ...AuthenticationResult,
                RefreshToken: AuthenticationResult.RefreshToken || refreshToken,
            },
        }))
    }
}
