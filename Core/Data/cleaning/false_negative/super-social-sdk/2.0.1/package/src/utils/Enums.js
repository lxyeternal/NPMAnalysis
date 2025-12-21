import socialProto from '../proto/social-proto.json'

const CommentMediaType = socialProto.nested.CommentMediaType.values
const CommentStatus = socialProto.nested.CommentStatus.values
const ErrorType = socialProto.nested.ErrorType.values
const FeatureFlagQuestionType = socialProto.nested.FeatureFlagQuestionType.values
const NotificationType = socialProto.nested.NotificationType.values
const ReactionType = socialProto.nested.ReactionType.values
const RoomPromotionType = socialProto.nested.RoomPromotionType.values
const SelectionStatus = socialProto.nested.SelectionStatus.values
const TicketStatus = socialProto.nested.TicketStatus.values
const TicketSystemType = socialProto.nested.TicketSystemType.values
const UserType = socialProto.nested.UserType.values

const TicketStatusAxilis = {
    active: 'active',
    canceled: 'canceled',
    lost: 'lost',
    obsolete: 'obsolete',
    payed: 'payed',
    refund: 'refund',
    win: 'win',
    cashedOut: 'cashedOut',
}

const EventStatusAxilis = {
    active: 'active',
    lost: 'lost',
    win: 'win',
    refund: 'refund',
}

const EventTypeAxilis = {
    live: 'live',
}

const SplitChatType = {
    singleMatch: 'single_match',
    allMatches: 'all_matches',
}

const SocialRouteNames = {
    social: 'Social',
    ticketFeed: 'Ticket Feed',
    ticketDetails: 'Ticket Details',
    socialProfile: 'Social Profile',
    myFollowers: 'My Followers',
    userProfile: 'User Profile',
    userFollowers: 'User Followers',
    userTicket: 'User Ticket',
}

const NotificationGroupType = {
    new: 'new',
    seen: 'seen',
    pinned: 'pinned',
    bucket: 'bucket',
}

const MobileSocialTabs = {
    superSocial: 'SuperSocial',
    myProfile: 'My Profile',
}

const BucketListType = {
    newFollowers: 'new_followers',
    followRequests: 'follow_requests',
    winningTickets: 'winning_tickets',
}

export {
    CommentMediaType,
    CommentStatus,
    ErrorType,
    FeatureFlagQuestionType,
    NotificationType,
    ReactionType,
    RoomPromotionType,
    SelectionStatus,
    TicketStatus,
    TicketSystemType,
    UserType,
    TicketStatusAxilis,
    EventStatusAxilis,
    SplitChatType,
    SocialRouteNames,
    NotificationGroupType,
    EventTypeAxilis,
    MobileSocialTabs,
    BucketListType,
}
