import os
import argparse
import re


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
PROVIDERS_DIR = SCRIPT_DIR
SMOKERS_DIR_NAME = "smokers"
SMOKERS_FNAME_RE = r"^[^_]+_[^_]+.*.py$"

from welcome import home


def list_smoker_providers():
    smoker_providers = os.listdir(PROVIDERS_DIR)
    smoker_providers = map(lambda x: os.path.join(PROVIDERS_DIR, x), smoker_providers)
    smoker_providers = filter(lambda x: os.path.isdir(x), smoker_providers)
    smoker_providers = filter(lambda x: not os.path.basename(x).startswith("__"), smoker_providers)
    return list(map(lambda x: os.path.basename(x), smoker_providers))


def list_smokers_fnames(smoker_provider):
    smokers = os.listdir(os.path.join(SCRIPT_DIR, smoker_provider, SMOKERS_DIR_NAME))
    return list(filter(lambda x: re.match(SMOKERS_FNAME_RE, x), smokers))


def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def get_class_name_from_smoker_name(smoker_name):
    components = smoker_name.split("_")
    return ''.join(x.title() for x in components) + "Smoker"


def run_smoker(smoker_provider, smoker_name):
    smoker_class = get_class_name_from_smoker_name(smoker_name)
    exec(f"from {smoker_provider}.smokers.{smoker_name} import {smoker_class}")
    eval(f"{smoker_class}().simulate()")


def main(smoker_provider, smoker_name, to_bucket, run_all):
    # TODO: implement 'to_bucket'
    if run_all:
        smoker_names = list_smokers_fnames(smoker_provider)
        smoker_names = [x[:-3] for x in smoker_names]
    else:
        smoker_names = [smoker_name]

    for smoker_name in smoker_names:
        run_smoker(smoker_provider, smoker_name)


if __name__ == "__main__":
    home()
    msg = (
        "Cloud Droid is a redteam-as-a-code tool for Incident Response Automated Simulations.\n"
        "The goal is to evaluate the security posture of cloud environments generating different real security findings.\n"
        "https://github.com/cloud-sniper/cloud-droid"
    )
    print(msg)
    print()

    parser = argparse.ArgumentParser(
        description="Cloud Droid smoker test executor."
    )
    # TODO: remove hardcoded version
    argparse.version="version: 2.0 - https://github.com/cloud-sniper/cloud-droid"
    parser.add_argument(
        "smoker_provider", help="smoker provider, the smoker provider is the family name for the smoker. Example: aws", choices=list_smoker_providers(),
    )
    smoker_name_arg = parser.add_argument(
        "smoker_name",
        nargs='?',
        default="",
        help="Name of the smoker to be executed. Example: s3_public"
    )
    parser.add_argument(
        "-a",
        "--all",
        help="Run all smokers for the given smoker_provider",
        action='store_true',
    )
    args = parser.parse_args()

    #validate smoker name:
    smokers_fnames = list_smokers_fnames(args.smoker_provider)
    smokers_names = [x[:-3] for x in smokers_fnames]
    if args.smoker_name == "":
        if not args.all:
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
    main(args.smoker_provider, args.smoker_name, args.bucket, args.all)
