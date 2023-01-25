import re


class Road:

    def __init__(self, nodelist=[]):
        self.nodelist = nodelist

    def add(self, node):
        self.nodelist.append(node)


class Node:

    def __init__(self, ip, info, time, id):
        # ip地址
        self.ip = ip
        # 唯一ID
        self.number = id
        # 备注信息
        self.info = info
        # 时延
        self.time = time


def readfile(path):

    filelines = open(path, 'r', encoding='utf-8').readlines()
    result = {}
    string_line = []
    flag = True
    school_name = ""
    for index, line in enumerate(filelines):
        if flag:
            school_name = line.rstrip();
            result[school_name] = ""
            flag = False
        if 'traceroute to' in line:
            continue
        else:
            line = line.rstrip()
        string_line.append(line)
        if filelines[index + 1] == '\n':
            result[school_name] = string_line
        if line == '\n':
            continue
    return result


def check(lines) -> bool:
    """
    检查该条信息是否可以用
    """
    for line in lines:
        if '*' in line:
            return False
    return True


def ipv6_check(addr):
    '''
    检查IPv6是否可用
    '''
    ip6_regex = (
        r'(^(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}$)|'
        r'(\A([0-9a-f]{1,4}:){1,1}(:[0-9a-f]{1,4}){1,6}\Z)|'
        r'(\A([0-9a-f]{1,4}:){1,2}(:[0-9a-f]{1,4}){1,5}\Z)|'
        r'(\A([0-9a-f]{1,4}:){1,3}(:[0-9a-f]{1,4}){1,4}\Z)|'
        r'(\A([0-9a-f]{1,4}:){1,4}(:[0-9a-f]{1,4}){1,3}\Z)|'
        r'(\A([0-9a-f]{1,4}:){1,5}(:[0-9a-f]{1,4}){1,2}\Z)|'
        r'(\A([0-9a-f]{1,4}:){1,6}(:[0-9a-f]{1,4}){1,1}\Z)|'
        r'(\A(([0-9a-f]{1,4}:){1,7}|:):\Z)|(\A:(:[0-9a-f]{1,4}){1,7}\Z)|'
        r'(\A((([0-9a-f]{1,4}:){6})(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3})\Z)|'
        r'(\A(([0-9a-f]{1,4}:){5}[0-9a-f]{1,4}:(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3})\Z)|'
        r'(\A([0-9a-f]{1,4}:){5}:[0-9a-f]{1,4}:(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\Z)|'
        r'(\A([0-9a-f]{1,4}:){1,1}(:[0-9a-f]{1,4}){1,4}:(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\Z)|'
        r'(\A([0-9a-f]{1,4}:){1,2}(:[0-9a-f]{1,4}){1,3}:(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\Z)|'
        r'(\A([0-9a-f]{1,4}:){1,3}(:[0-9a-f]{1,4}){1,2}:(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\Z)|'
        r'(\A([0-9a-f]{1,4}:){1,4}(:[0-9a-f]{1,4}){1,1}:(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\Z)|'
        r'(\A(([0-9a-f]{1,4}:){1,5}|:):(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\Z)|'
        r'(\A:(:[0-9a-f]{1,4}){1,5}:(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\Z)')
    return bool(re.match(ip6_regex, addr, flags=re.IGNORECASE))


def getNode(line, id, ip_set):
    str = "^((http://)|(https://))?([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}(/)"
    lines = line.split(' ')
    if ipv6_check(lines[1]):
        ip = lines[1]
        info = "无"
        times = map(float, [lines[4], lines[6], lines[8]])
        time = max(times)
        if ip_set.__contains__(ip):
            return Node(ip, info, time, ip_set[ip])
        else:
            id += 1
            ip_set[ip] = id
            return Node(ip, info, time, id)
    else:
        if bool(re.match(str, lines[1], flags=re.IGNORECASE)):
            info = lines[1]
            ip = lines[2].replace('(', "").replace(')', "")
            times = map(float, [lines[4], lines[6], lines[8]])
            time = max(times)
            if ip_set.__contains__(ip):
                return Node(ip, info, time, ip_set[ip])
            else:
                id += 1
                ip_set[ip] = id
                return Node(ip, info, time, id)
        else:
            ip = "niming"
            info = "无"
            time = 0
            if ip_set.__contains__(ip):
                return Node(ip, info, time, ip_set[ip])
            else:
                id += 1
                ip_set[ip] = id
                return Node(ip, info, time, id)


def getRoadSet(result):

    class_set = set()
    ip_set = {}
    set = set()
    for school_name, lines in result.items():
        r = Road()
        id = 0
        if check(lines):  # 该条信息可用时
            for line in lines:
                node = getNode(line, id, ip_set)
                set.add(node)
                r.add(node)
    return class_set, set


if __name__ == '__main__':
    result = readfile("road.txt")
    class_set, node_set = getRoadSet(result)
    know_ip_set = open("konw_ip_set.txt", 'r', encoding='utf-8').readlines()
    roadset_file = open('clear_data_road.txt', 'w', 'utf-8')

    with open("node_set.txt", 'w', encoding='utf-8') as file_node:
        for node in node_set:
            file_node.write(node.number + " " + node.ip + " " + node.time + " " + node.info + "\n")
    with open('road_set.txt', 'w', encoding='utf-8') as file_road:
        adjlist = set()
        road_info_list=[]
        for road in class_set:
            from_node = ""
            end_node = ""
            road_info = []
            flag = False
            for i, node in enumerate(road.nodelist):
                if flag and node.ip not in know_ip_set:
                    flag = True
                    road_info.append(int(node.number))
                    continue
                road_info.append(int(node.number))
                if from_node == "" and end_node == "":
                    from_node = str(node.number)
                else:
                    end_node = str(node.number)
                    adjlist.add(from_node + "-" + end_node)
                    from_node = end_node
            road_info_list.append(road_info)
        for line in adjlist:
            file_node.write(line + "\n")
        for road in road_info_list:
            roadset_file.write(str(road)+'\n')
        roadset_file.close()
