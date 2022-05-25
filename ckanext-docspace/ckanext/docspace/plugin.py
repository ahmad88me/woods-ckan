import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class DocspacePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IResourceView, inherit=True)
    plugins.implements(plugins.interfaces.IDatasetForm, inherit=True)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'docspace')

    # IResourceView
    def info(self):
        return {'preview_enabled': True, 'name': 'the button', 'title': 'The Buttonn'}

    def can_view(self, data_dict):
        return True

    def setup_template_variables(self, context, data_dict):
        return data_dict

    def view_template(self, context, data_dict):
        return 'button.html'

    def form_template(self, context, data_dict):
        return 'button.html'

    # IDatasetForm
    def resource_template(self, package_type):
        return '/package/resource_read.html'
