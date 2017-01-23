import subprocess
import os

def get_ram():
    "Returns a tuple (total ram, available ram) in megabytes. See www.linuxatemyram.com"
    try:
        s = subprocess.check_output(["free","-m"])
        lines = s.split("\n") 
        return ( int(lines[1].split()[1]), int(lines[2].split()[3]) )
    except:
        return 0

def get_process_count():
    "Returns the number of processes"
    try:
        s = subprocess.check_output(["ps","-e"])
        return len(s.split("\n")) 
    except:
        return 0

def get_up_stats():
    #"Returns a tuple (uptime, 5 min load average)"
    try:
        s = subprocess.check_output(["uptime"])
        load_split = s.split("load average: ")
        load_five = float(load_split[1].split(',')[1])
        up = load_split[0]
        up_pos = up.rfind(',',0,len(up)-4)
        up = up[:up_pos].split("up ")[1]
        return ( up , load_five ) 
    except:
        return ( "", 0 )

def get_connections():
    "Returns the number of network connections"
    try:
        s = subprocess.check_output(["netstat","-tun"])
        return len([x for x in s.split() if x == 'ESTABLISHED'])
    except:
        return 0

def get_temperature():
    "Returns the temperature in degrees C"
    try:
        s = subprocess.check_output(["/opt/vc/bin/vcgencmd","measure_temp"])
        return float(s.split('=')[1][:-3])
    except:
        return 0

def get_ipaddress():
    "Returns the current IP address"
    arg='ip route list'
    p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
    data = p.communicate()
    split_data = data[0].split()
    ipaddr = split_data[split_data.index('src')+1]
    return ipaddr

def get_cpu_speed_max():
    "Returns the current CPU speed"
    f = os.popen('/opt/vc/bin/vcgencmd get_config arm_freq')
    cpu = f.read()
    return str(cpu).split("=",)[1][:-1]

def get_cpu_speed_current():
    "Returns the current CPU speed"
    f = os.popen('/opt/vc/bin/vcgencmd get_config core_freq')
    cpu = f.read()
    return str(cpu).split("=",)[1][:-1]

# Return % of CPU used by user as a character string                                
def getCPUuse():
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip(\
    )))

# Return information about disk space as a list (unit included)                     
# Index 0: total disk space                                                         
# Index 1: used disk space                                                          
# Index 2: remaining disk space                                                     
# Index 3: percentage of disk used                                                  
def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()
        if i==2:
            return(line.split()[1:5])

def showDiskSpace():
	print "Disk space:"
	values = getDiskSpace()
	print "  Free: \t" + values[2]
	print "  Used: \t" + values[1]
	print "  Total:\t" + values[0]

def show_memory_info():
    freeMemory = get_ram()[1]
    totalMemory = get_ram()[0]
    progress = ((freeMemory*20) / totalMemory)
    progress = int(progress)
    print 'RAM: '+str(freeMemory)+'MB free of '+str(totalMemory)+'MB'
    bar = ""
    for x in xrange(20-progress):
    	bar += "#"
    for x in xrange(progress):
    	bar += " "
    print "Memory: " + str(100-((freeMemory*100) / totalMemory)) + "%"
    print "[" + bar + "]"
    

#print("\033[1;32;40m Bright Green  \n")
def showCPUTempWithColors():
	print 'Temperature: ' +str(get_temperature()) + "'C"
	#print("\033[" + color + text)


showCPUTempWithColors()
print 'CPU speed core: '+str(get_cpu_speed_current()) + " MHz"
print 'CPU speed max: '+str(get_cpu_speed_max()) + " MHz"
print 'CPU useage: ' + getCPUuse() + "%"
print 'Nr. of processes: '+str(get_process_count())
show_memory_info()
print 'IP-address: '+get_ipaddress()
print 'Nr. of connections: '+str(get_connections())
print 'Up time: '+get_up_stats()[0]
showDiskSpace()
