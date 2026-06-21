import json                  # Used to read the JSON event file
import os                    # Used for file path handling
from dynamicLoader import loader   # Your dynamic module loader


# ---------------------------------------------------------
# Context Class
# ---------------------------------------------------------
# This object carries data between all steps in a chain
# Each chain gets its own independent Context instance
# ---------------------------------------------------------
class Context:
    def __init__(self):
        self.data = {}              # Shared data storage
        self.status = "running"     # running / cancelled / done


# ---------------------------------------------------------
# Event Manager
# ---------------------------------------------------------
# Responsibilities:
# 1. Load event chains from JSON
# 2. Execute steps in order
# 3. Pass shared context between steps
# ---------------------------------------------------------
class EventManager:
    def __init__(self):

        # Root = /bin directory
        self.root = os.path.dirname(os.path.abspath(__file__))

        # Path to event database
        self.events_path = os.path.join(self.root, "Engine", "events.json")

        # Load event definitions into memory
        self.events = self.load_events()


        # Persistent app context
        self.app_context = Context()


        print("EVENTS IN MEMORY:", self.events)


    # ---------------------------------------------------------
    # Load JSON event file
    # ---------------------------------------------------------
    def load_events(self):

        print("EVENT FILE PATH:", self.events_path)

        # If file doesn't exist → return empty system
        if not os.path.exists(self.events_path):
            print("events.json not found")
            return {}

        # Read JSON file
        with open(self.events_path, "r") as f:
            data = json.load(f)

        print("LOADED JSON:", data)

        return data


    # ---------------------------------------------------------
    # Run a specific event chain
    # ---------------------------------------------------------
    def run_chain(self, chain_name):

        # Check if chain exists in JSON
        if chain_name not in self.events:
            print(f"Chain not found: {chain_name}")
            return

        # Create fresh context for this run
        #context = Context()
        context = self.app_context

        # Get step list
        chain = self.events[chain_name]

        # Execute steps in order
        for step_name in chain:

            # Load module dynamically
            module = loader.load(step_name)

            # Validate module
            if not module or not hasattr(module, "step"):
                print(f"Invalid step: {step_name}")
                break

            # Execute step
            result = module.step(context)

            # Handle flow control
            if result == "next":
                continue

            elif result == "stop":
                break

            elif result == "error":
                print(f"Error in step: {step_name}")
                break

            # External cancellation check
            if context.status == "cancelled":
                print("Chain cancelled")
                break

        print("Chain finished")


# ---------------------------------------------------------
# Singleton instance (global access point)
# ---------------------------------------------------------
event_manager = EventManager()