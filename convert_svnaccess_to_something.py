
# vim: ai:ts=4:sw=4:expandtab


def convert(infp, outfp):
    import ConfigParser
    config = ConfigParser.RawConfigParser()
    if isinstance(infp, basestring):
        config.read(infp)
    else:
        config.readfp(infp)
    allfoos = {}
    for section in config.sections():
        if section == 'groups':
            for group, memberlist in config.items(section):
                name = '@' + group
                if not allfoos.has_key(name):
                    allfoos[name] = Foo(name)
                g = allfoos[name]
                members = [x.strip() for x in memberlist.split(',')]
                for member in members:
                    if not allfoos.has_key(member):
                        allfoos[member] = Foo(member)
                    m = allfoos[member]
                    g.add_member(m)
        else:
            for principal, access in config.items(section):
                if not allfoos.has_key(principal):
                    allfoos[principal] = Foo(principal)
                p = allfoos[principal]
                p.add_access(section, access)
    for name in sorted(allfoos.iterkeys()):
        if not name.endswith('@itsc.uah.edu'):
            continue
        print name
        foo = allfoos[name]
        seen = set()
        repopaths = {}
        queue = [foo]
        while len(queue) > 0:
            bar = queue.pop(0)
            seen.add(bar)
            for repopath, access in bar.repopaths.iteritems():
                repopaths[repopath] = access
            for group in bar.groups.itervalues():
                if not group in seen:
                    queue.append(group)
        for repopath in sorted(repopaths.iterkeys()):
            print '   ', repopath, repopaths[repopath]


class Foo(object):
    def __init__(self, name):
        self.name = name
        self.members = {}
        self.groups = {}
        self.repopaths = {}

    def add_member(self, member):
        self.members[member.name] = member
        member.groups[self.name] = self

    def add_access(self, repopath, access):
        self.repopaths[repopath] = access


if __name__ == '__main__':
    import sys
    convert(sys.argv[1], sys.stdout)

