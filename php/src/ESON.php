<?php

if(!isset($_ESON_CONFIG)){
    $_ESON_CONFIG = array();
}


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
        return json_encode($eson_data);
    }

    private static encode_types($data){
        if(is_array($data) && self::is_assoc($data)){
            $eson_array = array();
            foreach ($data as $key => $value) {
                
            }
        }
    }

    private static encode_type($value){
        
    }

    public static function decode(string $eson_data){

    }

    public static function add_extension(array $extension){
        if(!isset($extension["name"])
            || !isset($extension["encode"])
            || !isset($extension["decode"])
            || !isset($extension["name"])){

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

    private static function is_assoc($array)[
        return array_keys($array) !== range(0, count($array) - 1);
    ]

    private static function config(){
        global $_ESON_CONFIG;
    }
}