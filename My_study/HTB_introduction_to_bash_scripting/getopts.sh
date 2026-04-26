#!/bin/bash
getopts "o:p:"  opt
  case "${opt}" in 
    o) oo=${OPTARG};;
    p) pp=${OPTARG};;
  esac

echo ${opt}
echo "${oo} ${pp}"
