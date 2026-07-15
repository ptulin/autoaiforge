import argparse
import json
import sys
import logging
from scapy.all import sniff, IP
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from colorama import Fore, Style

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def load_ai_model(model_path):
    """Load the pre-trained anomaly detection model."""
    try:
        model = load_model(model_path)
        logging.info("AI model loaded successfully.")
        return model
    except Exception as e:
        logging.error(f"Failed to load AI model: {e}")
        sys.exit(1)

def process_packet(packet, model, log_file):
    """Process a single packet and detect anomalies."""
    if IP in packet:
        packet_data = [ord(char) for char in str(packet[IP])[:100]]  # Convert packet to numeric data
        packet_data = pad_sequences([packet_data], maxlen=100, padding='post')

        # Predict using the AI model
        prediction = model.predict(packet_data, verbose=0)
        if prediction[0][0] > 0.5:  # Assuming 0.5 is the anomaly threshold
            alert = f"{Fore.RED}[ALERT]{Style.RESET_ALL} Suspicious activity detected! Source: {packet[IP].src}, Destination: {packet[IP].dst}"
            print(alert)

            if log_file:
                try:
                    with open(log_file, 'a') as log:
                        log_entry = {
                            "source": packet[IP].src,
                            "destination": packet[IP].dst,
                            "alert": "Suspicious activity detected"
                        }
                        log.write(json.dumps(log_entry) + '\n')
                except Exception as e:
                    logging.error(f"Failed to write to log file: {e}")

def monitor_traffic(interface, model, log_file):
    """Monitor live network traffic on the specified interface."""
    try:
        sniff(iface=interface, prn=lambda x: process_packet(x, model, log_file), store=False)
    except PermissionError:
        logging.error("Permission denied. Please run the script as root or with sufficient privileges.")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Error occurred while monitoring traffic: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Live Threat Monitor: Monitor live network traffic for suspicious activity.")
    parser.add_argument('--interface', required=True, help="Network interface to monitor (e.g., eth0)")
    parser.add_argument('--model', required=True, help="Path to the pre-trained AI model")
    parser.add_argument('--log', help="Optional path to save JSON log of detected threats")
    args = parser.parse_args()

    model = load_ai_model(args.model)
    monitor_traffic(args.interface, model, args.log)

if __name__ == "__main__":
    main()