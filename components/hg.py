# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from components.logging import logEntryExit
from components.providerbase import BaseProvider, INeedsCommandProvider, INeedsLoggingProvider


class MercurialProvider(BaseProvider, INeedsCommandProvider, INeedsLoggingProvider):
    def __init__(self, config):
        pass

    @logEntryExit
    def commit(self, library, bug_id, new_release_version):
        # Note that this commit message format changes, one must also edit the
        # Updatebot Verify job in mozilla-central ( verify-updatebot.py )
        bug_id = "Bug {0}".format(bug_id)
        self.run(["hg", "commit", "-m", "%s - Update %s to %s" %
                  (bug_id, library.name, new_release_version)])

    @logEntryExit
    def commit_patches(self, library, bug_id, new_release_version):
        # Note that this commit message format changes, one must also edit the
        # Updatebot Verify job in mozilla-central ( verify-updatebot.py )
        bug_id = "Bug {0}".format(bug_id)
        self.run(["hg", "commit", "-m", "%s - Apply mozilla patches for %s" %
                  (bug_id, library.name)])

    @logEntryExit
    def diff_stats(self):
        ret = self.run(["hg", "diff", "--stat"])
        return ret.stdout.decode().rstrip()
