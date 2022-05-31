import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class DocspacePlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDatasetForm)  # To add docspace field to the resources

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
        # schema.update({
        #     'docspace_viewid': [toolkit.get_validator('ignore_missing'),
        #                     toolkit.get_converter('convert_to_extras')]
        # })
        # Add our custom_resource_text metadata field to the schema
        schema['resources'].update({
            'docspace_viewid': [toolkit.get_validator('ignore_missing')]
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
        # schema.update({
        #     'custom_text': [toolkit.get_converter('convert_from_extras'),
        #         toolkit.get_validator('ignore_missing')]
        #     })

        schema['resources'].update({
                'docspace_viewid': [toolkit.get_validator('ignore_missing')]
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
