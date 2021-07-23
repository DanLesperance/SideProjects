<?php
$FirstName = trim($_REQUEST['first_name']);
$LastName =  trim($_REQUEST['last_name']);
$EmailAddress =  trim($_REQUEST['email']);
$FacebookURL =  str_replace("facebook.org", "facebook.com", trim($_REQUEST['facebook_url']));
$position = strpos($FacebookURL, "facebook.com");
if ($position === false) {
    $FacebookURL = "http://www.facebook.com/" . $FacebookURL;
}
$TwitterHandle =  trim($_REQUEST['twitter_handle']);
$twitter_url = "http://www.twitter.com/";
$twitter_pos = strpos($TwitterHandle, "@");
if ($twitter_pos === false) {
    $twitter_url = $twitter_url . $TwitterHandle;
} else {
    $twitter_url = $twitter_url . substr($TwitterHandle, $twitter_pos + 1);
}
?>


<html>
    <head>
        <link href="../css/phpMM.css" rel="StyleSheet" type="text/css" />
    </head>
    <body>
        <div id="header"><h1>PHP & MYSQL: THE MISSING MANUAL</h1></div>
        <div id="example">EXAMPLE -1</div>

        <div id="content">
            <h1> Record of what you submitted</h1>
            <p>
                Name: <?php echo $FirstName . " " . $LastName; ?><br />
                Email Address: <?php echo $EmailAddress; ?><br />
                <a href="<?php echo $FacebookURL; ?>">Your facebook page</a><br />
                <a href="<?php echo $twitter_url; ?>">Your Twitter page</a><br />
            </p>
        </div>
    <div id="footer"></div>
    </body>
</html>