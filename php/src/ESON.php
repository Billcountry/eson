<?php

/**
 * Class ESON
 * @package ESON
 */
class ESON
{
    public static function encode($data, $pretty = FALSE)
    {
        $eson_data = self::encode_types($data);
        if ($pretty) {
            return json_encode($eson_data, JSON_PRETTY_PRINT);
        }
        return json_encode($eson_data);
    }

    private static function encode_types($data)
    {
        if (is_array($data) && self::is_assoc($data)) {
            $eson_array = array();
            foreach ($data as $key => $value) {
                extract(self::encode_type($key, $value));
                $eson_array[$encoded_key] = $encoded_value;
            }
            return $eson_array;
        }
        if (is_array($data)) {
            $eson_array = array();
            foreach ($data as $value) {
                extract(self::encode_type("", $value));
                if ($encoded_key) {
                    array_push($eson_array, array($encoded_key => $encoded_value));
                } else {
                    array_push($eson_array, $encoded_value);
                }
            }
            return $eson_array;
        }
        extract(self::encode_type("", $data));
        if ($encoded_key) {
            return array($encoded_key => $encoded_value);
        }
        return $data;
    }

    private static function encode_type($key, $value)
    {
        $config = self::config();
        $encoded_key = $key;
        $encoded_value = $value;
        foreach ($config as $name => $extension) {
            if ($extension["should_encode"]($value)) {
                $encoded_key = "$name~$key";
                $encoded_value = $extension["encode"]($value);
                break;
            }
        }
        if(is_array($encoded_value)){
            $encoded_value = self::encode_types($encoded_value);
        }
        return array("encoded_key" => $encoded_key, "encoded_value" => $encoded_value);
    }

    public static function decode($eson_string)
    {
        $eson_data = json_decode($eson_string, true);
        return self::decode_types($eson_data);
    }

    private static function decode_types($data)
    {
        if(is_array($data) && self::is_assoc($data)){
            $eson_array = array();
            foreach($data as $encoded_key => $encoded_value){
                extract(self::decode_type($encoded_key, $encoded_value));
                if(is_array($value)){
                    $value = self::decode_types($value);
                }
                if(!$key){
                    return $value;
                }
                $eson_array[$key] = $value;
            }
            return $eson_array;
        }
        if(is_array($data)){
            $eson_array = array();
            foreach($data as $value){
                if(is_array($value)){
                    $value = self::decode_types($value);
                }
                array_push($eson_array, $value);
            }
            return $eson_array;
        }
        return $data;
    }

    private static function decode_type($encoded_key, $encoded_value){
        $key_parts = explode("~", $encoded_key);
        $config = self::config();
        if(count($key_parts) == 2 && isset($config[$key_parts[0]]) ){
            return array(
                "key" => $key_parts[1],
                "value" => $config[$key_parts[0]]["decode"]($encoded_value)
            );
        }
        return array("key" => $encoded_key, "value" => $encoded_value);
    }

    public static function add_extension(array $extension)
    {
        if (!isset($extension["name"])
            || !isset($extension["encode"])
            || !isset($extension["decode"])
            || !isset($extension["should_encode"])) {

            throw new Exception("An eson extension must provide the following"
                . " 'name'->string,"
                . " 'encode'->function,"
                . " 'decode'->function,"
                . " 'should_encode'->function"
            );
        }

        $config = self::config();
        $config[$extension["name"]] = $extension;
        $GLOBALS['_ESON_CONFIG'] = $config;
    }

    private static function is_assoc($array)
    {
        return array_keys($array) !== range(0, count($array) - 1);
    }

    private static function config()
    {
        if (!isset($GLOBALS['_ESON_CONFIG'])) {
            $GLOBALS['_ESON_CONFIG'] = array();
            // Add default extensions
            self::add_extension(array(
                "name" => "EsonDatetime",
                "should_encode" => function ($value) {
                    return $value instanceof DateTime;
                },
                "encode" => function ($value) {
                    return array("timestamp" => $value->getTimestamp() * 1000000);
                },
                "decode" => function ($value) {
                    $ts = $value["timestamp"];
                    $dt = new DateTime();
                    $dt->setTimestamp(intval($ts / 1000000));
                    return $dt;
                }
            ));
            self::add_extension(array(
                "name" => "EsonDate",
                // Should only decode not encode
                "should_encode" => function ($value) {
                    return false;
                },
                "encode" => true,
                "decode" => function ($value) {
                    $day = $value["day"];
                    $month = $value["month"];
                    $year = $value["year"];
                    return new DateTime("$day-$month-$year");
                }
            ));
        }
        return $GLOBALS['_ESON_CONFIG'];
    }
}
