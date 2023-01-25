def compare_whois(whois1, whois2):
    same = 0
    same = float(same)
    for i in range(8):
        if whois1.feature[i] == whois2.feature[i]:
            same += 1
    return float(same / 8)


def compare_Similarity(IP1, IP2):

    ip_string1 = getIPV6(IP1)
    ip_string2 = getIPV6(IP2)
    same = float(0.0)
    for i in range(128):
        if ip_string1[i] == ip_string2[2]:
            same += 1
    return float(same / 128)


def getIPV6(IP):

    ip1 = IP.split(':')
    d1 = {'0': '0000', '1': '0001', '2': '0010', '3': '0011', '4': '0100', '5': '0101', '6': '0110', '7': '0111',
          '8': '1000',
          '9': '1001', 'a': '1010', 'b': '1011', 'c': '1100', 'd': '1101', 'e': '1110', 'f': '1111'}
    for i in range(4 - len(ip1)):
        ip1.append('0')
    ip_string = ""
    for i in ip1:
        for k in range(4 - len(i)):
            i = '0' + i
        for j in i:
            ip_string = ip_string + d1[j]
    return ip_string
