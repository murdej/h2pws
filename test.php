<?php

$ch = curl_init();

curl_setopt($ch, CURLOPT_URL,            "http://localhost:8000/" );
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1 );
curl_setopt($ch, CURLOPT_POST,           1 );
curl_setopt($ch, CURLOPT_POSTFIELDS,     "<html><h1>fooo</h1><p>dfscvsdf asdcasd casssvsv adwed ADSASd</p></html>" ); 
curl_setopt($ch, CURLOPT_HTTPHEADER,     array('Content-Type: text/plain')); 

echo curl_exec ($ch);