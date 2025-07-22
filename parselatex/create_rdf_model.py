from rdflib import Graph, URIRef, RDFS
from py_sysml_rdf import SYSML
from obse.graphwrapper import GraphWrapper, create_ref
from .sysml_collector import SysMLCollector


def create_rdf_model(collector: SysMLCollector):
    # Create RDF model
    graph = Graph()

    # Bind a user-declared namespace to a prefix
    graph.bind("sysml", SYSML)

    wrapper = GraphWrapper(graph)

    for requirement_id, requirement in collector.dict_requirements.items():
        requirement_rdf = wrapper.add_labeled_instance(SYSML.Requirement, requirement["name"], requirement_id)
        wrapper.add_str_property(SYSML.requirementText, requirement_rdf, requirement["text"])
        wrapper.add_str_property(SYSML.requirementId, requirement_rdf, requirement["requirement_id"])
        if "nested" in requirement:
            for nested_id in requirement["nested"]:
                nested_rdf = create_ref(SYSML.Requirement, nested_id)
                wrapper.add_reference(SYSML.nestedRequirement, requirement_rdf, nested_rdf)

    return graph
