#!/bin/bash

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# MAC changing is temporary
# -> The MAC-Address will be reset to the original on reboot
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# All chars that can appear in a hex string
hex_chars=(0 1 2 3 4 5 6 7 8 9 A B C D E F)

# Function to generate two hex chars at random (pseudo random)
function hex_pair {
  echo "${hex_chars[((RANDOM % 16))]}${hex_chars[((RANDOM % 16))]}"
}

# Function to generate a random MAC address
function random_mac {
  echo "$(hex_pair):$(hex_pair):$(hex_pair):$(hex_pair):$(hex_pair):$(hex_pair)"
}


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# get the interface name
interface=$(ifconfig | grep ": flags" | cut -d ":" -f 1 | head -n 1)
# get current mac
cur_mac=$(ifconfig $interface | grep "ether" | cut -d " " -f 10)
# generate random mac
new_mac="00:11:22:33:44:55"
new_mac=$(random_mac)

# Output configuration
echo "Interface: $interface"
echo "Current MAC: $cur_mac"

# Change MAC
ifconfig $interface down
rerun=1
while [[ $rerun -eq 1 ]]
do
  echo "Trying to set MAC to: $new_mac"
  ifconfig $interface hw ether $new_mac 2> /dev/null
  rerun=$?
  if [[ $rerun -eq 1 ]]
  then
    echo "Failed to set MAC to: ${new_mac}"
    new_mac="$(random_mac)"
  else
    echo "Successfully set MAC to: ${new_mac}"
  fi
done
ifconfig $interface up

# Exit
exit 0
