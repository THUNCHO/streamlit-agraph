import os
import streamlit.components.v1 as components
import json

# python setup.py sdist bdist_wheel

_RELEASE = True

if not _RELEASE:
    _agraph = components.declare_component(
        "agraph",
        url="http://localhost:3001",
    )

else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _agraph = components.declare_component("agraph", path=build_dir)


class Config:
  def __init__(self, height=800, width=1000, nodeHighlightBehavior=True, highlightColor="#F7A7A6", directed=True, collapsible=True):
    self.height = height
    self.width = width
    self.nodeHighlightBehavior = nodeHighlightBehavior
    self.highlightColor = highlightColor
    self.automaticRearrangeAfterDropNode=True
    self.collapsible=collapsible
    self.directed=directed
    # self.node = { "highlightStrokeColor":"#F7A7A6"} #"highlightColor":"black",
    # self.link = {"highlightColor": "#FDD2BS"}

  def to_dict(self):
    return self.__dict__

class Node:
  def __init__(self,
              id,
              size=250,
              color="#ACDBC9",
              renderLabel=True,
              labelPosition="right",
              svg="",
              symbolType="circle",
              strokeColor="" #F7A7A6
               ):
    self.id=id
    self.size=size
    self.color=color #FDD2BS #F48B94 #F7A7A6 #DBEBC2
    self.renderLabel=renderLabel
    self.labelPosition=labelPosition #(left,top,bottom,right, center)
    self.svg=svg
    self.symbolType=symbolType  # "cross", "diamond", "square", "star", "triangle", "wye"
    self.strokeColor=strokeColor

  def to_dict(self):
    return self.__dict__

class Edge:
  def __init__(self, source, target,
              color="#F7A7A6",
              renderLabel=False,
              labelPosition="right",
              # highlightColor="#F7A7A6", #F7A7A6
              type="STRAIGHT",
              semanticStrokeWidth=False,
              strokeWidth=1.5,
              labelProperty="",
              linkValue=1
               ):
    self.source=source
    self.target=target
    self.color=color #labelPropertyF48B94 #F7A7A6 #
    self.renderLabel=renderLabel
    self.labelPosition=labelPosition #(left,top,bottom,right, center)
    # self.highlightColor=highlightColor
    self.type=type #CURVE_SMOOTH , CURVE_FULL
    self.semanticStrokeWidth=semanticStrokeWidth #strokeWidth += (linkValue * strokeWidth) / 10;
    self.strokeWidth=strokeWidth
    self.labelProperty=labelProperty
    self.linkValue=linkValue

  def to_dict(self):
    return self.__dict__

# def parse_node(*args):
#  nodes_data = [{"id": f"{node}"} for node in nodes]

def agraph(nodes, edges, config):

    nodes_data = [ node.to_dict() for node in nodes]
    edges_data = [ edge.to_dict() for edge in edges]

    #nodes_data = [{"id": f"{node}"} for node in nodes]
    #edges_data = [ {"source": f"{edge[0]}", "target": f"{edge[1]}"} for edge in edges]

    config_json = json.dumps(config.__dict__)
    # st.write(config_json)

    data = { "nodes": nodes_data, "links": edges_data}
    # st.write(data)
    data_json = json.dumps(data)
    component_value = _agraph(data=data_json, config=config_json)

    return component_value

# app: `$ streamlit run agraph/__init__.py`
if not _RELEASE:
    import json
    import streamlit as st

    st.subheader("Component with constant args")
    nodes = []
    edges = []
    nodes.append( Node(id="Spiderman", size=400, svg="http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_spiderman.png") ) # ,
    nodes.append( Node(id="Captain_Marvel", size=400, svg="http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_captainmarvel.png"))
    edges.append(Edge(source="Captain_Marvel", target="Spiderman", type="CURVE_SMOOTH"))
    # nodes.append( Node(id="Chris_Klose", size=400, svg="https://github.com/ChrisChross/streamlit-agraph/blob/master/imgs/Chris.png?raw=true") ) #
    # edges.append(Edge(source="Chris_Klose", target="Spiderman", type="CURVE_SMOOTH"))
    # edges.append( Edge(source="Chris_Klose", target="Spiderman", type="CURVE_SMOOTH") )
   # edges.append(Edge(source="Chris_Klose", target="Captain_Marvel", type="CURVE_SMOOTH" )) # renderLabel=True, labelProperty="best_friend_of"
    #nodes = ["Harry","Sally","Peter","Chris"]
    #edges = [("Harry","Sally"),("Peter","Chris")]

    # myConfig = { "nodeHighlightBehavior": "true", "node": { "color": "lightgreen", "size": 120, "highlightStrokeColor": "blue",}, "link": { "highlightColor": "lightblue",}, }

    config = Config(width=500, height=500, directed=True)
    return_value = agraph(nodes=nodes, edges=edges, config=config)

    # st.write(return_value)
    # st.markdown("You've clicked %s times!" % int(num_clicks))

    st.markdown("---")
