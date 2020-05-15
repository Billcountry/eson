<?php

use PHPUnit\Framework\TestCase;

final class ESONTest extends TestCase
{
    public function test_simple_encode()
    {
        $assoc_array = array("name" => "Jane Doe", "sibling" => "John Doe");
        $arr = [1, 2, 3];
        $this->assertEquals(json_encode($assoc_array), ESON::encode($assoc_array));
        $this->assertEquals(json_encode($arr), ESON::encode($arr));
        $this->assertEquals('null', ESON::encode(null));
    }

    public function test_simple_decode()
    {
        $json_assoc = '{"name": "Jane Doe"}';
        $expected_result = array("name" => "Jane Doe");
        $this->assertEquals($expected_result, ESON::decode($json_assoc));
        $json_array = '[1,2,"string",5]';
        $expected_result = [1, 2, "string", 5];
        $this->assertEquals($expected_result, ESON::decode($json_array));
        $this->assertNull(ESON::decode('null'));
    }

    public function test_date_decode()
    {
        $eson_date = '{"EsonDate~": {"year": 2020, "month": 4, "day": 20}}';
        $expected_date = new DateTime("20-04-2020");
        $this->assertEquals($expected_date, ESON::decode($eson_date));

        $eson_object = '{"EsonDate~dob": {"year": 2020, "month": 4, "day": 20}, "name": "Corona"}';
        $expected_object = array("dob" => new DateTime("20-04-2020"), "name" => "Corona");
        $this->assertEquals($expected_object, ESON::decode($eson_object));
    }

    public function test_date_time_encode()
    {
        $dt = new DateTime('2020-05-07T06:30:40.0004Z');
        $data = array("registered" => $dt, "username" => "bear");
        $expected_ts = $dt->getTimestamp() * 1000000;
        $expected_eson = sprintf('{"EsonDatetime~registered":{"timestamp":%u},"username":"bear"}', $expected_ts);
        $this->assertEquals($expected_eson, ESON::encode($data));
    }

    public function test_date_time_decode()
    {
        $eson_data = '{"EsonDatetime~date_of_birth": {"timestamp": 1588822240000000}, "horoscope": "taurus"}';
        $dt = new DateTime();
        $dt->setTimestamp(1588822240);
        $expected_data = array("date_of_birth" => $dt, "horoscope" => "taurus");
        $this->assertEquals($expected_data, ESON::decode($eson_data));
    }

    public function test_combined_list_data_encode()
    {
        $dt = new DateTime('2020-05-07T06:30:40.0004Z');
        $expected_ts = $dt->getTimestamp() * 1000000;
        $data = array("name"=>"Jane Doe", "log"=>["Some String", 0, $dt, false, null]);
        $expected_eson = sprintf(
            '{"name":"Jane Doe","log":["Some String",0,{"EsonDatetime~":{"timestamp":%u}},false,null]}',
            $expected_ts);
        $this->assertEquals($expected_eson, ESON::encode($data));
    }

    public function test_combined_list_data_decode()
    {
        $datetime = new DateTime('2020-05-07T06:30:40.0004Z');
        $expected_ts = $datetime->getTimestamp() * 1000000;
        $eson_string = sprintf(
            '{"name": "Jane Doe", "log": ["Some string", 0, {"EsonDatetime~": {"timestamp": %u}}, false, {"EsonDate~": {"year": 2020, "month": 4, "day": 20}}, null]}',
            $expected_ts
        );
        $date = new DateTime("20-04-2020");
        $expected_data = array(
            "name" => "Jane Doe",
            "log" => array(
                "Some string",
                0,
                $datetime,
                false,
                $date,
                null
            )
        );
        $this->assertEquals($expected_data, ESON::decode($eson_string));
    }
}
