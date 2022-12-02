import argparse
import sys
import yaml
from transformer import Transformer


def get_arg_parse_object(args):
    parser = argparse.ArgumentParser(description="Receiver")
    parser.add_argument('--global-config-file', type=str, help="Based on manycore-mail-global.yaml.", required=True)
    # v1.5 parser.add_argument('--beacon-url', type=str, help='If we want to inject beacons. ex: https://example.com/1-1234-234', required=False)
    parser.add_argument('--fernet-keyfile', type=str, help="Binary file with a Fernet symmetrical key.", required=True)
    parser.add_argument('--return-path-domain', type=str, help="The domain for the message id.", required=True)
    parser.add_argument('--dkim-private-key-file', type=str, help="Private key for signing dkim", required=True)
    return parser.parse_args()


if __name__ == "__main__":
    args = get_arg_parse_object(sys.argv[1:])
    with open(args.global_config_file, 'r') as file:
        global_config = yaml.safe_load(file)

    primary_queue = global_config["reliable-queue"]["queue-names"]["primary-queue"]
    default_queue = global_config["reliable-queue"]["queue-names"]["default-queue"]

    beacon_url = None  # args.beacon_url

    with open(args.fernet_keyfile, "rb") as keyfile:
        fernet_key = keyfile.read()

    with open(args.dkim_private_key_file) as fh:
        dkim_private_key = fh.read()

    return_path_domain = args.return_path_domain

    transformer = Transformer(primary_queue, default_queue, beacon_url, fernet_key, return_path_domain, dkim_private_key)
    transformer.run()
