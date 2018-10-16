import os
import copy
import json
from jinja2 import Environment, FileSystemLoader

from helpers import calculate_transforms_for_attribute, calculate_doc_list, calculate_attributes_config_dict


HERE = os.path.abspath(os.path.dirname(__file__))

def populate_template(template_dir, **kwargs):
    env = Environment(
        # keep python templates valid python
        block_start_string='#{%',
        loader=FileSystemLoader(template_dir),
        # trim_blocks=True,
        # lstrip_blocks=True,
    )

    template = env.get_template('netscaler_appfwlearningsettings.template')
    stream = template.stream(**kwargs)

    #output_file = 'netscaler_appfw_profile.py'
    output_file = os.path.join(HERE, '..', '..', '..', 'ansible-modules', 'netscaler_appfw_learningsettings.py')
    stream.dump(
        output_file,
        encoding='utf-8'
    )

def main():

    # Find template dir
    template_dir = os.path.join(HERE, '..', 'templates', 'appfw')
    if not os.path.exists(template_dir):
        raise Exception('Cannot find template dir')

    # Find nscli json data dir
    json_dir = os.path.join(HERE, '..', 'nitro_api_defines/kamet/appfw')
    if not os.path.exists(json_dir):
        raise Exception('Cannot find json dir')

    main_json_file = os.path.join(json_dir, 'appfwlearningsettings.json')
    with open(main_json_file, 'r') as fh:
        main_object_attributes = json.load(fh)

    main_object_doc_list = calculate_doc_list(main_object_attributes)

    attributes_config_list = []
    attributes_config_list.append(
        calculate_attributes_config_dict('appfwlearningsettings', main_object_attributes)
    )

    print(json.dumps(attributes_config_list, indent=4))

    # Populate the template
    populate_template(
        template_dir,
        main_object_doc_list=main_object_doc_list,
        main_nitro_class='appfwlearningsettings',
        main_object_put_id='jsoncontenttypevalue',
        attributes_config_list=attributes_config_list,
    )



if __name__ == '__main__':
    main()
