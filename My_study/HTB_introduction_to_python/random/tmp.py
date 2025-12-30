ss=            """Example:
nc.py -t 192.168.1.108 -p 5555 -l -s\t#command shell               

        nc.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt\t#upload to file

        nc.py -t 192.168.1.108 -p 5555 -l -e="cat /etc/passwd"\t# execute command 
        
        echo 'ABC' | ./nc.py -t 192.168.1.108 -p 135\t# echo text to server port 135
        
        nc.py -t 192.168.1.108 -p 5555\t# connect to server

        The default ip is 0.0.0.0 and the default port is 5555
        """
print(ss)
