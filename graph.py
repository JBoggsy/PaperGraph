from json import load, dump
import networkx as nx


class PaperGraph(nx.DiGraph):
    """A special sub-class of the networkx directed-graph class."""
    def __init__(self, filename):
        """
        Create a new, empty directed graph which references a JSON file.

        :param filename: The name of the JSON file to load, update and save the graph to.
        """
        self.filename = filename
        super(PaperGraph, self).__init__()

    def add_paper(self, name, title, authors, year, group):
        self.add_node(name, title=title, authors=authors, year=year, group=group)
        self.save_graph()

    def load_graph(self):
        with open(self.filename, 'r') as file:
            graph_dict = load(file)
        if 'nodes' not in graph_dict or 'links' not in graph_dict:
            return
        nodes_list = graph_dict['nodes']
        edges_list = graph_dict['links']
        for node_data in nodes_list:
            node_name = node_data['name']
            node_group = node_data['group']
            node_title = node_data['title']
            node_authors = node_data['authors']
            node_year = node_data['year']
            self.add_node(node_name, title=node_title, authors=node_authors, year=node_year, group=node_group)
        for edge_data in edges_list:
            edge_source = edge_data['source']
            edge_target = edge_data['target']
            self.add_edge(nodes_list[edge_source]['name'], nodes_list[edge_target]['name'])

    def save_graph(self):
        node_list = []
        node_position_dict = {}
        i = 0
        for node_name, node in self.nodes(data=True):
            node_group = node['group']
            node_title = node['title']
            node_authors = node['authors']
            node_year = node['year']
            node_dict = {'name': node_name,
                         'group': node_group,
                         'title': node_title,
                         'authors': node_authors,
                         'year': node_year}
            node_position_dict[node_name] = i
            node_list.append(node_dict)
            i += 1

        edges_list = []
        for src, dst in self.edges:
            src_idx = node_position_dict[src]
            dst_idx = node_position_dict[dst]
            link_dict = {'source': src_idx,
                         'target': dst_idx,
                         'value': 1}
            edges_list.append(link_dict)

        graph_dict = {'nodes': node_list,
                      'links': edges_list}

        with open(self.filename, 'w') as file:
            dump(graph_dict, file)


if __name__ == '__main__':
    g = PaperGraph("static/graph.json")
    g.load_graph()
    g.save_graph()