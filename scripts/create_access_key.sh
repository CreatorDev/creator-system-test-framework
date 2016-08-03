#!/bin/bash
#
# create a client access key/secret pair for accessing the device server using the REST API
#
##

if [ ! -z $1 ] 
then
     WEBSERVICE=$1
else
     WEBSERVICE=http://localhost:8080
fi

if [ ! -z $2 ] 
then
     ORGANISATION0_KEY=$2
else
     ORGANISATION0_KEY=abcdefg
fi

if [ ! -z $3 ] 
then
     ORGANISATION0_SECRET=$3
else
     ORGANISATION0_SECRET=abcdefg
fi


JSON_FILE=AccessKeyName.json

rm -rf accessIdentity accessKey


# Login as Organisation-0
response=$(curl -vX POST ${WEBSERVICE}/oauth/token \
           -d 'grant_type=password&username='${ORGANISATION0_KEY}'&password='${ORGANISATION0_SECRET} \
           --header "Content-Type: application/x-www-form-urlencoded")

org0_accessToken=$(echo ${response} | jq '.access_token' | sed -e 's/^"//' | sed -e 's/"$//')



# Obtain DeviceServer access key for a new organisation
response=$(curl -vX POST ${WEBSERVICE}/accesskeys \
           -d @${JSON_FILE} \
           --header "Content-Type: application/json" \
           --header "Authorization: Bearer "${org0_accessToken})

accessKey=$(echo ${response} | jq '.Key' | sed -e 's/^"//' | sed -e 's/"$//')
accessSecret=$(echo ${response} | jq '.Secret' | sed -e 's/^"//' | sed -e 's/"$//')
echo ${accessKey} > accessKey
echo ${accessSecret} > accessSecret



# Obtain DeviceServer client access token (login)
response=$(curl -vX POST ${WEBSERVICE}/oauth/token \
           -d 'grant_type=password&username='${accessKey}'&password='${accessSecret} \
           --header "Content-Type: application/x-www-form-urlencoded")

accessToken=$(echo ${response} | jq '.access_token' | sed -e 's/^"//' | sed -e 's/"$//')



# Obtain DeviceServer client psk identity and secret
response=$(curl -vX POST ${WEBSERVICE}/identities/psk \
           -d 'grant_type=password&username='${accessKey}'&password='${accessSecret} \
           --header "Authorization: Bearer "${accessToken})

pskIdentity=$(echo ${response} | jq '.Identity' | sed -e 's/^"//' | sed -e 's/"$//')
pskKey=$(echo ${response} | jq '.Secret' | sed -e 's/^"//' | sed -e 's/"$//')
echo ${pskIdentity} > pskIdentity
echo ${pskKey} > pskKey
