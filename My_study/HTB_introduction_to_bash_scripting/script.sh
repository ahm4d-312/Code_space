#!/bin/bash
# check the args, and assign them
if [ ${#} -eq 2 ]
then
  ip_address=$1
  domain_name=$2
elif [ ${#} -eq 3 ]
then
  ip_address=$1
  domain_name=$2
  sub_domain=$3
else
  echo -e "usage: ${0} <ip_address> <domain_name> <sub_domain> -> (optional)"
  echo -e "The order of the arga matters!, the args must be passed in order."
fi

Check_exist(){
  grep -i $1 /etc/hosts
  return $?
}

if [[ $(Check_exist ${domain_name}) -eq 0 ]];then
  echo 444
fi
