from wol_module import handle_wol_command  # Import the main WOL command handler
from mock_mqtt_client import MockMQTTClient  # Import the mock MQTT client for local testing

# Initialize the mock client instance for simulating MQTT functionality
client = MockMQTTClient("Test_WOL_Client")

# Define the machine to test with (use a machine name from machines.yaml)
machine_name = "serveur-dev"

# Run the WOL command with a valid machine name
print("\n--- Testing Wake-on-LAN Command ---")
handle_wol_command(machine_name, client)

# Run the WOL command with an invalid machine name to test error handling
invalid_machine_name = "unknown-machine"
print("\n--- Testing with Invalid Machine Name ---")
handle_wol_command(invalid_machine_name, client)
