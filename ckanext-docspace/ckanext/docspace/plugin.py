import traceback

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import os
from spreadsheetspace.sssapis import SSSAPIS
from spreadsheetspace import table_to_content
import ckan
from ckan.config.environment import CONFIG_FROM_ENV_VARS, config
# import pandas as pd
from multiprocessing import Process

# BASE_URL = "https://woods.linkeddata.es/api/3/action/"
# if 'docspace_api' in os.environ:
#     BASE_URL = os.environ['docspace_api']


class DocspacePlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDatasetForm)  # To add docspace field to the resources
    plugins.implements(plugins.IActions)  # To add a custom API
    # plugins.implements(plugins.IResourceView, inherit=True)
    # plugins.implements(plugins.interfaces.IDatasetForm, inherit=True)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')

    def create_package_schema(self):
        # let's grab the default schema in our plugin
        schema = super(DocspacePlugin, self).create_package_schema()
        # our custom field
        # schema.update({
        #     'docspace_viewid': [toolkit.get_validator('ignore_missing'),
        #                     toolkit.get_converter('convert_to_extras')]
        # })
        return schema

    def update_package_schema(self):
        schema = super(DocspacePlugin, self).update_package_schema()
        # our custom field
        # schema.update({
        #     'docspace_viewid': [toolkit.get_validator('ignore_missing'),
        #                     toolkit.get_converter('convert_to_extras')]
        # })
        return schema

    def _modify_package_schema(self, schema):
        # # Add our custom country_code metadata field to the schema.
        # schema.update({
        #     'country_code': [toolkit.get_validator('ignore_missing'),
        #                      toolkit.get_converter('convert_to_tags')('country_codes')]
        # })
        # Add our custom_test metadata field to the schema, this one will use
        # convert_to_extras instead of convert_to_tags.
        schema.update({
            'docspace_viewid': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')]
        })
        schema.update({
            'docspace_token': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')]
        })
        # Add our custom_resource_text metadata field to the schema
        schema['resources'].update({
            'docspace_viewid': [toolkit.get_validator('ignore_missing')]
        })

        schema['resources'].update({
            'docspace_token': [toolkit.get_validator('ignore_missing')]
        })
        return schema

    def show_package_schema(self):
        schema = super(DocspacePlugin, self).show_package_schema()

        # Don't show vocab tags mixed in with normal 'free' tags
        # (e.g. on dataset pages, or on the search page)
        # schema['tags']['__extras'].append(toolkit.get_converter('free_tags_only'))

        # # Add our custom country_code metadata field to the schema.
        # schema.update({
        #     'country_code': [
        #         toolkit.get_converter('convert_from_tags')('country_codes'),
        #         toolkit.get_validator('ignore_missing')]
        #     })

        # # Add our custom_text field to the dataset schema.
        schema.update({
            'docspace_viewid': [toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('ignore_missing')]
            })

        schema.update({
            'docspace_token': [toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('ignore_missing')]
            })

        schema['resources'].update({
                'docspace_viewid': [toolkit.get_validator('ignore_missing')],
                'docspace_token': [toolkit.get_validator('ignore_missing')]
            })
        return schema

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

    def get_actions(self):
        #actions = super(DocspacePlugin, self).get_actions()
        actions = dict()
        actions[u'docspace_update'] = add_update_docspace
        return actions

    # # IResourceView
    # def info(self):
    #     return {'preview_enabled': True, 'name': 'the button', 'title': 'The Buttonn'}
    #
    # def can_view(self, data_dict):
    #     return True
    #
    # def setup_template_variables(self, context, data_dict):
    #     return data_dict
    #
    # def view_template(self, context, data_dict):
    #     return 'button.html'
    #
    # def form_template(self, context, data_dict):
    #     return 'button.html'
    #
    # # IDatasetForm
    # def resource_template(self, package_type):
    #     return '/package/resource_read.html'


def f(data_dict):
    sss = SSSAPIS(token="bcc51260d15948ffb9346feee3d01358")
    print("To load the data")
    table = table_to_content(data_dict['url'])
    print("table is loaded")
    sss.create_private_view(table=table, description="Uploaded from CKAN", recipients=["aalobaid@fi.upm.es"])
    print("sending the data")


def add_update_docspace(context, data_dict):
    try:
        sss = SSSAPIS(token="bcc51260d15948ffb9346feee3d01358")
        print("ABC ... ")
        if data_dict['docspace_viewid'].strip() == "":
            # create
            p = Process(target=f, args=(data_dict,))
            p.start()
            p.join()
            # table = table_to_content(data_dict['url'])
            # sss.create_private_view(table=table, description="Uploaded from CKAN", recipients=["aalobaid@fi.upm.es"])
        else:
            # update
            table = table_to_content(data_dict['url'])
            sss.update_view(view_id=data_dict['docspace_viewid'], table=table)
            # ckan.logic.action.update.resource_update(context, {'docspace_viewid'})
    except Exception as e:
        print("Exception")
        print(str(e))
        traceback.print_exc()
    return {
        "context": str(context),
        "data_dict": str(data_dict)
    }
    # with open("/home/woods/docspace_logtest", 'w') as f:
    #     f.write(str(datetime.now()))
    #     f.write('\n')







# def add_update_docspace(context, data_dict):
#     try:
#         sss = SSSAPIS(token="bcc51260d15948ffb9346feee3d01358")
#         print("ABC ... ")
#         domain_url = config['ckan.site_url']
#         storage_path = config['ckan.storage_path']
#         if domain_url[-1] != '/':
#             domain_url += '/'
#         local_host = "http://127.0.0.1:3000/"
#         # print(os.environ['CKAN_CONFIG'])
#         # print(str(config))
#         # print(CONFIG_FROM_ENV_VARS['ckan.site_url'])
#         # for k in os.environ:
#         #     print(k)
#         #     if 'site_url' in k.lower():
#         #         print("====================\n\n")
#         # print(os.environ['CKAN_SITE_URL'])
#         print(str(data_dict))
#         url_without_protocol = data_dict['url'].replace("https://", "").replace("http://", "")
#         domain_end = url_without_protocol.find("/")
#         new_url = data_dict['url']
#         if data_dict['url'].startswith(domain_url):
#             new_url = local_host+url_without_protocol[domain_end+1:]
#         print("new url: %s" % new_url)
#         #.replace("https://woods.linkeddata.es/", "http://localhost:3000")
#         if data_dict['docspace_viewid'].strip() == "":
#             # create
#             table = table_to_content(new_url)
#             sss.create_private_view(table=table, description="Uploaded from CKAN", recipients=["aalobaid@fi.upm.es"])
#         else:
#             # update
#             table = table_to_content(new_url)
#             sss.update_view(view_id=data_dict['docspace_viewid'], table=table)
#             # ckan.logic.action.update.resource_update(context, {'docspace_viewid'})
#     except Exception as e:
#         print("Exception")
#         print(str(e))
#         traceback.print_exc()
#     return {
#         "context": str(context),
#         "data_dict": str(data_dict)
#     }
#     # with open("/home/woods/docspace_logtest", 'w') as f:
#     #     f.write(str(datetime.now()))
#     #     f.write('\n')
#
#
#






# def get_table_content(url):
#     pd.read_csv()
#     return [["A", "B", "C"]]


# def table_to_content(table_url):
#     print(table_url)
#     df = pd.read_csv(table_url)
#     print("data is loaded into pandas")
#     content = []
#     header = df.columns
#     for idx, row in df.iterrows():
#         r = []
#         for h in header:
#             r.append(row[h])
#         content.append(r)
#     print("content is returned")
#     print(content)
#     return content


# def add_update_docspace(context, data_dict):
#     try:
#         sss = SSSAPIS(token="bcc51260d15948ffb9346feee3d01358")
#         print("ABC ... ")
#         domain_url = config['ckan.site_url']
#         path = config['ckan.storage_path']
#         if domain_url[-1] != '/':
#             domain_url += '/'
#         local_host = "http://127.0.0.1:3000/"
#         # print(os.environ['CKAN_CONFIG'])
#         # print(str(config))
#         # print(CONFIG_FROM_ENV_VARS['ckan.site_url'])
#         # for k in os.environ:
#         #     print(k)
#         #     if 'site_url' in k.lower():
#         #         print("====================\n\n")
#         # print(os.environ['CKAN_SITE_URL'])
#         print(str(data_dict))
#         url_without_protocol = data_dict['url'].replace("https://", "").replace("http://", "")
#         domain_end = url_without_protocol.find("/")
#         new_url = data_dict['url']
#         if data_dict['url'].startswith(domain_url):
#             new_url = local_host+url_without_protocol[domain_end+1:]
#         print("new url: %s" % new_url)
#         #.replace("https://woods.linkeddata.es/", "http://localhost:3000")
#         if data_dict['docspace_viewid'].strip() == "":
#             # create
#             table = table_to_content(new_url)
#             sss.create_private_view(table=table, description="Uploaded from CKAN", recipients=["aalobaid@fi.upm.es"])
#         else:
#             # update
#             table = table_to_content(new_url)
#             sss.update_view(view_id=data_dict['docspace_viewid'], table=table)
#             # ckan.logic.action.update.resource_update(context, {'docspace_viewid'})
#     except Exception as e:
#         print("Exception")
#         print(str(e))
#         traceback.print_exc()
#     return {
#         "context": str(context),
#         "data_dict": str(data_dict)
#     }
#     # with open("/home/woods/docspace_logtest", 'w') as f:
#     #     f.write(str(datetime.now()))
#     #     f.write('\n')




