# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rapidfuzz import process
import logging

# Enable logging
logger = logging.getLogger(__name__)

class ActionserviceInfo(Action):

    services_info = {
        "Martech & Mobile Marketing Solutions": "utter_service_info_martech",
        "SalesTech for FMCG": "utter_service_info_salestech",
        "ImmersaLearn - VR-Based Training Platform": "utter_service_info_immersalearn",
        "Custom Development Solutions": "utter_service_info_engineering",
        "Smart Enterprise Solutions": "Advanced solutions to improve enterprise efficiency and productivity.",
        "AR/VR Simulations": "Augmented and Virtual Reality simulations for training and business applications."
    }

    def name(self) -> Text:
        return "action_service_info"

    def find_closest_match(self, service: str) -> str:
        """Find the closest matching service name from the dictionary keys."""
        match = process.extractOne(service, self.services_info.keys(), score_cutoff=50)
        return match if match else None

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        logger.info("Executing action_service_info...")

        # Extract service entity
        services = [e['value'] for e in tracker.latest_message.get('entities', []) if e['entity'] == 'service']
        logger.info(f" Extracted services: {services}")

        if services:
            for service in services:
                match = self.find_closest_match(service)
                if match:
                    logger.info(f"match score: {match[1]}")
                    dispatcher.utter_message(response= self.services_info[match[0]])
                else:
                    dispatcher.utter_message(text=f" Sorry, I couldn't find a service similar to '{service}'. Please try again.")
        else:
            dispatcher.utter_message(text="I didn't understand which service you're asking about. Could you rephrase?")
        
        
        return []
