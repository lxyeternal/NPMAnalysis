import { TicketStatus, TicketStatusAxilis } from '../../utils/Enums'

export const remapTicketStatus = ticketStatus => {
    switch (ticketStatus) {
        case TicketStatus.TICKETSTATUS_ACTIVE:
            return TicketStatusAxilis.active

        case TicketStatus.TICKETSTATUS_CANCELED:
            return TicketStatusAxilis.canceled

        case TicketStatus.TICKETSTATUS_LOST:
            return TicketStatusAxilis.lost

        case TicketStatus.TICKETSTATUS_OBSOLETE:
            return TicketStatusAxilis.obsolete

        case TicketStatus.TICKETSTATUS_PAYED:
            return TicketStatusAxilis.payed

        case TicketStatus.TICKETSTATUS_REFUND:
            return TicketStatusAxilis.refund

        case TicketStatus.TICKETSTATUS_WIN:
            return TicketStatusAxilis.win

        case TicketStatus.TICKETSTATUS_CASHED_OUT:
            return TicketStatusAxilis.cashedOut

        default:
            return 'unknown'
    }
}

export const remapTicketStatusForClient = status => {
    switch (status) {
        case TicketStatusAxilis.active:
            return TicketStatus.TICKETSTATUS_ACTIVE

        case TicketStatusAxilis.canceled:
            return TicketStatus.TICKETSTATUS_CANCELED

        case TicketStatusAxilis.lost:
            return TicketStatus.TICKETSTATUS_LOST

        case TicketStatusAxilis.obsolete:
            return TicketStatus.TICKETSTATUS_OBSOLETE

        case TicketStatusAxilis.payed:
            return TicketStatus.TICKETSTATUS_PAYED

        case TicketStatusAxilis.refund:
            return TicketStatus.TICKETSTATUS_REFUND

        case TicketStatusAxilis.win:
            return TicketStatus.TICKETSTATUS_WIN

        case TicketStatusAxilis.cashedOut:
            return TicketStatus.TICKETSTATUS_CASHED_OUT

        default:
            return TicketStatus.TICKETSTATUS_UNKNOWN
    }
}
