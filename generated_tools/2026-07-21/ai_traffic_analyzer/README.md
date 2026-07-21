# AI Traffic Analyzer

AI Traffic Analyzer is a CLI tool designed to monitor network traffic and detect potential anomalies caused by AI-driven cyberattacks. It uses machine learning techniques to analyze packet data in real-time, identifying unusual patterns indicative of malicious behavior.

## Features

- **Real-time network traffic monitoring**: Analyze live traffic from a specified network interface.
- **AI-based anomaly detection**: Uses a pre-trained Isolation Forest model to detect anomalies.
- **Offline analysis**: Analyze traffic from PCAP files.
- **Threat reporting**: Generates detailed threat reports in JSON format.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd ai_traffic_analyzer
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Monitor a Network Interface

```bash
python ai_traffic_analyzer.py --interface eth0 --output threats.json
```

### Analyze a PCAP File

```bash
python ai_traffic_analyzer.py --pcap traffic.pcap --output threats.json
```

### Print Results to Console

```bash
python ai_traffic_analyzer.py --interface eth0
```

## Requirements

- Python 3.8+
- `scapy==2.4.5`
- `scikit-learn==1.3.0`
- `pandas==2.1.1`

## Limitations

- The tool is designed for educational purposes and may require further tuning for production use.
- Real-time monitoring may require elevated privileges.

## License

This project is licensed under the MIT License.