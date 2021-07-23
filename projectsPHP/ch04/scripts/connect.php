<?php
    $servername = "50.87.143.209";
    $username = "wtfcgcmy";
    $password = "100199B1ology!";

    $conn = new mysqli($servername,$username,$password);

    if($conn->connect_error) {
        die("Connection Failed: " . $conn->connect_error);
    }
    echo "CONNECTED TO MYSQL";

    $mysqli_select_db($conn,"wtfcgcmy_WPBDL")
        or die("<p>Error selecting the database wtfcgcmy_WPBDL: " . mysqli_error($conn) . "</p>");

    echo "<p>Connected to Mysql, using database wtfcgcmy_WPBDL. </p>";
?>
