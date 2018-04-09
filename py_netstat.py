import socket
from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM

import psutil

AD = "-"
AF_INET6 = getattr(socket, 'AF_INET6', object())
proto_map = {
    (AF_INET, SOCK_STREAM): 'tcp',
    (AF_INET6, SOCK_STREAM): 'tcp6',
    (AF_INET, SOCK_DGRAM): 'udp',
    (AF_INET6, SOCK_DGRAM): 'udp6',
}

f = open('netstat-output.txt', 'w')


def main():
    templ = "%-5s %-30s %-30s %-13s %-6s %s"
    f.write((templ % ("Protocol", "Local address", "Remote address", "Status", "PID", "Program name \n")))
    proc_names = {}
    for p in psutil.process_iter(attrs=['pid', 'name']):
        proc_names[p.info['pid']] = p.info['name']
    for c in psutil.net_connections(kind='inet'):
        laddr = "%s:%s" % (c.laddr)
        raddr = ""
        if c.raddr:
            raddr = "%s:%s" % (c.raddr)

        f.write(templ % (proto_map[(c.family, c.type)], laddr, raddr or AD, c.status, c.pid or AD, proc_names.get(c.pid, '?')[:15]) + "\n")
    print("simple script to output info about all working programs in computer and all viewing active ports :)")
    print("output file saved as netstat-output.txt ")

if __name__ == '__main__':
    main()