import argparse
from routeros_api import RouterOsApiPool

def optimize_router(host, user, password, prioritize_ports, bandwidth_limit):
    """
    Automates MikroTik router configuration for optimizing networking setups tailored to large language model (LLM) communication.
    """
    api_pool = None
    try:
        # Connect to the MikroTik router
        api_pool = RouterOsApiPool(host, username=user, password=password, plaintext_login=True)
        api = api_pool.get_api()

        # Parse the ports
        ports = prioritize_ports.split(',')

        # Add firewall mangle rules to mark LLM traffic
        for port in ports:
            api.get_resource('/ip/firewall/mangle').add(
                chain='prerouting',
                protocol='tcp',
                dst_port=port,
                action='mark-connection',
                new_connection_mark=f'llm_conn_{port}',
                passthrough='yes'
            )
            api.get_resource('/ip/firewall/mangle').add(
                chain='prerouting',
                connection_mark=f'llm_conn_{port}',
                action='mark-packet',
                new_packet_mark=f'llm_packet_{port}',
                passthrough='no'
            )

        # Add queue tree for bandwidth management if bandwidth limit is provided
        if bandwidth_limit:
            for port in ports:
                api.get_resource('/queue/tree').add(
                    name=f'llm_queue_{port}',
                    parent='global',
                    packet_mark=f'llm_packet_{port}',
                    max_limit=int(bandwidth_limit) * 1024  # Convert kbps to bps
                )

        print("Router optimization completed successfully.")

    except Exception as e:
        print(f"Error: {e}")
        raise e

    finally:
        if api_pool:
            api_pool.disconnect()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Optimize MikroTik router for LLM communication.")
    parser.add_argument('--host', required=True, help='MikroTik router IP address')
    parser.add_argument('--user', required=True, help='MikroTik username')
    parser.add_argument('--password', required=True, help='MikroTik password')
    parser.add_argument('--prioritize-ports', required=True, help='Comma-separated list of ports to prioritize for LLM traffic')
    parser.add_argument('--bandwidth-limit', default=None, type=int, help='Bandwidth limit for LLM traffic in kbps (e.g., 10000 for 10 Mbps)')

    args = parser.parse_args()

    optimize_router(args.host, args.user, args.password, args.prioritize_ports, args.bandwidth_limit)