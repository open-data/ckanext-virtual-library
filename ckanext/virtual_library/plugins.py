from ast import literal_eval
import ckan as ckan
import ckan.plugins as p
import ckan.lib.helpers as h
import ckan.lib.formatters as formatters
import ckan.model as model
import json
from ckanext.virtual_library import helpers
from logging import getLogger
from pylons.i18n import _
from wcms import wcms_configure

class VirtualLibrary(p.SingletonPlugin):
    """
    Plugin for the Open Information (virtual library) on open.canada.ca
    """
    p.implements(p.IConfigurer)
    p.implements(p.ITemplateHelpers)
    p.implements(p.IConfigurable)
    p.implements(p.IPackageController)
    p.implements(p.IFacets)

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
            'get_license',
            'get_site_url',
            'get_res_lang',
            'googleanalytics_id'
            ])

    def configure(self, config):

        if ('ckan.drupal.url' in config):
            wcms_configure(config['ckan.drupal.url'])

    def read(self, entity):
        return entity

    def create(self, entity):
        return entity

    def edit(self, entity):
        return entity

    def authz_add_role(self, object_role):
        return object_role

    def authz_remove_role(self, object_role):
        return object_role

    def delete(self, entity):
        return entity

    def after_create(self, context, pkg_dict):
        return pkg_dict

    def after_update(self, context, pkg_dict):
        return pkg_dict

    def after_delete(self, context, pkg_dict):
        return pkg_dict

    def after_show(self, context, pkg_dict):
        return pkg_dict

    def before_search(self, search_params):
        return search_params

    def after_search(self, search_results, search_params):
        return search_results

    def before_index(self, pkg_dict):
        '''
             Extensions will receive what will be given to the solr for
             indexing. This is essentially a flattened dict (except for
             multli-valued fields such as tags) of all the terms sent to
             the indexer. The extension can modify this by returning an
             altered version.
        '''

        def kw(value):
            s = value.strip()
            if not s:
                return []
            return [k.strip() for k in s.split(',')]

        def le(langs):
            facets = []
            if 'eng' in langs:
                facets.append('English')
            if 'fra' in langs:
                facets.append('French')
            return facets

        def lf(langs):
            facets = []
            if 'eng' in langs:
                facets.append('Anglais')
            if 'fra' in langs:
                facets.append(u'Fran\xe7ais')
            return facets

        if pkg_dict['type'] == u'doc':
            try:
                if 'extras_source_organizations_ml' in pkg_dict:
                    source_orgs = json.loads(pkg_dict['extras_source_organizations_ml'])
                    if 'en' in source_orgs:
                        pkg_dict['vocab_source_org_en'] = kw(source_orgs['en'])
                    if 'fr' in source_orgs:
                        pkg_dict['vocab_source_org_fr'] = kw(source_orgs['fr'])
                if 'subject_ml' in pkg_dict:
                    subject = json.loads(pkg_dict['subject_ml'])
                    if 'en' in subject:
                        pkg_dict['vocab_subject_en'] = kw(subject['en'])
                    if 'fr' in subject:
                        pkg_dict['vocab_subject_fr'] = kw(subject['fr'])
                langs = []
                if 'data_dict' in pkg_dict:
                    data_dict = json.loads(pkg_dict['data_dict'])
                    if 'resources' in data_dict:
                        for r in data_dict['resources']:
                            if 'languages' in r:
                                rlangs = r['languages'].split(',')
                                for l in rlangs:
                                    if not l in langs:
                                        langs.append(l)
                pkg_dict['vocab_languages_en'] = le(langs)
                pkg_dict['vocab_languages_fr'] = lf(langs)


            except ValueError as v:
                log = getLogger('ckanext')
                log.error(v.message)

        return pkg_dict

    def before_view(self, pkg_dict):
        return pkg_dict

    # IFacets --------------

    def dataset_facets(self, facets_dict, package_type):
        if package_type == 'doc':
            facets_dict['vocab_source_org_en'] = _('Publisher')
            facets_dict['vocab_subject_en'] = _('Subject')
            facets_dict['vocab_source_org_fr'] = _('Publisher')
            facets_dict['vocab_subject_fr'] = _('Subject')
            facets_dict['vocab_languages_en'] = _('Language')
            facets_dict['vocab_languages_fr'] = _('Language')
        return facets_dict

    def group_facets(self, facets_dict, group_type, package_type):
        return facets_dict

    def organization_facets(self, facets_dict, organization_type, package_type):
        return facets_dict
