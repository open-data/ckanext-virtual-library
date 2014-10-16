from wcms import wcms_dataset_comments, wcms_dataset_comment_count, wcms_dataset_rating
from ckan.model import Package
from pylons import config

CKAN_SITE_URL_OPTION = 'ckan.site_url'
SITE_URL_DEFAULT = 'http://localhost/'

# Retrieve the comments for this dataset that have been saved in the Drupal database
def dataset_comments(pkg_id, lang):

    return wcms_dataset_comments(pkg_id, lang)


def dataset_rating(package_id):

    return wcms_dataset_rating(package_id)


def dataset_comment_count(package_id):

    return wcms_dataset_comment_count(package_id)

def get_license(license_id):

    return Package.get_license_register().get(license_id)

def get_site_url(lang):

    return "{0}/{1}/doc".format(str(config.get(CKAN_SITE_URL_OPTION, SITE_URL_DEFAULT)), lang)

def get_res_lang(lang_str, lang):
    has_lang = False
    langs = lang_str.split(',')
    for l in langs:
        if l == lang:
            has_lang = True
            break
    return has_lang