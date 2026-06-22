<?php 
$conn = oci_connect('VSREDDY','admin','localhost/XE');
if(!$conn)
{
	echo "Database Connection Error";
}
else{
	//echo "<center>Connection Success</center>";
}

?>