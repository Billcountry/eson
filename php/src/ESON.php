<?php
/**
 * Class ESON
 * @package ESON
 */
class ESON
{
    public static function encode($data, $pretty=FALSE){
        $eson_data = self::encode_types($data);
        if($pretty){
            return json_encode($data, JSON_PRETTY_PRINT);
        }
        return json_encode($data);
    }

    private static function encode_types($data){
        if(is_array($data) && self::is_assoc($data)){
            $eson_array = array();
            foreach ($data as $key => $value) {
                $result = self::encode_type($key, $value);
                $encoded_key = $result["encoded_key"];
                $encoded_value = $result["encoded_value"];
                if(is_array($encoded_value)){
                    $encoded_value = self::encode_types($data);
                }
                $eson_array[$encoded_key] = $encoded_value;
            }
            return $eson_array;
        }
        if(is_array($data)){
            $eson_array = array();
            foreach($data as $value){
                $result = self::encode_type("", $value);
                $encoded_key = $result["encoded_key"];
                $encoded_value = $result["encoded_value"];
                if(is_array($encoded_value)){
                    $encoded_value = self::encode_types($data);
                }
                if($encoded_key){
                    array_push($eson_array, array($encoded_key => $encoded_value));
                }else{
                    array_push($eson_array, $encoded_value);
                }
            }
            return $eson_array;
        }
        $result = self::encode_type("", $data);
        $encoded_key = $result["encoded_key"];
        $encoded_value = $result["encoded_value"];
        if(is_array($encoded_value)){
            $encoded_value = self::encode_types($data);
        }
        if($encoded_key){
            return array($encoded_key => $encoded_value);
        }
        return $data;
    }

    private static function encode_type($key, $value){
        $config = self::config();
        foreach ($config as $name => $extension){
            if($extension["should_encode"]($value)){
                return array(
                    "encoded_key" => "$name~$key",
                    "encoded_value" => $extension["encode"]($value)
                );
            }
        }
        return array("encoded_key" => $key, "encoded_value" => $value);
    }

    public static function decode($eson_string){
        return json_decode($eson_string, true);
    }

    public static function add_extension(array $extension){
        if(!isset($extension["name"])
            || !isset($extension["encode"])
            || !isset($extension["decode"])
            || !isset($extension["should_encode"])){

            throw new Exception("An eson extension must provide the following"
                                ." 'name'->string,"
                                ." 'encode'->function,"
                                ." 'decode'->function,"
                                ." 'should_encode'->function"
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

    private static function config(){
        return $GLOBALS['_ESON_CONFIG'];
    }
}

if(!isset($_ESON_CONFIG)){
    $_ESON_CONFIG = array();
    // Add default extensions
    ESON::add_extension(array(
        "name" => "DateTime",
        "should_encode" => function($value){
            return $value instanceof DateTime;
        },
        "encode" => function($value){
            return array("timestamp" => $value->getTimestamp() * 1000000);
        },
        "decode" => function($value){
            $ts = $value["timestamp"];
            $dt = new DateTime();
            $dt->setTimestamp(intval($ts/1000000));
            return $dt;
        }
    ));
    ESON::add_extension(array(
        "name" => "Date",
        // Should only decode not encode
        "should_encode" => function($value){
            return false;
        },
        "encode" => null,
        "decode" => function($value){
            $day = $value["day"];
            $month = $value["month"];
            $year = $value["year"];
            return new DateTime("$day-$month-$year");
        }
    ));
}
