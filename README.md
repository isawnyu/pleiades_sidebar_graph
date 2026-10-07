# pleiades_sidebar_graph

by Tom Elliott for the Institute for the Study of the Ancient World (ISAW) at New York University.\
(c) Copyright 2026 by New York University.\
Licensed under the AGPL-3.0; see LICENSE.txt file.   

## What?

Create RDF (and then work with it) from the [Linked Places Format JSON data](https://github.com/isawnyu/pleiades.datasets/tree/main/data/sidebar) compiled to support the [Pleiades Linked Data Sidebar](https://pleiades.stoa.org/help/linked-data-sidebar) feature of the [Pleiades gazetteer of ancient places](https://pleiades.stoa.org/). 

Triples in the graph, as currently produced (see "How?" below), are like this:

```turtle
@prefix geojson: <https://purl.org/geojson/vocab#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix schema: <https://schema.org/> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .

<https://pleiades.stoa.org/places/570740> skos:relatedMatch <http://nomisma.org/id/tiryns>,
        <http://www.wikidata.org/entity/Q217379>,
        <https://chronique.efa.gr/?r=topo_public&id=37697>,
        <https://resource.manto.unh.edu/8253955>,
        <https://topostext.org/place/376228PTir> .

<https://vici.org/vici/11432> a geojson:Feature ;
    rdfs:label "Tiryns"@und ;
    skos:closeMatch <http://www.wikidata.org/entity/Q217379>,
        <https://pleiades.stoa.org/places/570740> .

<https://chronique.efa.gr/?r=topo_public&id=37697> a geojson:Feature ;
    rdfs:label "Tirynthe, Tiryntha, Tiryns, Τίρυνς"@und ;
    skos:closeMatch <https://pleiades.stoa.org/places/570740> .

<https://resource.manto.unh.edu/8253955> a geojson:Feature ;
    rdfs:label "Tiryns (Argolid)"@und ;
    skos:closeMatch <https://pleiades.stoa.org/places/570740> ;
    schema:description "city in the Argolid"@und .                    

<https://topostext.org/place/376228PTir> a geojson:Feature ;
    rdfs:label "Tiryns (Argolid)"@und ;
    skos:closeMatch <https://pleiades.stoa.org/places/570740>,
        <https://www.wikidata.org/wiki/Q217379> ;
    schema:description "Archaic to Hellenistic polis at Tirynthos in Argolid Peloponnese"@und .

<http://nomisma.org/id/tiryns> a geojson:Feature ;
    rdfs:label "Tiryns"@und ;
    skos:closeMatch <http://dbpedia.org/resource/Tiryns>,
        <http://vocab.getty.edu/tgn/7011074>,
        <https://ikmk.smb.museum/ndp/ort/3051>,
        <https://pleiades.stoa.org/places/570740> ;
    schema:description "The mint at the ancient site of Tiryns in Argolis."@und .

<http://www.wikidata.org/entity/Q217379> a geojson:Feature ;
    rdfs:label "Tiryns"@und ;
    skos:closeMatch <http://nomisma.org/id/tiryns>,
        <https://pleiades.stoa.org/places/570740>,
        <https://www.geonames.org/408652>,
        <https://www.trismegistos.org/place/37671> ;
    schema:description "Ancient city and archaeological site in Argolis, Greece"@und .        
```
The subject resources are the origins of the assertions contained in the dependent triples. Obviously, the graph for Tiryns is not fully connected.

## What next?

Lots could be done with this. The first thing I'm thinking about doing is reasoning across the graph to find all the unique resources that relate to a given Pleiades resource and then script additions to Pleiades for those that are not currently part of the Pleiades references scheme. This will want some error checking (e.g., if multiple Pleiades IDs show in a reference graph, what's going on?) and some supervision. 

## How?

### Script Convert Sidebar LPF to RDF TTL: `scripts/generate_graph_from_sidebar_json.py`

```
python scripts/generate_graph_from_sidebar_json.py -v
INFO:root:logging level changed to INFO via command line option; was WARNING
INFO:SidebarDataset:Loaded 5000 JSON files so far...
INFO:SidebarDataset:Loaded 10000 JSON files so far...
INFO:SidebarDataset:Loaded 15000 JSON files so far...
INFO:SidebarDataset:Loaded 20000 JSON files so far...
INFO:SidebarDataset:Loaded a total of 23955 JSON files.
WARNING:SidebarDataset:Empty title for PID 79726
{'@id': 'https://edh.ub.uni-heidelberg.de/edh/geographie/G031958',
 'links': [{'identifier': 'https://pleiades.stoa.org/places/79726',
            'type': 'closeMatch'},
           {'identifier': 'https://www.geonames.org/2635202',
            'type': 'closeMatch'}],
 'properties': {'reciprocal': False, 'summary': None, 'title': ''},
 'type': 'Feature'}
INFO:SidebarDataset:Processed 5000 inbound items so far...
INFO:SidebarDataset:Processed 10000 inbound items so far...
INFO:SidebarDataset:Processed 15000 inbound items so far...
INFO:SidebarDataset:Processed 20000 inbound items so far...
INFO:SidebarDataset:Processed 25000 inbound items so far...
INFO:SidebarDataset:Processed 30000 inbound items so far...
INFO:SidebarDataset:Processed 35000 inbound items so far...
INFO:SidebarDataset:Processed 40000 inbound items so far...
INFO:SidebarDataset:Processed 45000 inbound items so far...
INFO:SidebarDataset:Processed 50000 inbound items so far...
INFO:SidebarDataset:Processed 55000 inbound items so far...
INFO:SidebarDataset:Processed 60000 inbound items so far...
INFO:SidebarDataset:Processed 65000 inbound items so far...
WARNING:SidebarDataset:Empty title for PID 207549
{'@id': 'https://edh.ub.uni-heidelberg.de/edh/geographie/G015043',
 'links': [{'identifier': 'https://pleiades.stoa.org/places/207549',
            'type': 'closeMatch'},
           {'identifier': 'https://www.geonames.org/786827',
            'type': 'closeMatch'},
           {'identifier': 'https://www.trismegistos.org/place/29649',
            'type': 'closeMatch'}],
 'properties': {'reciprocal': False, 'summary': None, 'title': ''},
 'type': 'Feature'}
INFO:SidebarDataset:Processed 70000 inbound items so far...
INFO:SidebarDataset:Processed 75000 inbound items so far...
INFO:SidebarDataset:Processed 80000 inbound items so far...
INFO:SidebarDataset:Processed 85000 inbound items so far...
INFO:SidebarDataset:Processed 90000 inbound items so far...
INFO:SidebarDataset:Processed 95000 inbound items so far...
INFO:SidebarDataset:Processed a total of 99763 inbound items.
INFO:SidebarDataset:Graph has 352428 triples.
WARNING:__main__:Output file already exists: /Users/paregorios/Documents/files/P/pleiades_sidebar_graph/data/sidebar_graph.ttl. Backing up to /Users/paregorios/Documents/files/P/pleiades_sidebar_graph/data/sidebar_graph.ttl.bak.
```

Most of the script's functionality is provided by the `SidebarDataset` class defined in `src/pleiades_sidebar_graph/sidebar.py`.

### Script to get stats from an RDF file

The `graph_stats.py` script loads an RDF graph using `rdflib` and then converts it to a `networkx` `graph` and then prints out a bunch of statistics on it as provided by those tools and a bit of code. 

```
python scripts/graph_stats.py data/sidebar_graph.ttl
Stats from rdflib
--------------------------------------------------------------------------------
  Statements: 352,428
  Subjects: 352,428
  Unique Subjects: 79,652
  Unique Subject Netlocs:
    - atlas.paths-erc.eu
    - chronique.efa.gr
    - edh.ub.uni-heidelberg.de
    - itiner-e.org
    - nomisma.org
    - p-lod.org
    - pleiades.stoa.org
    - resource.manto.unh.edu
    - romeresearchgroup.org
    - topostext.org
    - vici.org
    - whgazetteer.org
    - www.wikidata.org
  Predicates: 352,428
  Unique Predicates: 5
  Unique Predicate Values:
    - rdf:type
    - rdfs:label
    - schema:description
    - skos:closeMatch
    - skos:relatedMatch
  Objects: 352,428
  Unique Objects: 152,437
  Unique Object Netlocs (not in subject netlocs):
    - 
    - catalogue.bnf.fr
    - collection.britishmuseum.org
    - d-nb.info
    - dare.ht.lu.se
    - dbpedia.org
    - en.wikipedia.org
    - gazetteer.dainst.org
    - id.loc.gov
    - ikmk.smb.museum
    - isni.org
    - omnesviae.org
    - palp.art
    - pompeiiinpictures.com
    - purl.org
    - slsgazetteer.org
    - sws.geonames.org
    - tesauros.mecd.es
    - viaf.org
    - vocab.getty.edu
    - wikidata.org
    - www.britishmuseum.org
    - www.dbpedia.org
    - www.freebase.com
    - www.geonames.org
    - www.idref.fr
    - www.livius.org
    - www.pompeiiinpictures.com
    - www.trismegistos.org

Stats from networkx
--------------------------------------------------------------------------------
  Edges: 332,522
  Nodes: 198,459
  Density: 1
  Degree (maximum): 66,457
  Degree (minimum): 1
  Degree (average): 3.35

```

## Roadmap

See "What's next" above. And:

- [ ] `geojson:Feature` is an artifact of the LPF source of the data and it's not actually accurate for how I want to use it here. Probably best to redfine these as some sort of documents about places (Pleiades makes this distinction in its RDF, but not all of the others do, because not all of them even have RDF).
- [ ] could flesh out the Pleiades subjects by grabbing titles and summaries from the existing Pleiades RDF.
- [ ] could fix "und" language/script on some literals by pulling from original project RDF, but why given current use cases?
- [ ] an early fun reasoning test might be to generate reports of (a) resources that a Pleiades place resource links to but that don't reciprocate, and (b) external resources that reference a Pleiades resource, but Pleiades doesn't reciprocate.