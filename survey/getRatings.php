<?php

error_reporting(E_ALL);
ini_set("display_errors", 1);

require_once '_db.php';

$dbh = getDatabaseHandle();

if ($dbh) {
	try{
		$query = $dbh->prepare('SELECT ratings from survey');
		$query->execute();
		$ratings = $query->fetchAll(PDO::FETCH_ASSOC);

		echo json_encode( $ratings );

	} catch(PDOException $e) {
		echo 'ERROR: ' . $e->getMessage();
	}
}

?>