exports.__encode = (config, value, pretty) => {
    const eson_encoded_data = eson_encode(config, value)
    if (pretty) return JSON.stringify(eson_encoded_data, null, 4)
    return JSON.stringify(eson_encoded_data)
}

const eson_encode = (config, value) => {
    console.log("++++++++++++++++++++++++++++++++++++++++++++++++++++")
    console.log(value)
    console.log("----------------------------------------------------")
    if (Array.isArray(value)) {
        const eson_list = {}
        value.forEach((element, index) => {
            eson_list[`${index}`] = element
        })
        return {
            "__eson-list__": eson_encode(config, eson_list),
        }
    }

    const eson_data = {}
    Object.entries(value).forEach(([key, value]) => {
        let [encoded_key, encoded_value] = eson_encode_type(config, key, value)
        if (
            encoded_value &&
            (Array.isArray(encoded_value) ||
                encoded_value.constructor == Object)
        ) {
            encoded_value = eson_encode(config, encoded_value)
        }
        eson_data[encoded_key] = encoded_value
    })
    return eson_data
}

const eson_encode_type = (config, key, value) => {
    let name
    for (name in config) {
        const extension = config[name]
        if (extension.should_encode(value)) {
            const encoded_key = `${extension.name}~${key}`
            const encoded_value = extension.encode(value)
            return [encoded_key, encoded_value]
        }
    }
    return [key, value]
}
