

import streamlit as st
import pandas as pd
from pyvis.network import Network
import networkx as nx
#from community import community_louvain
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
def create_graph(data_, alg="force", buttons=False, target_color="#1dbde6", 
    edge_color="#595cff", source_shape="circle", target_shape="circle", cred_shape="triangle"):

    st.title('Network Graph Visualization of Content Sharing across Domains')

    data = pd.read_csv(data_)

    domain_list = data['source'].unique()

    domain_list.sort()

    selected_domain = st.multiselect('Select drug(s) to visualize', domain_list)

    # set info message on initial site load
    if len(selected_domain) == 0:
        st.text('Select at least 1 domain to begin')

    # create network graph when a domain >= 1 is selected
    else:
        data_select = data.loc[data['source'].isin(selected_domain) | \
                        data['target'].isin(selected_domain)]
        data_select = data_select.reset_index(drop=True)

        G = nx.from_pandas_edgelist(data_select, 'source', 'target', 'number_links')

        net = Network(height='100%', width='100%', bgcolor='#222222', font_color='white', directed=True)

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
        components.html(HtmlFile.read())

    create_graph("datasets/russian_domain_links.csv", buttons=False)

    #cred_colour(credibility, cred_color=cred_color)
    #graph_algorithm(net, alg=alg)
    #net.set_edge_smooth("dynamic")
    #net.show('data.html')