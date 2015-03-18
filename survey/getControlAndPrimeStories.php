<?php

error_reporting(E_ALL);
ini_set("display_errors", 1);

require_once '_db.php';

$dbh = getDatabaseHandle();

if ($dbh) {
	try{
		$query = $dbh->prepare('SELECT step6_response from all_control');
		$query->execute();
		$control_stories = $query->fetchAll(PDO::FETCH_ASSOC);

		$query = $dbh->prepare('SELECT step6_response from all_primed');
		$query->execute();
		$prime_stories = $query->fetchAll(PDO::FETCH_ASSOC);

		echo json_encode( array_merge($control_stories, $prime_stories) );

	} catch(PDOException $e) {
		echo 'ERROR: ' . $e->getMessage();
	}
}

?>