import os
import argparse
import re

WORKING_DIR = os.path.dirname(os.path.realpath(__file__))
SMOKERS_DIR = os.path.join(WORKING_DIR, "smokers")
SMOKERS_FNAME_RE = r"^[^_]+_[^_]+.*.py$"

from welcome import home


def list_cloud_providers():
    cloud_providers = os.listdir(SMOKERS_DIR)
    cloud_providers = map(lambda x: os.path.join(SMOKERS_DIR, x), cloud_providers)
    cloud_providers = filter(lambda x: os.path.isdir(x), cloud_providers)
    return list(map(lambda x: os.path.basename(x), cloud_providers))


def list_smokers_fnames(cloud_provider):
    smokers = os.listdir(os.path.join(SMOKERS_DIR, cloud_provider))
    return list(filter(lambda x: re.match(SMOKERS_FNAME_RE, x), smokers))


def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def get_class_name_from_smoker_name(smoker_name):
    components = smoker_name.split("_")
    return ''.join(x.title() for x in components) + "Smoker"


def run_smoker(cloud_provider, smoker_name):
    smoker_class = get_class_name_from_smoker_name(smoker_name)
    print()
    print(smoker_class)
    print()
    exec(f"from smokers.{cloud_provider}.{smoker_name} import {smoker_class}")
    eval(f"{smoker_class}().simulate()")


def main(cloud_provider, smoker_name, to_bucket, run_all):
    # TODO: implement 'to_bucket'
    if run_all:
        smoker_names = list_smokers_fnames(cloud_provider)
    else:
        smoker_names = [smoker_name]

    for smoker_name in smoker_names:
        run_smoker(cloud_provider, smoker_name)


if __name__ == "__main__":
    home()
    msg = (
        "Cloud Droid is the redteam as a code for Incident Response "
        "Automated 'Simulations'.\n This is a simple scripting tool to create "
        "differents TTPs.\n The goal is to generate actual smoke events "
        "and test alerts in your SIEM.\n "
        "https://github.com/cloud-sniper/cloud-droid"
    )
    print(msg)

    parser = argparse.ArgumentParser(
        description="Create the template to implement your own smoker."
    )
    argparse.version="version: 2.0 - https://github.com/cloud-sniper/cloud-droid"
    parser.add_argument(
        "cloud_provider", help="Cloud provider", choices=list_cloud_providers(),
    )
    smoker_name_arg = parser.add_argument(
        "smoker_name",
        default="",
        help="Name of the smoker to be executed. Example: s3_public",
    )
    parser.add_argument(
        "-a",
        "--all",
        help="Run all smokers for the given cloud_provider",
        action='store_true',
    )
    parser.add_argument(
        "-b",
        "--bucket",
        help="save the results into a bucket",
        action='store_true',
    )
    args = parser.parse_args()

    #validate smoker name:
    smokers_fnames = list_smokers_fnames(args.cloud_provider)
    smokers_names = [x[:-3] for x in smokers_fnames]
    if args.smoker_name == "" and not args.all:
        raise argparse.ArgumentError(
            smoker_name_arg,
            f"smoker_name must be set, unless --all option is passed."
        )
    elif args.smoker_name not in smokers_names:
        nl = "\n"
        bullet = f"{nl} *"
        raise argparse.ArgumentError(
            smoker_name_arg,
            f"smoker_name {args.smoker_name} should be one in this list: "
            f"{bullet.join(smokers_names)}"
        )
    main(args.cloud_provider, args.smoker_name, args.bucket, args.all)
