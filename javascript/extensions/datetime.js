exports.EsonDatetime = {
    name: "EsonDatetime",
    should_encode: value => value instanceof Date,
    encode: value => {
        // ESON processes datetime in micro-seconds
        return {
            timestamp: value.getTime() * 1000,
        }
    },
    decode: value => new Date(value.timestamp / 1000),
}

exports.EsonDate = {
    name: "EsonDate",
    // Javascript doesn't support separation of date and datetime
    should_encode: () => false,
    encode: () => null,
    decode: value => {
        return new Date(value.year, value.month - 1, value.day)
    },
}
