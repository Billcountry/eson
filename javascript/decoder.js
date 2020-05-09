exports.__decode = (config, value) => {
    const eson_data = JSON.parse(value)
    return decode_eson_data(config, eson_data)
}

const decode_eson_data = (config, data) => {
    if (data && data.constructor === Object) {
        const _data = {}
        let encoded_key
        let encoded_value
        for (encoded_key in data) {
            encoded_value = data[encoded_key]
            let [key, value] = decode_value(config, encoded_key, encoded_value)
            if (
                value &&
                (Array.isArray(value) || value.constructor == Object)
            ) {
                encoded_value = decode_eson_data(config, encoded_value)
            }
            if (!key) return value
            _data[key] = value
        }
        return _data
    }

    if (Array.isArray(data)) {
        return data.map(value => {
            if (
                value &&
                (Array.isArray(value) || value.constructor == Object)
            ) {
                value = decode_eson_data(config, value)
            }
            return value
        })
    }
    return data
}

const decode_value = (config, encoded_key, encoded_value) => {
    const key_parts = encoded_key.split("~")
    if (key_parts.length !== 2) return [encoded_key, encoded_value]
    const [name, key] = key_parts
    const extension = config[name]
    if (extension) return [key, extension.decode(encoded_value)]
    console.warn(`Missing ESON extension ${name}`)
    return [encoded_key, encoded_value]
}
