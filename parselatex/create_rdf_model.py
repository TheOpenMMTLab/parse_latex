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
        try:
            print(entity)
        except UnicodeEncodeError:
            # Skip printing if encoding error occurs
            pass

        if isinstance(entity, Requirement):
            requirement_rdf = wrapper.add_typed_instance(Traceability.Requirement, entity.id, label=entity.id)
            wrapper.add_str_property(Traceability.identifier, requirement_rdf, entity.id)
            wrapper.add_str_property(Traceability.title, requirement_rdf, entity.text)
            wrapper.add_str_property(Traceability.modality, requirement_rdf, entity.modality)
            if "bedingung" in entity.options:
                wrapper.add_str_property(Traceability.condition, requirement_rdf, entity.options["bedingung"])

            if "ursprung" in entity.options:
                # TODO: handle if ursprung is other Requirement or Source (e.g. DIN-EN-50716)
                parent_rdf = wrapper.create_ref(None, entity.options["ursprung"])
                wrapper.add_reference(Traceability.contains, parent_rdf, requirement_rdf)
                # if ursprung is Source use justifies as relation

        if isinstance(entity, Decision):
            decision_rdf = wrapper.add_typed_instance(Traceability.Decision, entity.id, label=entity.id)
            wrapper.add_str_property(Traceability.identifier, decision_rdf, entity.id)
            wrapper.add_str_property(Traceability.decisionStatus, decision_rdf, entity.state)
            wrapper.add_str_property(Traceability.title, decision_rdf, entity.problem)

            # Add references (can be multiple)
            for reference in entity.references:
                ref_rdf = wrapper.create_ref(None, reference)
                wrapper.add_reference(Traceability.references, decision_rdf, ref_rdf)

    return graph
