<?php
ini_set("display_errors", "1");
error_reporting(E_ALL);

require_once( __DIR__ . '/../../../vendor/simpletest/simpletest/autorun.php');

class AllTests extends TestSuite {
    function __construct() {
        parent::__construct();
        $this->addFile('altitud_test.php');
        $this->addFile('api_rest_test.php');
    }
}
?>