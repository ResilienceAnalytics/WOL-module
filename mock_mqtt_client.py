class MockMQTTClient:
    """
    A simulated MQTT client for testing local command publishing and subscription.
    
    Attributes:
    ----------
    client_id : str
        Unique identifier for the client instance, used for tracking and logging.
    broker : str
        Simulated broker URL (used only for display).
    subscriptions : dict
        Dictionary to store subscribed topics and associated callback functions.
    commands : dict
        Dictionary to store registered commands and their handlers.
    """

    def __init__(self, client_id):
        """
        Initializes the MockMQTTClient with a unique client ID.
        
        Parameters:
        ----------
        client_id : str
            Unique identifier for the MQTT client instance.
        """
        self.client_id = client_id
        self.broker = None
        self.subscriptions = {}  # Stores topic-callback pairs
        self.commands = {}       # Stores commands and handlers

    def connect(self, broker):
        """
        Simulates a connection to an MQTT broker.
        
        Parameters:
        ----------
        broker : str
            The broker address to "connect" to (simulation).
        """
        self.broker = broker
        print(f"[CONNECT] {self.client_id} connecting to broker at {broker} (Simulated)")

    def disconnect(self):
        """
        Simulates a disconnection from the MQTT broker.
        """
        print(f"[DISCONNECT] {self.client_id} disconnected from broker at {self.broker} (Simulated)")
        self.broker = None

    def publish(self, topic, message):
        """
        Simulates publishing a message to a specified topic.
        
        Parameters:
        ----------
        topic : str
            The topic to publish the message to.
        message : str
            The message content to be published.
        """
        print(f"[PUBLISH] {self.client_id} | Topic: {topic} | Message: {message}")
        
        # Trigger callbacks for any subscribers to this topic
        if topic in self.subscriptions:
            for callback in self.subscriptions[topic]:
                callback(message)

    def subscribe(self, topic, callback):
        """
        Simulates subscribing to a specified topic.
        
        Parameters:
        ----------
        topic : str
            The topic to subscribe to.
        callback : function
            A callback function to execute when a message is published to the topic.
        """
        if topic not in self.subscriptions:
            self.subscriptions[topic] = []
        self.subscriptions[topic].append(callback)
        print(f"[SUBSCRIBE] {self.client_id} subscribed to topic: {topic}")

    def unsubscribe(self, topic):
        """
        Simulates unsubscribing from a specified topic.
        
        Parameters:
        ----------
        topic : str
            The topic to unsubscribe from.
        """
        if topic in self.subscriptions:
            del self.subscriptions[topic]
            print(f"[UNSUBSCRIBE] {self.client_id} unsubscribed from topic: {topic}")
        else:
            print(f"[UNSUBSCRIBE] {self.client_id} tried to unsubscribe from topic: {topic}, but was not subscribed.")

    def register_command(self, command, handler):
        """
        Registers a command with an associated handler function.
        
        Parameters:
        ----------
        command : str
            The command name to register.
        handler : callable
            The function that will handle this command.
        """
        self.commands[command] = handler
        print(f"[REGISTER] Command '{command}' registered.")
