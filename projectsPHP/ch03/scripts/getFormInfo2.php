<?php
    $file_cabinet['first_name'] = "Derek";
    $file_cabinet['last_name'] = "Chauvin";
    $file_cabinet['email'] = "Derek@gmail.com";
    $file_cabinet['facebook'] = "http://www.facebook.com/DerekTrucks";
    $file_cabinet['twitter'] = "@derekandsusan";

    $first_name = $file_cabinet['first_name'];
    $last_name = $file_cabinet['last_name'];
    $email = $file_cabinet['email'];
    $facebook = $file_cabinet['facebook'];
    $twitter = $file_cabinet['twitter'];

    echo $first_name . " " . $last_name;
    echo "\nEmail: " . $email;
    echo "\nFacebook: " . $facebook;
    echo "\nTwitter: " . $twitter;
?>