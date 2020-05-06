const encode = (value, pretty) => {
    return JSON.stringify(value)
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
exports.add_extension = add_extension

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
    global_object().__eson_config__ || {}
}

module.exports = {
    encode,
    decode,
    add_extension,
}
