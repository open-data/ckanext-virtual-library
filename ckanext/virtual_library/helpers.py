from wcms import wcms_dataset_comments, wcms_dataset_comment_count, wcms_dataset_rating
from ckan.model import Package

# Retrieve the comments for this dataset that have been saved in the Drupal database
def dataset_comments(pkg_id, lang):

    return wcms_dataset_comments(pkg_id, lang)


def dataset_rating(package_id):

    return wcms_dataset_rating(package_id)


def dataset_comment_count(package_id):

    return wcms_dataset_comment_count(package_id)

def get_license(license_id):

    return Package.get_license_register().get(license_id)
