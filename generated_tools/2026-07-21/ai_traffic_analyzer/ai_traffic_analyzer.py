import argparse
import json
from scapy.all import sniff, rdpcap
import pandas as pd
from sklearn.ensemble import IsolationForest


def analyze_traffic(packets):
    """
    Analyze network packets using an Isolation Forest model to detect anomalies.

    Args:
        packets (list): List of scapy packets.

    Returns:
        list: List of detected anomalies with their details.
    """
    # Extract features from packets
    data = []
    for packet in packets:
        if hasattr(packet, 'time') and hasattr(packet, 'len'):
            data.append({
                'time': packet.time,
                'length': len(packet),
                'src': packet[0][1].src if packet.haslayer(1) else 'unknown',
                'dst': packet[0][1].dst if packet.haslayer(1) else 'unknown'
            })

    df = pd.DataFrame(data)

    if df.empty:
        return []  # No data to analyze

    # Use only numerical features for anomaly detection
    numerical_features = df[['time', 'length']]

    # Train Isolation Forest model
    model = IsolationForest(contamination=0.01, random_state=42)
    model.fit(numerical_features)

    # Predict anomalies
    df['anomaly'] = model.predict(numerical_features)

    # Extract anomalies
    anomalies = df[df['anomaly'] == -1]
    return anomalies.to_dict(orient='records')


def monitor_interface(interface, output):
    """
    Monitor network traffic on a given interface and detect anomalies.

    Args:
        interface (str): Network interface to monitor.
        output (str): Output file to save the threat report.
    """
    try:
        packets = sniff(iface=interface, count=100, timeout=10)  # Capture 100 packets or timeout after 10 seconds
        anomalies = analyze_traffic(packets)

        if output:
            with open(output, 'w') as f:
                json.dump(anomalies, f, indent=4)
        else:
            print(json.dumps(anomalies, indent=4))

    except Exception as e:
        print(f"Error: {e}")


def analyze_pcap(file_path, output):
    """
    Analyze a PCAP file for anomalies.

    Args:
        file_path (str): Path to the PCAP file.
        output (str): Output file to save the threat report.
    """
    try:
        packets = rdpcap(file_path)
        anomalies = analyze_traffic(packets)

        if output:
            with open(output, 'w') as f:
                json.dump(anomalies, f, indent=4)
        else:
            print(json.dumps(anomalies, indent=4))

    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    except Exception as e:
        print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="AI Traffic Analyzer: Detect anomalies in network traffic.")
    parser.add_argument('--interface', type=str, help="Network interface to monitor (e.g., eth0).")
    parser.add_argument('--pcap', type=str, help="Path to a PCAP file for offline analysis.")
    parser.add_argument('--output', type=str, help="Path to save the threat report as a JSON file.")

    args = parser.parse_args()

    if args.interface and args.pcap:
        print("Error: Please specify either --interface or --pcap, not both.")
    elif args.interface:
        monitor_interface(args.interface, args.output)
    elif args.pcap:
        analyze_pcap(args.pcap, args.output)
    else:
        print("Error: Please specify either --interface or --pcap.")


if __name__ == "__main__":
    main()