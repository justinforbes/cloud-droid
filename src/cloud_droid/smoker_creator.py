import os
import re
import argparse

from droid import (
    list_cloud_providers,
    list_smokers_fnames,
    get_class_name_from_smoker_name,
    SMOKERS_DIR_NAME
)

from jinja2 import Template
from welcome import home


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_FNAME = "template.py.jinja2"
SMOKERS_NAME_RE = r"^[a-z0-9]+_[a-z0-9_]+$"


def smoker_name_type(value):
    # Regex check
    if not re.match(SMOKERS_NAME_RE, value):
        raise argparse.ArgumentTypeError("should be lower case with a '_' like 'service_functionality'")
    return value


def main(cloud_provider, smoker_name):
    template_fpath = os.path.join(SCRIPT_DIR, cloud_provider, TEMPLATE_FNAME)
    smoker_dir = os.path.join(SCRIPT_DIR, cloud_provider, SMOKERS_DIR_NAME)
    output_fpath = os.path.join(smoker_dir, f"{smoker_name}.py")
    output_config_fpath = os.path.join(smoker_dir, f"{smoker_name}.yaml")

    with open(template_fpath) as fd:
        template = Template(fd.read())

        with open(output_fpath, "w") as output_fd:
            smoker_class_name = get_class_name_from_smoker_name(smoker_name)
            output_fd.write(template.render(
                smoker_class_name=smoker_class_name,
                smoker_name=smoker_name
            ))

        with open(output_config_fpath, "w") as output_fd:
            output_fd.write('my_variable: "variable_value"')

    print(f"\nSmoker to be implemented can be found here "
          f"{os.path.relpath(output_fpath)}\nand the corresponding config "
          f"here {os.path.relpath(output_config_fpath)}\n")


if __name__ == "__main__":
    home()
    msg = (
        "Cloud Droid smokers generator tool.\n "
        "https://github.com/cloud-sniper/cloud-droid"
    )
    print(msg)
    print()

    parser = argparse.ArgumentParser(
        description="Create your own smoker tests."
    )
    # TODO: remove hardcoded version
    argparse.version="version: 2.0 - https://github.com/cloud-sniper/cloud-droid"
    parser.add_argument(
        "cloud_provider", help="Cloud provider", choices=list_cloud_providers(),
    )
    smoker_name_arg = parser.add_argument(
        "smoker_name",
        default="",
        type=smoker_name_type,
        help="Name of the smoker to be created. Example: s3_public",
    )
    args = parser.parse_args()

    #validate smoker name:
    smokers_fnames = list_smokers_fnames(args.cloud_provider)
    smokers_names = [x[:-3] for x in smokers_fnames]
    if args.smoker_name in smokers_names:
        raise argparse.ArgumentError(
            smoker_name_arg,
            f"{args.smoker_name} already exists"
        )
    main(args.cloud_provider, args.smoker_name)
