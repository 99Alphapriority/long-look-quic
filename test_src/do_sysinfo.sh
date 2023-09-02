outfile=$1
host=$2

# CPU
printf "CPU info :\n" >> $outfile"_sysinfo.txt"
cat /proc/cpuinfo >> $outfile"_sysinfo.txt"

# Memory
printf "\n\n Memory info :\n" >> $outfile"_sysinfo.txt"
cat /proc/meminfo >> $outfile"_sysinfo.txt"

# Network
printf "\n\n Network info :\n" >> $outfile"_sysinfo.txt"
cat /sys/class/net/enp*/speed >> $outfile"_sysinfo.txt"