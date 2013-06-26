<?php
$message = '<html><body>';
$message .= '<img src="/Dropbox_sites/Dropbox_sites/imageServertmp/images/images_jpg_PhotoSelects/3151/315111401/315111401_1.jpg" alt="Test Image Display" width="200" />';
$message .= '<table rules="all" style="border-color: #666;" cellpadding="10">';
$message .= "<tr style='background: #eee;'><td><strong>Merchant Name:</strong> </td><td>" . strip_tags($_POST['req-name']) . "</td></tr>";
$message .= "<tr><td><strong>Email:</strong> </td><td>" . strip_tags($_POST['req-email']) . "</td></tr>";
$message .= "<tr><td><strong>Style:</strong> </td><td>" . strip_tags($_POST['style']) . "</td></tr>";
$message .= "<tr><td><strong>Brand:</strong> </td><td>" . strip_tags($_POST['brand']) . "</td></tr>";
$message .= "<tr><td><strong>Shot Date (main):</strong> </td><td>" . $_POST['shotdate'] . "</td></tr>";
$message .= "<tr><td><strong>URL To Change (main):</strong> </td><td>" . $_POST['URL-main'] . "</td></tr>";
$addURLS = $_POST['addURLS'];
if (($addURLS) != '') {
    $message .= "<tr><td><strong>URL To Change (additional):</strong> </td><td>" . strip_tags($addURLS) . "</td></tr>";
}
$curText = htmlentities($_POST['curText']);           
if (($curText) != '') {
    $message .= "<tr><td><strong>CURRENT Content:</strong> </td><td>" . $curText . "</td></tr>";
}
$message .= "<tr><td><strong>NEW Content:</strong> </td><td>" . htmlentities($_POST['newText']) . "</td></tr>";
$message .= "</table>";
$message .= "</body></html>";

echo($message);
?>