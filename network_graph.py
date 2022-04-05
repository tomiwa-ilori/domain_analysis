{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "import streamlit as st\n",
    "import pandas as pd\n",
    "from pyvis.network import Network\n",
    "from community import community_louvain\n",
    "import streamlit.components.v1 as components"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#import community\n",
    "#louvain_partition = community.best_partition(G, weight='weight')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "# funtion to select grapgh algorithm\n",
    "def graph_algorithm(net, alg=\"barnes\"):\n",
    "    if alg=='barnes':\n",
    "        net.barnes_hut()\n",
    "    if alg=='force':\n",
    "        net.force_atlas_2based()\n",
    "    if alg=='hrepul':\n",
    "        net.hrepulsion()\n",
    "\n",
    "def cred_colour(credibility, cred_color=\"0efb02\"):\n",
    "    if credibility=='low':\n",
    "        cred_color='fc081a'\n",
    "    if credibility=='high':\n",
    "        cred_color='0598fb'\n",
    "    if credibility=='medium':\n",
    "        cred_color='f5fb02'\n",
    "\n",
    "# function to create graph data\n",
    "def create_graph(data_, alg=\"force\", buttons=False, target_color=\"#1dbde6\", \n",
    "    edge_color=\"#595cff\", source_shape=\"circle\", target_shape=\"circle\", cred_shape=\"triangle\"):\n",
    "\n",
    "    st.title('Network Graph Visualization of Content Sharing across Domains')\n",
    "\n",
    "    data = pd.read_csv(data_)\n",
    "\n",
    "    domain_list = data['source'].unique()\n",
    "\n",
    "    domain_list.sort()\n",
    "\n",
    "    selected_domain = st.multiselect('Select drug(s) to visualize', domain_list)\n",
    "\n",
    "    # set info message on initial site load\n",
    "    if len(selected_domain) == 0:\n",
    "        st.text('Select at least 1 domain to begin')\n",
    "\n",
    "    # create network graph when a domain >= 1 is selected\n",
    "    else:\n",
    "        data_select = data.loc[data['source'].isin(selected_domain) | \\\n",
    "                        data['target'].isin(selected_domain)]\n",
    "        data_select = data_select.reset_index(drop=True)\n",
    "\n",
    "        net = Network(height='100%', width='100%', bgcolor='#222222', font_color='white', directed=True)\n",
    "        \n",
    "        if buttons==True:\n",
    "            net.width=\"75%\"\n",
    "            net.show_buttons(filter_=['physics', 'edges'])\n",
    "        \n",
    "        sources = data.iloc[:, 0]\n",
    "        targets = data.iloc[:, 1]\n",
    "        weights = data.iloc[:, 2]\n",
    "        age     = data.iloc[:, 3]\n",
    "        cred    = data.iloc[:, 4]\n",
    "\n",
    "        edge_data = zip(sources, targets, weights, age, cred)\n",
    "        \n",
    "        for e in edge_data:\n",
    "            source = e[0]\n",
    "            target = e[1]\n",
    "            weight = e[2]\n",
    "            site_age = int(e[3])\n",
    "            credibility = e[4]\n",
    "            \n",
    "            cred_color = 'fc081a' if credibility=='low' else '0598fb' if credibility=='high' else 'f5fb02'\n",
    "            node_color = '#ffeda0' if site_age<=1 else '#ffa585' \n",
    "            age_title = 'emerging_domain' if site_age<=1 else 'old_domain'\n",
    "            \n",
    "            net.add_node(source, source, color=node_color, shape=source_shape, size=30, title=source, labelHighlightBold=True)\n",
    "            net.add_node(target, target, color=target_color, shape=target_shape, size=30, title=target, labelHighlightBold=True)\n",
    "            #net.add_node(credibility, credibility, color=cred_color, shape=cred_shape, title=credibility, labelHighlightBold=True)\n",
    "\n",
    "            net.add_edge(source, target, color=edge_color, value=weight, title=age_title)\n",
    "            #net.add_edge(source, credibility, color=cred_color, value=weight, title=age_title)\n",
    "        \n",
    "        neighbor_map = net.get_adj_list() # map node id to list of other node id's\n",
    "\n",
    "        # hover on a node and it shows the neighboring data\n",
    "        for node in net.nodes:\n",
    "            #node['title'] += ' Neighbors:<br>' + '<br>'.join(neighbor_map[node['id']])\n",
    "            node['title'] += '<br> Number of Neighbors: <br>' + str(len(neighbor_map[node['id']]))\n",
    "            node['value'] = len((neighbor_map[node['id']]))\n",
    "\n",
    "        # Save and read graph as HTML file (locally)\n",
    "        net.show('pyvis_graph.html')\n",
    "        HtmlFile = open('pyvis_graph.html', 'r', encoding='utf-8')\n",
    "\n",
    "        # Load HTML file in HTML component for display on Streamlit page\n",
    "        components.html(HtmlFile.read())\n",
    "\n",
    "        \n",
    "\n",
    "    #cred_colour(credibility, cred_color=cred_color)\n",
    "    #graph_algorithm(net, alg=alg)\n",
    "    #net.set_edge_smooth(\"dynamic\")\n",
    "    #net.show('data.html')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [],
   "source": [
    "create_graph(\"datasets/russian_domain_links.csv\", buttons=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "#data_2 = pd.read_csv('datasets/russian_domain_links.csv', index=False)\n",
    "#data_2.drop(columns=['Unnamed: 0', 'Unnamed: 0.1' ])\n",
    "#data_2['age'].astype(int)\n",
    "#data_2.loc[data_2['age'].isna(), 'age'] = int(1)\n",
    "#data_2.to_csv('datasets/russian_domain_links.csv', index=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "interpreter": {
   "hash": "31f2aee4e71d21fbe5cf8b01ff0e069b9275f58929596ceb00d14d90e3e16cd6"
  },
  "kernelspec": {
   "display_name": "Python 3.6.9 64-bit",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.5"
  },
  "orig_nbformat": 4
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
