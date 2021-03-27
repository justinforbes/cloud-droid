import os
import re
import sys
import json
import requests

import argparse
import jinja2

from typing import Dict, List


WORKING_DIR = os.path.dirname(os.path.realpath(__file__))
SMOKERS_DIR = os.path.join(WORKING_DIR, "..", "src", "smokers")
SMOKERS_FNAME_RE = r"^[^_]+_[^_]+.*.py$"


def process_feature(  # nosec
    external: bool,
    table_name: str,
    start_date_time: str = "",
    end_date_time: str = "",
    token: str = "",
) -> None:
    """Main function to process in Databricks a feature

    Args:
        table_name (str): the table that be backfilled
        start_date_time (str): the start date, as YYYYMMDDHHMM
        end_date_time (str): the end date, as YYYYMMDDHHMM
        external (bool): True if this is not a feature but external source
        token (str): your databricks API token
    """
    deps_fname = os.path.join(DEPS_DIR, table_name + ".yaml")
    if not external and not os.path.exists(deps_fname):
        deps_fname = os.path.join(DEPS_DIR, table_name + ".yml")
        if not os.path.exists(deps_fname):
            raise IOError(
                f"Feature {table_name} does not have a config "
                f"file in {DEPS_DIR} folder. If it's an "
                f"external source, run it with option -e."
            )
    deps, _ = get_dependencies_from_configs(DEPS_DIR, False)
    depending_features = _get_dependencies_for_table(deps, table_name)
    _print_dependencies_info(depending_features)
    if external:
        print("This is an external source, cannot run databricks job on it...")
    elif start_date_time and end_date_time and token:
        _run_feature(table_name, start_date_time, end_date_time, token)


def parse_smoker_names(smoker_fname):
    smoker_name = smoker_fname[:-3]
    split = smoker_name.split("_")
    return split[0], "_".join(split[1:])


def get_class_name_from_args(service_name, smoker_action):
    return (
        f"{service_name.title()}"
        f"{smoker_action.title().replace('_', '')}"
        "Smoker"
    )


def list_cloud_providers():
    cloud_providers = os.listdir(SMOKERS_DIR)
    cloud_providers = map(lambda x: os.path.join(SMOKERS_DIR, x), cloud_providers)
    cloud_providers = filter(lambda x: os.path.isdir(x), cloud_providers)
    return map(lambda x: os.path.basename(x), cloud_providers)


def list_existing_services(cloud_provider):
    smokers = os.listdir(os.path.join(SMOKERS_DIR, cloud_provider))
    smokers = filter(lambda x: re.match(SMOKERS_FNAME_RE, x), smokers)
    parsed_smokers = map(parse_smoker_names, smokers)
    return [name[0] for name in parsed_smokers]


def check_service_name(value):
    if value.lower() != value:
        raise argparse.ArgumentTypeError(f"service_name {value} should be in lower case")
    if "_" in value:
        raise argparse.ArgumentTypeError(f"service_name {value} cannot have '_' characters")
    return value


def check_smoker_action(value):
    if value.lower() != value:
        raise argparse.ArgumentTypeError(f"smoker_action {value} should be in lower case")
    return value


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create the template to implement your own smoker.",
    )
    parser.add_argument(
        "cloud_provider",
        help="Cloud provider",
        choices=list(list_cloud_providers()),
    )
    parser.add_argument(
        "service_name",
        type=check_service_name,
        help="Name of the service you want your smoker for. Examples: s3, cloudtrail",
    )
    parser.add_argument(
        "smoker_action",
        type=check_smoker_action,
        help="Name of the action the smoker will perform",
    )
    args = parser.parse_args(sys.argv[1:])
    existing_services = list_existing_services(args.cloud_provider)
    print()
    print(args.cloud_provider)
    print(args.service_name)
    print(args.smoker_action)
    print(existing_services)
    print()
    if (args.service_name not in existing_services):
        nl = "\n"
        bullet = f"{nl} *"
        print(f"There are no smokers for the service {args.service_name}. "
              f"All the services we have are: {bullet.join(existing_services)}"
              f"{nl}{nl}Do you still want to continue with {args.service_name}? (y/n)")
        yes = {'yes', 'y'}
        no = {'no', 'n'}
        while True:
            choice = raw_input().lower()
            if choice in no:
                break
            elif choice in no:
                sys.stderr.write("Aborting...")
                sys.exit(1)
            else:
                sys.stdout.write("Please respond with 'y' or 'n'")

    class_name = get_class_name_from_args(args.service_name, args.smoker_action)
    print()
    print(f"Class created: {class_name}")
    fname = os.path.join(SMOKERS_DIR, args.cloud_provider, f"{args.service_name}_{args.smoker_action}.py")
    print(f"File created: {os.path.relpath(fname)}")
