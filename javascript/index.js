const { EsonDate, EsonDatetime } = require("./extensions/datetime")
const { __encode } = require("./encoder")

const global_object = () => {
    try {
        return global
    } catch (err) {}

    try {
        return window
    } catch (err) {}

    return self
}

const get_config = () => {
    return global_object().__eson_config__ || {}
}

const encode = (value, pretty) => {
    return __encode(get_config(), value, pretty)
}
exports.encode = encode

const decode = value => {}
exports.decode = decode

const add_extension = extension => {
    if (typeof extension.should_encode !== "function") {
        throw new Error("Extension must provide a function, `should_encode`")
    }
    if (typeof extension.encode !== "function") {
        throw new Error("Extension must provide a function, `encode`")
    }
    if (typeof extension.decode !== "function") {
        throw new Error("Extension must provide a function, `decode`")
    }
    if (!extension.name || typeof extension.name !== "string") {
        throw new Error(
            "Extension must provide a 'name' to identify the extension data type"
        )
    }
    const config = get_config()
    config[extension.name] = extension
    global_object().__eson_config__ = config
}

add_extension(EsonDate)
add_extension(EsonDatetime)
exports.add_extension = add_extension

module.exports = {
    encode,
    decode,
    add_extension,
}
