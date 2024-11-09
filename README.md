# Wake-on-LAN (WOL) Module for GHBot

This module provides a Wake-on-LAN (WOL) command to remotely power on machines in the network. Built with modularity in mind, it uses MQTT messaging to communicate with GHBot, allowing commands to be issued via IRC.

## Features

- **Wake-on-LAN (WOL) Command**: Sends a WOL "magic packet" to specified machines.
- **Modular Configuration**: Reads machine configurations (MAC and IP addresses) from a YAML file for easy updates.
- **MQTT Integration**: Communicates over MQTT topics for seamless interaction with GHBot.
- **Error Handling**: Graceful error messages when a machine cannot be found or lacks a MAC address.

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ResilienceAnalytics/WOL-module.git
   cd YourRepo
   ```

2. **Dependencies**
   - Install required Python libraries with:
     ```bash
     pip install pyyaml
     ```

3. **Configuration**  
   - Configure machines and their MAC addresses in `machines.yaml`:
     ```yaml
     machines:
       serveur-dev:
         mac: "00:1A:2B:3C:4D:5E"
         ip: "192.168.1.100"
         description: "Development server"
         location: "Server Room"
       imprimante-3D:
         mac: "11:22:33:44:55:66"
         ip: "192.168.1.101"
         description: "3D printer"
         location: "Workshop"
     ```
   - Edit the MQTT broker and GHBot settings if necessary.

4. **Run the Test**
   - To verify functionality, run:
     ```bash
     python test_wol.py
     ```

## Usage

### Commands

1. **Wake-on-LAN Command**
   - Syntax: `!wol <machine_name>`
   - Example: `!wol serveur-dev`
   - Description: Sends a WOL packet to the specified machine using its MAC address.

2. **Configuration Reload**
   - To update machine configurations, simply modify `machines.yaml` and restart the module.

### MQTT Topics

- **To send WOL requests**: Publishes to `GHBot/to/irc/channel/privmsg`.
- **To respond with errors**: Publishes error messages to the same topic with an explanation.

## Code Structure

- **`wol_module.py`**: Main module for WOL functionality.
- **`machines.yaml`**: Contains machine information including MAC and IP addresses.
- **`mock_mqtt_client.py`**: Mock MQTT client for testing.
- **`test_wol.py`**: Automated test for the WOL module.

## Testing

1. **Run Tests**
   - Execute `test_wol.py` to test functionality. This script checks:
     - Sending a WOL packet to a valid machine.
     - Error handling for invalid machine names.

   Sample output:
   ```plaintext
   [CONNECT] GHBot_WOL_Client connecting to broker at broker_address (Simulated)
   [REGISTER] Command 'wol' registered.

   --- Testing Wake-on-LAN Command ---
   [INFO] WOL packet sent to MAC address 00:1A:2B:3C:4D:5E.
   [PUBLISH] Test_WOL_Client | Topic: GHBot/to/irc/channel/privmsg | Message: Wake-on-LAN packet sent to serveur-dev.

   --- Testing with Invalid Machine Name ---
   [PUBLISH] Test_WOL_Client | Topic: GHBot/to/irc/channel/privmsg | Message: Machine 'unknown-machine' not found or lacks a MAC address.
   [WARN] WOL attempt failed: Machine 'unknown-machine' not found or no MAC address provided.
   ```

## Additional Notes

- **Modular Design**: The configuration and MQTT client are separate from the main module to allow flexibility in test environments versus production.
- **Compatibility**: Tested with GHBot on IRC, adaptable to other MQTT-compatible environments.

## Contribution

Feel free to open issues and submit pull requests to enhance functionality or suggest new features!


