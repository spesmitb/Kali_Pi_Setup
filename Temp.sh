#!/bin/bash

cpu=(</sys/class/thermal/thermalzone0/temp)
echo "$((cpu/1000)) c"
