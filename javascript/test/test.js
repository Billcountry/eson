const assert = require("assert")
const eson = require("../index")

describe("Test Normal JSON Operations", () => {
    it("Should encode the same way as Javascript built in JSON", () => {
        assert.equal(eson.encode(null), JSON.stringify(null))
        assert.equal(eson.encode("test"), JSON.stringify("test"))
        assert.equal(eson.encode(10), JSON.stringify(10))
        assert.equal(eson.encode(false), JSON.stringify(false))
        const object = {
            name: "Jane Doe",
            sibling: "John Doe",
        }
        assert.equal(eson.encode(object), JSON.stringify(object))
    })

    it("Should be able to decode JSON meant for built in JSON", () => {
        assert.equal(eson.decode("null"), null)
        assert.equal(eson.decode('"test"'), "test")
        assert.equal(eson.decode("10"), 10)
        assert.equal(eson.decode("false"), false)
        const json_data = '{"name":"Jane Doe"}'
        assert.deepEqual(eson.decode(json_data), JSON.parse(json_data))
    })

    it("Should return pretty JSON equal to built in JSON", () => {
        const registered = new Date(2020, 4, 7, 6, 30, 40, 400)
        const data = {
            name: "Jane Doe",
            registered,
        }
        eson_data = {
            name: "Jane Doe",
            "EsonDatetime~registered": {
                timestamp: registered.getTime() * 1000,
            },
        }
        assert.equal(
            eson.encode(data, true),
            JSON.stringify(eson_data, null, 4)
        )
    })
})

describe("Test Datetime Operations", () => {
    it("Should decode EsonDate object to a javascript date object", () => {
        const dob = new Date(2020, 3, 20)
        const eson_dob = '{"EsonDate~": {"year": 2020, "month": 4, "day": 20}}'
        assert.deepEqual(eson.decode(eson_dob), dob)
        const eson_data =
            '{"EsonDate~dob": {"year": 2020, "month": 4, "day": 20}, "name": "Corona"}'
        const expected_object = {
            dob,
            name: "Corona",
        }
        assert.deepEqual(eson.decode(eson_data), expected_object)
    })

    it("Should encode Javascript Date object to EsonDatetime object", () => {
        const registered = new Date(2020, 4, 7, 6, 30, 40, 400)
        assert.equal(
            eson.encode(registered),
            `{"EsonDatetime~":{"timestamp":${registered.getTime() * 1000}}}`
        )
        const data = {
            registered,
            username: "bear",
        }
        const expected_eson = `{"EsonDatetime~registered":{"timestamp":${registered.getTime() *
            1000}},"username":"bear"}`
        assert.equal(eson.encode(data), expected_eson)
    })

    it("Should decode EsonDatetime object to a javascript date object", () => {
        const registered = new Date(2020, 4, 7, 6, 30, 40, 400)
        const eson_registered = `{"EsonDatetime~":{"timestamp":${registered.getTime() *
            1000}}}`
        assert.deepEqual(eson.decode(eson_registered), registered)
        const eson_data = `{"EsonDatetime~registered": {"timestamp": ${registered.getTime() *
            1000}}, "username": "bear"}`
        const expected_object = {
            registered,
            username: "bear",
        }
        assert.deepEqual(eson.decode(eson_data), expected_object)
    })
})

describe("Test Combined List Data", () => {
    it("Should encode data in lists and dictionaries correctly", () => {
        const dt = new Date(2020, 4, 7, 6, 30, 40, 400)
        const data = {
            name: "Jane Doe",
            log: ["Some string", 0, dt, false, null],
        }
        const expected_eson = `{"name":"Jane Doe","log":["Some string",0,{"EsonDatetime~":{"timestamp":${dt.getTime() *
            1000}}},false,null]}`
        assert.equal(eson.encode(data), expected_eson)
    })

    it("Shoud decode data in lists and dictionaries correctly", () => {
        const datetime = new Date(2020, 4, 7, 6, 30, 40, 400)
        const eson_string = `{"name": "Jane Doe", "log": ["Some string", 0, {"EsonDatetime~": {"timestamp": ${datetime.getTime() *
            1000}}}, false, {"EsonDate~": {"year": 2020, "month": 4, "day": 20}}, null]}`
        const date = new Date(2020, 3, 20)
        const expected_object = {
            name: "Jane Doe",
            log: ["Some string", 0, datetime, false, date, null],
        }
        assert.deepEqual(eson.decode(eson_string), expected_object)
    })
})
