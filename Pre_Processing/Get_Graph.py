
from Pre_Processing.Feature_extraction import Node
from Pre_Training.Computer import compute
from Pre_Processing.prossessing import compare_whois, compare_Similarity, getIPV6
import networkx as nx
import numpy as np


def getAdjList():

    with open('road_set.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        n = len(lines)
        adjlist = np.zeros([2, n])
        for id, line in enumerate(lines):
            r = line.split('-')
            adjlist[id] = [int(r[0]), int(r[1])]
        return adjlist


def get_Vet_Feature():

    G = nx.DiGraph()
    road = open('road_set.txt', 'r', encoding='utf-8').readlines()
    for line in road:
        nodes = line.split("-")
        G.add_edge(int(nodes[0]), int(nodes[1]))
    nodes = open("node_set.txt", "r", encoding="utf-8").readlines()
    for node in nodes:
        node = node.split(" ")
        G[int(node[0])]["ip"] = node[1]
    result = np.zeros([len(road), 3472])
    for index, node in enumerate(nodes):
        node = node.split(" ")
        ip = list(getIPV6(node[1]))
        neighbors = list(G.neighbors([int(node[0])]))
        one_hot = [0 for i in range(3344)]
        for i in range(len(neighbors)):
            one_hot[i] = 1
        ip.extend(one_hot)
        result[index] = np.array(ip)
    return result


def getinfo(ip, infoset):

    for i in infoset:
        if ip == i[0]:
            return i


def getinfoset():
    konw_info = open("konw_ip_set.txt", 'r', 'utf-8').readlines()
    result = []
    temp_list = []
    string = ""
    for id, line in enumerate(konw_info):
        if line == '\n':
            strs = string.split('-')
            for i in range(1, len(strs)):
                if i % 2 == 1:
                    temp_list.append(str[i])
                    result.append(temp_list)
                    temp_list.clear()
        string = "-" + string
    return result


def get_Edge_Feature(T):

    node_list = open("node.txt", 'r', 'utf-8').readlines()
    nodes = []
    for node in node_list:
        info = node.split(" ")
        nodes.append(Node(info[1], int(info[0])), float(info[2]), info[3])
    nodes.sort(key=lambda x1: x1.number)

    road_list = open("road_set.txt", 'r', 'utf-8').readlines()
    result = np.zeros([len(node_list), len(node_list)])
    res = getinfoset()

    for lines in road_list:

        lines = lines.split("-")
        from_node = nodes[lines[0] + 1]
        end_node = nodes[lines[1] + 1]
        if from_node.time - end_node.time > 0:
            time = from_node.time - end_node.time
        else:
            time = 0.0
        if from_node.info == end_node.info:
            name = 1
        else:
            name = 0
        whois1 = []
        info1 = getinfo(from_node.ip, res)
        info2 = getinfo(end_node.ip, res)
        whois2 = []
        list1 = [0, 1, 2, 3, 4, 5, 8, 9]
        for i in list1:
            whois1.append(info1[i])
            whois2.append(info2[i])
        result_whois = compare_whois(whois1, whois2)
        ip_sim = compare_Similarity(from_node.ip, end_node.ip)
        x = [result_whois, ip_sim, name, time]
        t_pred = compute(x, T)
        result[from_node.number][end_node] = np.array(t_pred)[0]
    return result
