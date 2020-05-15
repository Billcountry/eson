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

}
