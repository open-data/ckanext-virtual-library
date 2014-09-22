import ckan as ckan
import ckan.plugins as p
import ckan.lib.helpers as h
import ckan.lib.formatters as formatters
import ckan.model as model
from ckanext.virtual_library import helpers
from wcms import wcms_configure

class VirtualLibrary(p.SingletonPlugin):
    """
    Plugin for public-facing version of data.gc.ca site, aka the "portal"
    This plugin requires the DataGCCAForms plugin
    """
    p.implements(p.IConfigurer)
    p.implements(p.ITemplateHelpers)
    p.implements(p.IConfigurable)

    def update_config(self, config):

        # add our templates - note that the Web Experience Toolkit distribution
        # files should be installed in the public folder
        p.toolkit.add_template_directory(config, 'templates')
        p.toolkit.add_public_directory(config, 'public')


    def get_helpers(self):
        return dict((h, getattr(helpers, h)) for h in [
            'dataset_rating',
            'dataset_comment_count',
            'dataset_comments',
            'get_license'
            ])

    def configure(self, config):

        if ('ckan.drupal.url' in config):
            wcms_configure(config['ckan.drupal.url'])
