#####################
# write in console: #
#####################
# 
# bash ./start.bash
# 
#############################################
# this will make 'exe' files: pinger, csver #
#############################################

g++ pinger.cpp -o pinger
g++ csver.cpp -o csver
./pinger | ./csver

########################################
# stdout of pinger ---> stdin of csver #
########################################
# 
######################
# csv file: ping.csv #
######################