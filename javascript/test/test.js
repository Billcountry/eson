const assert = require("assert")
const eson = require("../index")

describe("Test Normal JSON Operations", () => {
    it("Should encode the same way as Javascript built in JSON", () => {
        const object = {
            name: "Jane Doe",
            sibling: "John Doe",
        }
        assert.equal(eson.encode(object), JSON.stringify(object))
    })

    it("Should be able to decode JSON meant for built in JSON", () => {
        const json_data = '{"name":"Jane Doe"}'
        assert.equal(eson.decode(json_data), JSON.parse(json_data))
    })

    it("Should return pretty JSON equal to built in JSON", () => {
        const data = {
            name: "Jane Doe",
            registered: new Date(2020, 4, 7, 6, 30, 40, 400),
        }
        eson_data = {
            name: "Jane Doe",
            "EsonDatetime~registered": { timestamp: 1588822240400000 },
        }
        assert.equal(
            eson.encode(data, true),
            JSON.stringify(eson_data, null, 4)
        )
    })
})

describe("Test Datetime Operations", () => {
    it("Should decode EsonDate object to a javascript date object", () => {
        const eson_data =
            '{"EsonDate~dob": {"year": 2020, "month": 4, "day": 20}, "name": "Corona"}'
        const expected_object = {
            dob: new Date(2020, 3, 20),
            name: "Corona",
        }
        assert.equal(eson.decode(eson_data), expected_object)
    })

    it("Should encode Javascript Date object to EsonDatetime object", () => {
        const data = {
            registered: new Date(2020, 4, 7, 6, 30, 40, 400),
            username: "bear",
        }
        const expected_eson =
            '{"EsonDatetime~registered":{"timestamp":1588822240400000},"username":"bear"}'
        assert.equal(eson.encode(data), expected_eson)
    })

    it("Should decode EsonDatetime object to a javascript date object", () => {
        const eson_data =
            '{"EsonDatetime~registered": {"timestamp": 1588822240400000}, "username": "fox"}'
        const expected_object = {
            registered: new Date(2020, 4, 7, 6, 30, 40, 400),
            username: "bear",
        }
        assert.equal(eson.decode(eson_data), expected_object)
    })
})

describe("Test Combined List Data", () => {
    it("Should encode data in lists and dictionaries correctly", () => {
        const dt = new Date(2020, 4, 7, 6, 30, 40, 400)
        const data = {
            name: "Jane Doe",
            log: ["Some string", 0, dt, false, null],
        }
        const expected_eson =
            '{"name":"Jane Doe","log":["Some string",0,{"EsonDatetime~":{"timestamp":1588822240400000}},false,null]}'
        assert.equal(eson.encode(data), expected_eson)
    })

    it("Shoud decode data in lists and dictionaries correctly", () => {
        const eson_string =
            '{"name": "Jane Doe", "log": {"__eson-list__": {"0": "Some string", "1": 0, "EsonDatetime~2": {"timestamp": 1588822240400000}, "3": false, "EsonDate~4": {"year": 2020, "month": 4, "day": 20}, "5": null}}}'
        const datetime = new Date(2020, 4, 7, 6, 30, 40, 400)
        const date = new Date(2020, 3, 20)
        const expected_object = {
            name: "Jane Doe",
            log: ["Some string", 0, datetime, false, date, null],
        }
        assert.equal(eson.decode(eson_string), expected_object)
    })
})
