import sys
from typing import Any, Text, Dict, List

from SPARQLWrapper import SPARQLWrapper, JSON
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

sys.path.append("/Users/kalpafernando/PycharmProjects/resbot/actions/submodules")


# knowledge graph connection

class QueryKnowledgeGraph(Action):
    def name(self) -> Text:
        return "action_query_knowledge_graph"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the entity value from user input
        entity = tracker.latest_message['entities'][0]['value']

        # Create a SPARQL query to retrieve relevant information from the knowledge graph
        query = f"""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX schema: <http://schema.org/>
            SELECT ?description
            WHERE {{
                ?entity rdfs:label "{entity}"@en ;
                        schema:description ?description .
            }}
        """

        # Send the query to the knowledge graph using the SPARQLWrapper library
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        # Extract the information from the query results and send it back to the chatbot
        description = results['results']['bindings'][0]['description']['value']
        dispatcher.utter_message(text=f"The description of {entity} is: {description}")

        return []
