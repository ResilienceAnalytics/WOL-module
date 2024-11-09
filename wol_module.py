import socket  # Standard library import for network communication
import yaml  # Library to parse YAML configuration files
from mock_mqtt_client import MockMQTTClient  # Importing the mock MQTT client for testing

def load_machines_config(config_path="machines.yaml"):
    """
    Load machine configurations from a YAML file.
    
    Args:
        config_path (str): Path to the YAML configuration file, default is 'machines.yaml'.
    
    Returns:
        dict: Dictionary containing machine configurations with each entry's MAC and optional IP addresses.
    """
    try:
        # Open and read the configuration file
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)  # Parse YAML into a dictionary
        return config.get("machines", {})  # Return the 'machines' dictionary or empty if not found
    except FileNotFoundError:
        print(f"[ERROR] Configuration file '{config_path}' not found.")
        return {}
    except yaml.YAMLError as e:
        print(f"[ERROR] Failed to parse YAML file: {e}")
        return {}

def send_wol_packet(mac_address):
    """
    Send a Wake-on-LAN (WOL) magic packet to the specified MAC address.
    
    Args:
        mac_address (str): MAC address of the target machine to wake.
    """
    try:
        # Convert MAC address to binary without colons (e.g., "00:1A:2B..." -> b'\x00\x1A\x2B...')
        mac_bytes = bytes.fromhex(mac_address.replace(":", ""))
        # Create magic packet: 6 bytes of 0xFF followed by the MAC address repeated 16 times
        packet = b'\xff' * 6 + mac_bytes * 16
        
        # Open socket to send packet over the network
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Enable broadcast on socket
            sock.sendto(packet, ('<broadcast>', 9))  # Broadcast packet to all devices on port 9
        print(f"[INFO] WOL packet sent to MAC address {mac_address}.")
    except Exception as e:
        print(f"[ERROR] Failed to send WOL packet to {mac_address}: {e}")

def handle_wol_command(machine_name, client, config_path="machines.yaml"):
    """
    Handle WOL command to send a magic packet to a specified machine by its name.
    
    Args:
        machine_name (str): Name of the machine to wake.
        client (MockMQTTClient): MQTT client instance used for messaging.
        config_path (str): Path to the YAML configuration file, default is 'machines.yaml'.
    """
    machines = load_machines_config(config_path)  # Load machine configurations
    machine = machines.get(machine_name)  # Find machine by name

    # Check if machine exists and has a MAC address
    if machine and "mac" in machine:
        mac_address = machine["mac"]
        send_wol_packet(mac_address)  # Send WOL packet to specified MAC
        # Notify success
        client.publish("GHBot/to/irc/channel/privmsg", f"Wake-on-LAN packet sent to {machine_name}.")
    else:
        # Publish error message if machine not found or lacks MAC address
        client.publish("GHBot/to/irc/channel/privmsg", f"Machine '{machine_name}' not found or lacks a MAC address.")
        print(f"[WARN] WOL attempt failed: Machine '{machine_name}' not found or no MAC address provided.")

# Initialize MQTT client and register the WOL command
mqtt_client = MockMQTTClient("GHBot_WOL_Client")
mqtt_client.connect("broker_address")  # Replace with actual broker address as needed
mqtt_client.register_command("wol", handle_wol_command)
