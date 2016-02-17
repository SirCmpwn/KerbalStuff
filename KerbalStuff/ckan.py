from KerbalStuff.config import _cfg
from github import Github
from flask import url_for
import subprocess
import json
import os
import re

# I am not sure if we want to keep the name KerbalStuff hardcoded here, but to keep CKAN integration running
# I won't change it. We'll have to talk with the CKAN Devs and SirCmpwn to remove the name her / make the 
# Integration as modular as possible, for people who don't have a CKAN accessable.
# TODO(Thomas): Fix CKAN and make this modular.
def send_to_ckan(mod):
    if not _cfg("netkan_repo_path"):
        return
    if not mod.ckan:
        return
    json_blob = {
        'spec_version': 'v1.4',
        'identifier': re.sub(r'\W+', '', mod.name),
        '$kref': '#/ckan/kerbalstuff/' + str(mod.id),
        'license': mod.license,
        'x_via': 'Automated SpaceDock CKAN submission'
    }
    wd = _cfg("netkan_repo_path")
    path = os.path.join(wd, 'NetKAN', json_blob['identifier'] + '.netkan')

    if os.path.exists(path):
        # If the file is already there, then chances are this mod has already been indexed
        return

    with open(path, 'w') as f:
        f.write(json.dumps(json_blob, indent=4))
    subprocess.call(['git', 'fetch', 'upstream'], cwd=wd)
    subprocess.call(['git', 'checkout', '-b', 'add-' + json_blob['identifier'], 'upstream/master'], cwd=wd)
    subprocess.call(['git', 'add', '-A'], cwd=wd)
    subprocess.call(['git', 'commit', '-m', 'Add {0} from SpaceDock\n\nThis is an automated commit on behalf of {1}'\
            .format(mod.name, mod.user.username), '--author={0} <{1}>'.format(mod.user.username, mod.user.email)], cwd=wd)
    subprocess.call(['git', 'push', '-u', 'origin', 'add-' + json_blob['identifier']], cwd=wd)
    g = Github(_cfg('github_user'), _cfg('github_pass'))
    r = g.get_repo("KSP-CKAN/NetKAN")
    r.create_pull(title="Add {0} from SpaceDock".format(mod.name), base=r.default_branch, head="KerbalStuffBot:add-" + json_blob['identifier'], body=\
"""\
This pull request was automatically generated by SpaceDock on behalf of {0}, to add [{1}]({4}{2}) to CKAN.

Please direct questions about this pull request to [{0}]({4}{3}).
""".format(mod.user.username, mod.name,\
    url_for('mods.mod', mod_name=mod.name, id=mod.id),\
    url_for("profile.view_profile", username=mod.user.username),\
    _cfg("protocol") + "://" + _cfg("domain")))
