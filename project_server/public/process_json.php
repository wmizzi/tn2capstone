<?php include("../includes/layouts/header.php") ?>
<?php require_once("../includes/db_connection.php") ?>
<?php require_once("../includes/functions.php") ?>

<?php

	if (isset($_POST['file']))
	{
		$file_location = $_POST['file'];
	}
	else
	{
		exit("No file path entered!");
	}


	$jsondata = file_get_contents($file_location);


	// Check the file exists
	if (!file_exists($file_location))
	{

		exit("File not found");

	}

	// Convert json object to php associative array
    $data = json_decode($jsondata, true);

    $udp_download = $data['IPERF']['UDP']['download'];
    $udp_upload = $data['IPERF']['UDP']['upload'];
    $udp_jitter = $data['IPERF']['UDP']['jitter'];
    $udp_packetloss = $data['IPERF']['UDP']['packetloss'];

    $tcp_download = $data['IPERF']['TCP']['download'];
    $tcp_upload = $data['IPERF']['TCP']['upload'];

    $get_avg = $data['HTTP']['GET']['avg'];
    $get_site1 = $data['HTTP']['GET']['site1'];
    $get_site2 = $data['HTTP']['GET']['site2'];
    $get_site3 = $data['HTTP']['GET']['site3'];

    $post_avg = $data['HTTP']['POST']['avg'];
    $post_site1 = $data['HTTP']['POST']['site1'];
    $post_site2 = $data['HTTP']['POST']['site2'];
    $post_site3 = $data['HTTP']['POST']['site3'];

    $user_id = $data['UserInfo']['user id'];
    $timestamp = $data['UserInfo']['timestamp'];


    // Check whether the user's table exists
    $query = "DESCRIBE " . $user_id;

    $exists = mysqli_query($connection, $query);

    if($exists)
    {

    	$query = "INSERT INTO " . $user_id . " (";
    	$query .= "timestamp, udp_upload, udp_download, udp_jitter, udp_packetloss, tcp_download, tcp_upload, get_avg, get_site1, get_site2, get_site3, post_avg, post_site1, post_site2, post_site3"; 
    	$query .= ") VALUES (";
    	$query .= "'{$timestamp}', {$udp_upload}, {$udp_download}, {$udp_jitter}, {$udp_packetloss}, {$tcp_download}, {$tcp_upload}, {$get_avg}, {$get_site1}, {$get_site2}, {$get_site3}, {$post_avg}, {$post_site1}, {$post_site2}, {$post_site3}";
    	$query .= ")";

    	$success = mysqli_query($connection, $query);

    	if (!$success)
		{
			exit("FAILURE: Entry not added");
		}
		else
		{
			echo "Entry added successfully!";
		}
  
  		// display whether successful or not here

    } else {

    	// TO CONSIDER: Are the values going to be the same
    	// number of decimal points, etc, each time?
    	// Got to set data type accordingly
    	// Consider changing timestamp to a date data format
    	// eg. DATETIME

    	$query = "CREATE TABLE " . $user_id ." (
    		id SMALLINT NOT NULL AUTO_INCREMENT,
    		timestamp VARCHAR(16) NOT NULL,
    		udp_upload DOUBLE(16,6) NOT NULL,
    		udp_download DOUBLE(16,6) NOT NULL,
    		udp_jitter DOUBLE(16,6) NOT NULL,
    		udp_packetloss DOUBLE(16,6) NOT NULL,
    		tcp_download DOUBLE(16,6) NOT NULL,
    		tcp_upload DOUBLE(16,6) NOT NULL,
    		get_avg DOUBLE(16,6) NOT NULL,
    		get_site1 DOUBLE(16,6) NOT NULL,
    		get_site2 DOUBLE(16,6) NOT NULL,
    		get_site3 DOUBLE(16,6) NOT NULL,
    		post_avg DOUBLE(16,6) NOT NULL,
    		post_site1 DOUBLE(16,6) NOT NULL,
    		post_site2 DOUBLE(16,6) NOT NULL,
    		post_site3 DOUBLE(16,6) NOT NULL,
    		PRIMARY KEY (id)
    		);";

    	$success = mysqli_query($connection, $query);

    	if (!$success)
		{
			exit("FAILURE: Table not created");
		}
		else
		{
			echo "New user table created!";
		}

    }

?>























