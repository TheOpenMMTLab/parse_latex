

# install 

pip install -r requirements.txtx


# usage

python main.py --input-latex text.tex --output-rdf model.ttl


# tests 

python -m pytest tests

# docker image

$ docker build -t frittenburger/parselatex:dev .


