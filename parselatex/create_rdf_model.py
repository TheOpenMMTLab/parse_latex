from rdflib import Graph, URIRef, RDFS
from parselatex.requirement import Requirement
from parselatex.decision import Decision
from py_traceability_rdf import Traceability

from obse.graphwrapper import GraphWrapper


def create_rdf_model(collector):
    # Create RDF model
    graph = Graph()

    # Bind a user-declared namespace to a prefix
    graph.bind("trc", Traceability)

    wrapper = GraphWrapper(graph, "https://osm.hpi.de/2026/08/SQuIRRL")

    for entity in collector:
        print(entity)

        if isinstance(entity, Requirement):
            requirement_rdf = wrapper.add_typed_instance(Traceability.Requirement, entity.id, label=entity.id)
            wrapper.add_str_property(Traceability.identifier, requirement_rdf, entity.id)
            wrapper.add_str_property(Traceability.title, requirement_rdf, entity.text)
            if "ursprung" in entity.options:
                parent_rdf = wrapper.create_ref(None, entity.options["ursprung"])
                wrapper.add_reference(Traceability.contains, parent_rdf, requirement_rdf)

        if isinstance(entity, Decision):
            decision_rdf = wrapper.add_typed_instance(Traceability.Decision, entity.id, label=entity.id)
            wrapper.add_str_property(Traceability.identifier, decision_rdf, entity.id)
            wrapper.add_str_property(Traceability.decisionStatus, decision_rdf, entity.state)

            rationale_rdf = wrapper.add_typed_instance(Traceability.Rationale, entity.reference, label=entity.reference)
            wrapper.add_reference(Traceability.isJustifiedBy, decision_rdf, rationale_rdf)

            #if entity.selected:
            #    sel_id, sel_text = entity.selected
            #    selected_rdf = wrapper.create_ref(ADM.Option, entity.id + "#" + sel_id)
            #    wrapper.add_reference(ADM.selectedOption, decision_rdf, selected_rdf)
            #    wrapper.add_str_property(ADM.optionText, selected_rdf, sel_text)

            #for alt_id, alt_text in entity.alternatives.items():
            #    alt_rdf = wrapper.add_labeled_instance(ADM.Option, entity.id + "#" + alt_id)
            #    wrapper.add_str_property(ADM.optionText, alt_rdf, alt_text)
            #    wrapper.add_reference(ADM.hasOption, decision_rdf, alt_rdf)

    return graph
