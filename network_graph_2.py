import streamlit as st
import pandas as pd
from pyvis.network import Network
import networkx as nx
from community import community_louvain
import community
import streamlit.components.v1 as components

# funtion to select grapgh algorithm
def graph_algorithm(net, alg="barnes"):
    if alg=='barnes':
        net.barnes_hut()
    if alg=='force':
        net.force_atlas_2based()
    if alg=='hrepul':
        net.hrepulsion()

def cred_colour(credibility, cred_color="0efb02"):
    if credibility=='low':
        cred_color='fc081a'
    if credibility=='high':
        cred_color='0598fb'
    if credibility=='medium':
        cred_color='f5fb02'

# function to create graph data
#def create_graph(data_, alg="force", buttons=False, target_color="#1dbde6", 
    #edge_color="#595cff", source_shape="circle", target_shape="circle", cred_shape="triangle"):

st.title('Network Graph Visualization of Content Sharing across Domains')

data = pd.read_csv("datasets/russian_domain_links.csv")

domain_list = data['source'].unique()

domain_list.sort()

selected_domain = st.multiselect('Select domain(s) to visualize', domain_list)

    # set info message on initial site load
if len(selected_domain) == 0:
    st.text('Select at least 1 domain to begin')

    # create network graph when a domain >= 1 is selected
else:
    data_select = data.loc[data['source'].isin(selected_domain) | \
                        data['target'].isin(selected_domain)]
    data_select = data_select.reset_index(drop=True)

    G = nx.from_pandas_edgelist(data_select, 'source', 'target', 'number_links')

    partition_object = community.best_partition(G)

    values = [partition_object.get(node) for node in G.nodes()]

    color_list = ["#0157a1", "#77f431", "#000cb3", "#e4ff3f",
        "#6213c6", "#1abd00", "#ab39eb", "#00c932", "#e232e8",
        "#2a9b00", "#975bff", "#aecf00", "#01119c", "#ffe02b",
        "#5565ff", "#c1ff73", "#a5009f", "#00ca5f", "#ff64e7",
        "#43ffa5", "#f60095", "#76ffa5", "#ff50c9", "#a0ffa4",
        "#3a0067", "#f6ff7f", "#00216e", "#e5bc00", "#e378ff",
        "#aab000", "#828bff", "#ff7910", "#0281e2", "#e08900",
        "#019def", "#ff3f2b", "#01e0d3", "#da0120", "#03bde6",
        "#d04b00", "#819cff", "#648e00", "#ff46ad", "#018436",
        "#b40078", "#01a165", "#ca0067", "#3d7900", "#640063",
        "#f2ffa5", "#16003e", "#f3ffbe", "#0f002d", "#ffd580",
        "#000c26", "#ff6b47", "#01ad92", "#ff5552", "#85e2ff",
        "#b5002d", "#b4ffec", "#8e0023", "#e4ffe9", "#82004f",
        "#667000", "#feaaff", "#284f00", "#b8a8ff", "#8d6d00",
        "#8dbfff", "#724200", "#0174ae", "#ff4f70", "#00512a",
        "#ff9acb", "#0f2a00", "#ffedfe", "#000a05", "#f9fffd",
        "#280e00", "#c9f1ff", "#6b001f", "#e3d2ff", "#571800",
        "#ffdec2", "#003361", "#ff8a77", "#00353c", "#ff839a",
        "#018093", "#ffb094", "#00506d", "#ffbeb9", "#371400",
        "#342c00"]

    color_list = color_list[0:len(set(values))]

    color_dict = pd.Series(color_list, index=np.arange(0,len(set(values)))).to_dict()

    for key, value in partition_object.items():
        partition_object[key] = color_dict[value]

    nx.set_node_attributes(g, partition_object, 'color')

    net = Network(height='400px', width='100%', bgcolor='#222222', font_color='white')

    net.from_nx(G)

    net.force_atlas_2based(
                        gravity=-50,
                        central_gravity=0.01,
                        spring_length=100,
                        spring_strength=0.08,
                        damping=0.4,
                        overlap=0
    )
        
        #if buttons==True:
        #    net.width="75%"
        #    net.show_buttons(filter_=['physics', 'edges'])

        
        #sources = data.iloc[:, 0]
        #targets = data.iloc[:, 1]
        #weights = data.iloc[:, 2]
        #age     = data.iloc[:, 3]
        #cred    = data.iloc[:, 4]

        #edge_data = zip(sources, targets, weights, age, cred)
        
        #for e in edge_data:
         #   source = e[0]
          #  target = e[1]
           # weight = e[2]
           # site_age = int(e[3])
           # credibility = e[4]
            
            #cred_color = 'fc081a' if credibility=='low' else '0598fb' if credibility=='high' else 'f5fb02'
            #node_color = '#ffeda0' if site_age<=1 else '#ffa585' 
            #age_title = 'emerging_domain' if site_age<=1 else 'old_domain'
            
            #net.add_node(source, source, color=node_color, shape=source_shape, size=30, title=source, labelHighlightBold=True)
            #net.add_node(target, target, color=target_color, shape=target_shape, size=30, title=target, labelHighlightBold=True)
            #net.add_node(credibility, credibility, color=cred_color, shape=cred_shape, title=credibility, labelHighlightBold=True)

            #net.add_edge(source, target, color=edge_color, value=weight, title=age_title)
            #net.add_edge(source, credibility, color=cred_color, value=weight, title=age_title)
        
        #neighbor_map = net.get_adj_list() # map node id to list of other node id's

        # hover on a node and it shows the neighboring data
        #for node in net.nodes:
            #node['title'] += ' Neighbors:<br>' + '<br>'.join(neighbor_map[node['id']])
         #   node['title'] += '<br> Number of Neighbors: <br>' + str(len(neighbor_map[node['id']]))
          #  node['value'] = len((neighbor_map[node['id']]))

        # Save and read graph as HTML file (on Streamlit Sharing)
    try:
        path = '/tmp'
        net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html','r',encoding='utf-8')# Save and read graph as HTML file (locally)
    except:
        path = '/html_files'
        net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html','r',encoding='utf-8')

        # Save and read graph as HTML file (locally)
        #net.show('pyvis_graph.html')
        #HtmlFile = open('pyvis_graph.html', 'r', encoding='utf-8')

        # Load HTML file in HTML component for display on Streamlit page
    components.html(HtmlFile.read(), height=435)

    #create_graph("datasets/russian_domain_links.csv", buttons=False)

    #cred_colour(credibility, cred_color=cred_color)
    #graph_algorithm(net, alg=alg)
    #net.set_edge_smooth("dynamic")
    #net.show('data.html')