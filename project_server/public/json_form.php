<?php include("../includes/layouts/header.php") ?>
<?php require_once("../includes/db_connection.php") ?>
<?php require_once("../includes/functions.php") ?>


<form method = "POST" action = "process_json.php">

	What is the path to the file?
	data/0xa434d9c0e3faL14-11_02-03-17.json

	<input type = "text" name = "file">
	<input type = "submit">

</form>

<?php include("../includes/layouts/footer.php") ?>