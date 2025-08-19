from rdflib import Graph, URIRef, RDFS
from parselatex.requirement import Requirement
from parselatex.decision import Decision
from py_sysml_rdf import SYSML
from py_adm_rdf import ADM

from obse.graphwrapper import GraphWrapper, create_ref


def create_rdf_model(collector):
    # Create RDF model
    graph = Graph()

    # Bind a user-declared namespace to a prefix
    graph.bind("sysml", SYSML)

    wrapper = GraphWrapper(graph)

    for entity in collector:
        print(entity)

        if isinstance(entity, Requirement):
            requirement_rdf = wrapper.add_labeled_instance(SYSML.Requirement, entity.id)
            wrapper.add_str_property(SYSML.requirementText, requirement_rdf, entity.text)
            wrapper.add_str_property(SYSML.requirementId, requirement_rdf, entity.id)
            if "ursprung" in entity.options:
                nested_rdf = create_ref(SYSML.Requirement, entity.options["ursprung"])
                wrapper.add_reference(SYSML.nestedRequirement, requirement_rdf, nested_rdf)

        if isinstance(entity, Decision):
            decision_rdf = wrapper.add_labeled_instance(ADM.Decision, entity.id)
            wrapper.add_str_property(ADM.decisionState, decision_rdf, entity.state)
            rationale_rdf = create_ref(ADM.Option, entity.reference)
            wrapper.add_reference(ADM.hasRationale, decision_rdf, rationale_rdf)

            if entity.selected:
                sel_id, sel_text = entity.selected
                selected_rdf = create_ref(ADM.Option, entity.id + "#" + sel_id)
                wrapper.add_reference(ADM.selectedOption, decision_rdf, selected_rdf)
                wrapper.add_str_property(ADM.optionText, selected_rdf, sel_text)

            for alt_id, alt_text in entity.alternatives.items():
                alt_rdf = wrapper.add_labeled_instance(ADM.Option, entity.id + "#" + alt_id)
                wrapper.add_str_property(ADM.optionText, alt_rdf, alt_text)
                wrapper.add_reference(ADM.hasOption, decision_rdf, alt_rdf)

    return graph
