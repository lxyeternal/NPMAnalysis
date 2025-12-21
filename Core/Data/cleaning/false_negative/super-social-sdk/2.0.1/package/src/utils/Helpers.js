import { isMobileLayout, respondToAbove, ScreenWidth } from '@superbet-group/web.lib.vue-utilities'
import enGB from 'date-fns/locale/en-GB'
import hr from 'date-fns/locale/hr'
import pl from 'date-fns/locale/pl'
import ro from 'date-fns/locale/ro'
import srLatn from 'date-fns/locale/sr-Latn'
import sha1 from 'sha1'

import { remapTicketStatusForClient } from '../components/chat/remapTicketStatus'

import { EventStatusAxilis, ReactionType } from './Enums'

const COLOUR_PALETTE = [
    '#07ACAE',
    '#E9BBB7',
    '#848484',
    '#FB6969',
    '#70312B',
    '#BABABA',
    '#A31C1C',
    '#244770',
    '#6D597A',
    '#5583A3',
    '#364957',
    '#F2981B',
    '#73AD21',
    '#258A54',
    '#B0866F',
]

export const getBackgroundColorByUserId = userId =>
    COLOUR_PALETTE[parseInt(sha1(userId).substring(0, 8), 16) % COLOUR_PALETTE.length]

export const datesAreOnSameDay = (first, second) =>
    first.getFullYear() === second.getFullYear() &&
    first.getMonth() === second.getMonth() &&
    first.getDate() === second.getDate()

// Factorial function.
const fact = x => {
    if (x === 0) {
        return 1
    }

    return x * fact(x - 1)
}

// Returns the binomial coefficient
// where a is the total set of possibilities
// and b is the number of combinations we're interested in
export const binomialCoefficient = (a, b) => {
    if (a < b) {
        throw Error("Total set can't be smaller than number of combinations")
    }

    const numerator = fact(a)
    const denominator = fact(a - b) * fact(b)

    return numerator / denominator
}

export const isMobile = () => isMobileLayout()

export const isDesktopWidth = () => respondToAbove(ScreenWidth.dMd)

export const isMobileUserAgent = () => {
    const toMatch = [/Android/i, /webOS/i, /iPhone/i, /iPad/i, /iPod/i, /BlackBerry/i, /Windows Phone/i]

    return toMatch.some(toMatchItem => navigator.userAgent.match(toMatchItem))
}

// eslint-disable-next-line sonarjs/cognitive-complexity
export const remapTicketForBackend = ticket => {
    const selections = ticket.events.map(event => {
        const betRadarEventId = event.externalIds?.betradar ? `br:match:${event.externalIds.betradar}` : null
        const marketId = `${event.isSpecial && event.market?.marketId ? 'S' : ''}${
            event.market?.marketId?.toString() || ''
        }`

        // because axilis sometimes has date as date and sometimes as string...
        const eventDate = event.date instanceof Date ? event.date.toISOString() : event.date

        return {
            tournament_name: '',
            team1_name: event.isSpecial ? '' : event.teamNameOne || '',
            team2_name: event.isSpecial ? '' : event.teamNameTwo || '',
            status: event.status,
            odd_name: event.odd.name,
            odd_uuid: event.odd.oddUuid,
            odd_coefficient: event.odd.coefficient,
            market_name: event.market?.name || '',
            event_id: event.eventId,
            date: eventDate.replace(/\.[0-9]{3}/, ''),
            betradar_event_id: betRadarEventId,
            market_id: marketId,
            odd_id: event.odd.oddId,
            odd_special_value: event.odd.specialValue,
            special_name: event.isSpecial ? event.teamNameOne : null,
            sport_id: event.sportId.toString(),
        }
    })

    const combinationCount = ticket.system
        ? ticket.system.selected.reduce((a, b) => a + binomialCoefficient(ticket.system.count, b), 0)
        : 1

    let cashoutCoefficient
    if (ticket.cashout) {
        const payout = ticket.cashout.value
        const potentialPayout = ticket.minPotentialWin

        cashoutCoefficient = potentialPayout ? (payout / potentialPayout) * 100 : 0
    } else {
        cashoutCoefficient = null
    }

    const betTypesSet = new Set(ticket.events.map(event => (ticket.dateReceived > event.date ? 'live' : 'pregame')))
    const betType = betTypesSet.length === 1 ? betTypesSet[0] : 'mix'

    let dateReceived
    let dateModified
    if (ticket.dateReceived) {
        dateReceived = new Date(ticket.dateReceived)

        dateReceived.setMilliseconds(0)

        dateReceived = dateReceived.toISOString().replace(/\.[0-9]{3}/, '')
    }

    if (ticket.dateLastModified) {
        dateModified = new Date(ticket.dateLastModified)

        dateModified.setMilliseconds(0)

        dateModified = dateModified.toISOString().replace(/\.[0-9]{3}/, '')
    }

    return {
        code: ticket.id,
        date_created: dateReceived,
        date_modified: dateModified || dateReceived,
        system_type: ticket.system ? 'system' : 'normal',
        coefficient: ticket.coefficient,
        combination_count: combinationCount,
        win_count: ticket.events.filter(event => event.status === EventStatusAxilis.win).length,
        lost_count: ticket.events.filter(event => event.status === EventStatusAxilis.lost).length,
        refund_count: ticket.events.filter(event => event.status === EventStatusAxilis.refund).length,
        active_count: ticket.events.filter(event => event.status === EventStatusAxilis.active).length,
        status: ticket.status,
        selections,
        shared_to_feed: true,
        cashout_coefficient: cashoutCoefficient,
        bet_type: betType,
    }
}

// eslint-disable-next-line sonarjs/cognitive-complexity
export const remapTicketForClient = ticket => {
    const selections = ticket.events.map(event => {
        const betRadarEventId = event.externalIds?.betradar ? `br:match:${event.externalIds.betradar}` : null
        const marketId = `${event.isSpecial && event.market?.marketId ? 'S' : ''}${
            event.market?.marketId?.toString() || ''
        }`

        // because axilis sometimes has date as date and sometimes as string...
        const eventDateSeconds = `${
            +new Date(event.date instanceof Date ? event.date.toISOString() : event.date) / 1000
        }`

        return {
            tournamentName: '',
            team1Name: event.isSpecial ? '' : event.teamNameOne || '',
            team2Name: event.isSpecial ? '' : event.teamNameTwo || '',
            status: event.status,
            oddName: event.odd.name,
            oddUuid: event.odd.oddUuid,
            oddCoefficient: { value: event.odd.coefficient },
            marketName: event.market?.name || '',
            eventId: event.eventId,
            date: { seconds: eventDateSeconds },
            betRadarEventId,
            marketId,
            oddId: event.odd.oddId,
            oddSpecialValue: event.odd.specialValue,
            specialName: event.isSpecial ? event.teamNameOne : null,
            sportId: { value: event.sportId.toString() },
        }
    })

    const combinationCount = ticket.system
        ? ticket.system.selected.reduce((a, b) => a + binomialCoefficient(ticket.system.count, b), 0)
        : 1

    let cashoutCoefficient
    if (ticket.cashout) {
        const payout = ticket.cashout.value
        const potentialPayout = ticket.minPotentialWin

        cashoutCoefficient = potentialPayout ? (payout / potentialPayout) * 100 : 0
    } else {
        cashoutCoefficient = null
    }

    const betTypesSet = new Set(ticket.events.map(event => (ticket.dateReceived > event.date ? 'live' : 'pregame')))
    const betType = betTypesSet.length === 1 ? betTypesSet[0] : 'mix'

    let dateReceived
    if (ticket.dateReceived) {
        dateReceived = new Date(ticket.dateReceived)

        dateReceived.setMilliseconds(0)

        dateReceived = dateReceived.toISOString().replace(/\.[0-9]{3}/, '')
    }

    return {
        ticketId: ticket.id,
        dateShared: { nanos: 0, seconds: Math.round(Date.now() / 1000).toString() },
        systemType: ticket.system ? 'system' : 'normal',
        coefficient: { value: ticket.coefficient },
        combinationCount,
        winCount: ticket.events.filter(event => event.status === EventStatusAxilis.win).length,
        lostCount: ticket.events.filter(event => event.status === EventStatusAxilis.lost).length,
        refundCount: ticket.events.filter(event => event.status === EventStatusAxilis.refund).length,
        reactions: [
            { reaction: ReactionType.REACTIONTYPE_DART, count: 0 },
            { reaction: ReactionType.REACTIONTYPE_POOP, count: 0 },
            { reaction: ReactionType.REACTIONTYPE_DISLIKE, count: 0 },
            { reaction: ReactionType.REACTIONTYPE_LIKE, count: 0 },
        ],
        currentUserDislike: false,
        currentUserLike: false,
        activeCount: ticket.events.filter(event => event.status === EventStatusAxilis.active).length,
        selections,
        sharedToFeed: true,
        ticketStatus: remapTicketStatusForClient(ticket.status),
        cashoutCoefficient,
        betType: { value: betType },
    }
}

export const getLocale = lang => {
    switch (lang) {
        case 'ro':
            return ro

        case 'hr':
            return hr

        case 'pl':
            return pl

        case 'rs':
            return srLatn

        case 'en':

        // eslint-disable-next-line no-fallthrough
        default:
            return enGB
    }
}

export const abbreviateNumber = (value, fixed = 0) => {
    const suffixes = ['', 'k', 'm', 'b', 't']

    if (value == null) {
        return null
    } // terminate early

    if (value === 0) {
        return '0'
    } // terminate early

    const precision = fixed > 0 ? fixed : 0 // number of decimal places to show

    const power = value.toPrecision(2).split('e') // get power
    const suffixIndex = power.length === 1 ? 0 : Math.floor(Math.min(power[1].slice(1), 14) / 3) // floor at decimals, ceiling at trillions
    const shortNumber =
        suffixIndex < 1 ? value.toFixed(precision) : (value / 10 ** (suffixIndex * 3)).toFixed(1 + precision) // divide by power

    const d = shortNumber < 0 ? shortNumber : Math.abs(shortNumber) // enforce -0 is 0
    // append power

    return d + suffixes[suffixIndex]
}

export const findLinks = someString => {
    const regex = /(((https?:\/\/)|(www\.))[^\s]+)/g

    return someString.match(regex)
}
