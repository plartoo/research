<?php
error_reporting(E_ALL);
ini_set("display_errors", 1);

require_once '_db.php';

$gender = $_REQUEST['gender'];
$name = $_REQUEST['name'];
$grade = $_REQUEST['grade'];
$ratings = $_REQUEST['ratings'];

$dbh = getDatabaseHandle();

if($dbh) {
	try{
		$query = $dbh->prepare('INSERT INTO survey (name, gender, grade, ratings) VALUES (:name, :gender, :grade, :ratings)');

		$dbh->beginTransaction();
		$query->execute( array('gender' => $gender, 'name' => $name, 'grade' => $grade, 'ratings' => $ratings) );
		echo $dbh->lastInsertId();
		$dbh->commit();

	} catch(PDOException $e) {
		$dbh->rollback(); 
		echo 'ERROR: ' . $e->getMessage();
	}
}
?>
