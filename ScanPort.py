import optparse
import socket
import threading


screenLock=threading.Semaphore(value=1)
#global open_port_count
open_port_count=0
def connScan(tgtHost,tgtPort):


    try:

        connSkt=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connSkt.connect((tgtHost,tgtPort))
        connSkt.send('ViolentPython\r\n')
        results=connSkt.recv(100)
        global open_port_count
        open_port_count = open_port_count + 1
        screenLock.acquire()

        print('[+] %d/tcp open' %tgtPort)
        print('[+] %s'  %str(results))
    except:
        screenLock.acquire()


       # print('[-] %d/tcp closed' %tgtPort)

    finally:
        screenLock.release()
        connSkt.close()

def portScan(tgtHost, tgtPorts):

    socket.setdefaulttimeout(3)
    for tgtPort in tgtPorts:
        t=threading.Thread(target=connScan,args=(tgtHost,int(tgtPort)))
        t.start()

def main():

    parser=optparse.OptionParser("%prog -H <target host> -p <target port>")
    parser.add_option('-H',dest='tgtHost',type='string',help='specify target host')
#   parser.add_option('-p' ,dest='tgtPort',type='string',help='specify target port[s] separated by comma')
    parser.add_option('-p' ,dest='tgtPorts',type='string',help='specify target port[s] separated by comma')
    (options,args)=parser.parse_args()
    tgtHost = options.tgtHost
#   tgtPorts=str(options.tgtPort).split(',')
    print('the ports list is %s' %options.tgtPorts)
    print('the type of options.tgtPorts is ' , type(options.tgtPorts) )
    tgtPorts=str(options.tgtPorts).split(',')

#    if (tgtHost == None) | (options.tgtPorts == None):
#        print parser.usage
#        exit(1)

    if (tgtHost == None):
        print parser.usage
        exit(1)
    if (options.tgtPorts == None):
        tgtPorts=range(1,65534)
    portScan(tgtHost,tgtPorts)
#    global open_port_count
    print "The Open Port number is %d" %open_port_count

if __name__ == '__main__':
        main()



