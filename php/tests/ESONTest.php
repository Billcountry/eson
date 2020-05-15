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
}
