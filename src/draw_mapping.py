import pygraphviz as pgv
import traceback, re

def _get_arg_names(stack):
    _, _, _, code = stack[-2]
    args = re.compile(r'\((.*?)\).*$').search(code).groups()[0]
    temp = tuple([x.strip() for x in args.split(',')])
    arg_names = []
    for t in temp:
        arg_names.append(t[0])
    return arg_names

def _isupper(arg_name):
    return arg_name[0].isupper()

def create_mapping(**kwargs):
    stack = traceback.extract_stack()
    arg_names = _get_arg_names(stack)
    set_names = []
    function_names = []
    for arg_name in arg_names:
        if _isupper(arg_name):
            set_names.append(arg_name)
        else:
            function_names.append(arg_name)
    graph = pgv.AGraph()
    graph.graph_attr['rankdir'] = 'LR'
    graph.node_attr['shape'] = 'point'
    graph.graph_attr['ranksep'] = '2.0'
    graph.node_attr['nodesep'] = '2.0'

    for set_name in set_names:
        nodes = kwargs[set_name]
        for node in nodes:
            graph.add_node(node, xlabel=node)
        cluster_name = "cluster_" + set_name
        graph.add_subgraph(nodes, cluster_name, label=set_name)

    for i in range(len(function_names)):
        function_name = function_names[i]
        mapping = kwargs[function_name]
        for a, b in mapping:
            graph.add_edge(a, b)

    return graph

if __name__ == '__main__':
    A = {'Troy', 'Chris', 'Travis'}
    B = {'A', 'B', 'C', 'D', 'F'}
    f = {('Troy', 'B'), ('Chris', 'A'), ('Travis', 'C')}
    graph = create_mapping(A=A, B=B, f=f)
    graph.add_edge('Troy', 'D', label='f', ltail='cluster_A', lhead='cluster_B')
    graph.draw('test.dot', prog='dot')

