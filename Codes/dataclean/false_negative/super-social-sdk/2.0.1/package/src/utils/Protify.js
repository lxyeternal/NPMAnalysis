import protobuf from 'protobufjs'

import protoSchema from '../proto/social-proto.json'

const decodingOptions = {
    longs: String,
    defaults: true, // includes default values
    arrays: true, // populates empty arrays (repeated fields) even if defaults=false
    objects: true, // populates empty objects (map fields) even if defaults=false
    oneofs: true, // includes virtual oneof fields set to the present field's name
}

/**
 * Returns a new array buffer based on a provided bas64 string
 * @param {String} str - Base64 encoded string
 */
function convertBase64ToArrayBuffer(str) {
    const arrayToDecode = protobuf.util.newBuffer(protobuf.util.base64.length(str))
    protobuf.util.base64.decode(str, arrayToDecode, 0)

    return arrayToDecode
}

/**
 * Returns a decoded object from a proto binary
 * @param {String} lookupModel - Model name which we use to decode the message
 * @param {ArrayBuffer, String} message - Binary API response to decode with the proto schema
 */
// eslint-disable-next-line func-names
export default function (lookupModel, message) {
    const root = protobuf.Root.fromJSON(protoSchema)
    const protoModel = root.lookupType(lookupModel)

    // eslint-disable-next-line compat/compat
    const arrayToDecode = typeof message === 'string' ? convertBase64ToArrayBuffer(message) : new Uint8Array(message)

    const decoded = protoModel.decode(arrayToDecode)

    return protoModel.toObject(decoded, decodingOptions)
}
