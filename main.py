import argparse
from parselatex.parse import parse_anforderung
from rdflib import Graph, URIRef, RDFS
from py_sysml_rdf import SYSML
from obse.graphwrapper import GraphWrapper, create_ref

def parse_args():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='SysMP to RDF Transformation.')
    parser.add_argument("--input-latex", required=True, help="Inputfile in SysML Format")
    parser.add_argument("--output-rdf", required=True, help="Outputfile in RDF Format")
    args = parser.parse_args()

    return args.input_latex, args.output_rdf


input_latex, output_rdf = parse_args()


# Create RDF model
graph = Graph()

# Bind a user-declared namespace to a prefix
graph.bind("sysml", SYSML)

wrapper = GraphWrapper(graph)


latex_code = open(input_latex, 'r', encoding='utf-8').read()

for anforderung in parse_anforderung(latex_code):
    print("--- Anforderung ---")
    print("Optionen:", anforderung['options'])
    print("Modality:", anforderung['modality'])
    print("Id:", anforderung['id'])
    print("Text:", anforderung['text'])
    print()

    requirement_rdf = wrapper.add_labeled_instance(SYSML.Requirement, anforderung['id'])
    wrapper.add_str_property(SYSML.requirementText, requirement_rdf, anforderung["text"])
    wrapper.add_str_property(SYSML.requirementId, requirement_rdf, anforderung["id"])
    if "ursprung" in anforderung['options']:
        parent_requirement_rdf = create_ref(SYSML.Requirement, anforderung['options']['ursprung'])
        wrapper.add_reference(SYSML.nestedRequirement, parent_requirement_rdf, requirement_rdf)


graph.serialize(destination=output_rdf, format='turtle')
