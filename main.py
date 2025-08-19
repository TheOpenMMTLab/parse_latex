import argparse
from parselatex.parse import parse_latex
from rdflib import Graph
from py_sysml_rdf import SYSML
from obse.graphwrapper import GraphWrapper, create_ref
from parselatex.create_rdf_model import create_rdf_model


def parse_args():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='SysMP to RDF Transformation.')
    parser.add_argument("--input-latex", required=True, help="Inputfile in SysML Format")
    parser.add_argument("--output-rdf", required=True, help="Outputfile in RDF Format")
    args = parser.parse_args()

    return args.input_latex, args.output_rdf


input_latex, output_rdf = parse_args()

latex_code = open(input_latex, 'r', encoding='utf-8').read()

content = parse_latex(latex_code)

graph = create_rdf_model(content)

graph.serialize(destination=output_rdf, format='turtle')
