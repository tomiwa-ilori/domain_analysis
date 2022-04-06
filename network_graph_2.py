import numpy as np
import pandas as pd
import networkx as nx
import streamlit as st
from pyvis.network import Network
from community import community_louvain
import streamlit.components.v1 as components


st.title('Network Graph Visualization of Content Sharing across Domains')

data = pd.read_csv('../datasets/domain_threshold.csv')

domain_list = data['source_domain'].unique()

domain_list.sort()

selected_domain = st.multiselect('Select domain(s) to visualize', domain_list)

    # set info message on initial site load
if len(selected_domain) == 0:
    st.text('Select at least 1 domain to begin')

    # create network graph when a domain >= 1 is selected
else:
    data_select = data.loc[data['source_domain'].isin(selected_domain) | \
                        data['target_domian'].isin(selected_domain)]
    data_select = data_select.reset_index(drop=True)

    G = nx.from_pandas_edgelist(data_select, 'source_domain', 'target_domian', 'size')

    partition_object = community_louvain.best_partition(G)

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

    nx.set_node_attributes(G, partition_object, 'color')

    net = Network(height='750px', width='100%', bgcolor='#222222', font_color='white')

    net.from_nx(G)

    net.force_atlas_2based(
                        gravity=-50,
                        central_gravity=0.01,
                        spring_length=100,
                        spring_strength=0.08,
                        damping=0.4,
                        overlap=0
    )
     
    # Save and read graph as HTML file (on Streamlit Sharing)
    try:
        path = '/tmp'
        net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html','r',encoding='utf-8')# Save and read graph as HTML file (locally)
    except:
        path = '/html_files'
        net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html','r',encoding='utf-8')

    # Load HTML file in HTML component for display on Streamlit page
    components.html(HtmlFile.read(), height=750)
