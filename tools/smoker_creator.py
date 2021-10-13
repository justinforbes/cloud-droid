import os
import sys
import argparse
from jinja2 import Template

WORKING_DIR = os.path.dirname(os.path.realpath(__file__))
CD_DIR = os.path.join(WORKING_DIR, "..", "src", "cloud_droid")
sys.path.append(CD_DIR)

from droid import list_cloud_providers, list_smokers_fnames


SMOKERS_DIR = "smokers"
SMOKERS_FNAME_RE = r"^[^_]+_[^_]+.*.py$"


def parse_smoker_names(smoker_fname):
    smoker_name = smoker_fname[:-3]
    components = smoker_name.split("_")
    return components[0], "_".join(components[1:])


def get_class_name_from_args(service_name, smoker_action):
    return (
        f"{service_name.title()}" f"{smoker_action.title().replace('_', '')}" "Smoker"
    )


# def list_cloud_providers():
#     cloud_providers = os.listdir(SMOKERS_DIR)
#     cloud_providers = map(lambda x: os.path.join(SMOKERS_DIR, x), cloud_providers)
#     cloud_providers = filter(lambda x: os.path.isdir(x), cloud_providers)
#     return map(lambda x: os.path.basename(x), cloud_providers)


def list_existing_services(cloud_provider):
    # smokers = os.listdir(os.path.join(SMOKERS_DIR, cloud_provider))
    # smokers = filter(lambda x: re.match(SMOKERS_FNAME_RE, x), smokers)
    # parsed_smokers = map(parse_smoker_names, smokers)
    # return [name[0] for name in parsed_smokers]
    smokers = list_smokers_fnames(cloud_provider)
    parsed_smokers = map(parse_smoker_names, smokers)
    return [name[0] for name in parsed_smokers]



def check_service_name(value):
    if value.lower() != value:
        raise argparse.ArgumentTypeError(
            f"service_name {value} should be in lower case"
        )
    if "_" in value:
        raise argparse.ArgumentTypeError(
            f"service_name {value} cannot have '_' characters"
        )
    return value


def check_smoker_action(value):
    if value.lower() != value:
        raise argparse.ArgumentTypeError(
            f"smoker_action {value} should be in lower case"
        )
    return value


def load_template(cloud_provider, class_name):
    template_path = os.path.join(WORKING_DIR, cloud_provider, "template.j2")
    if not os.path.exists(template_path):
        sys.stderr.write(f"No template file {template_path}\n")
        sys.exit(1)

    with open(template_path) as fd:
        template = Template(fd.read())

    return template.render(smoker_class_name=class_name)


def create_code(cloud_provider, service_name, smoker_action):
    class_name = get_class_name_from_args(service_name, smoker_action)
    fname = os.path.join(
        CD_DIR, args.cloud_provider, SMOKERS_DIR, f"{args.service_name}_{args.smoker_action}.py"
    )
    file_content = load_template(cloud_provider, class_name)
    with open(fname, "w") as fd:
        fd.write(file_content)
    return class_name, fname, file_content


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create the template to implement your own smoker.",
    )
    parser.add_argument(
        "cloud_provider", help="Cloud provider", choices=list_cloud_providers(),
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
    args = parser.parse_args()
    existing_services = list_existing_services(args.cloud_provider)

    if args.service_name not in existing_services:
        nl = "\n"
        bullet = f"{nl} *"
        # TODO: what if existing_services is empty? anyway, existing_services should start with a bullet
        if not existing_services:
            print(
                f"Currently there are no smokers at all for {args.cloud_provider}."
                f"{nl}{nl}Do you still want to continue with {args.service_name}? (y/n)"
            )
        else:
            existing_services = bullet.join(set(existing_services))
            existing_services = bullet + existing_services
            print(
                f"There are no smokers for the service {args.service_name}. "
                f"All the services we have are: {existing_services}"
                f"{nl}{nl}Do you still want to continue with {args.service_name}? (y/n)"
            )
        yes = {"yes", "y"}
        no = {"no", "n"}
        while True:
            choice = input().lower()
            if choice in yes:
                break
            elif choice in no:
                sys.stderr.write("Aborting...\n")
                sys.exit(1)
            else:
                sys.stdout.write("Please respond with 'y' or 'n'\n")

    class_name, fname, file_content = create_code(
        args.cloud_provider, args.service_name, args.smoker_action
    )
    print("Class created: \n\t" + class_name)
    print("File created: \n\t" + os.path.relpath(fname))
