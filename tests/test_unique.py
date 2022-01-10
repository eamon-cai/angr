import os


import angr

location = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'binaries', 'tests')

find = {
    'veritesting_a': {
        'x86_64': 0x40066a
    }
}

criteria = {
    'veritesting_a': lambda input_found: input_found.count(b'B') == 10
}

def run_unique(binary, arch):
    proj = angr.Project(os.path.join(location, arch, binary),
                        auto_load_libs=False)
    simgr = proj.factory.simulation_manager()
    technique = angr.exploration_techniques.UniqueSearch()
    simgr.use_technique(technique)

    def found(simgr):
        return simgr.active[0].addr == find[binary][arch]
    simgr.run(until=found)
    assert simgr.active[0].addr == find[binary][arch]

    input_found = simgr.active[0].posix.dumps(0)
    assert criteria[binary](input_found)

def test_unique():
    for binary in find:
        for arch in find[binary]:
            yield run_unique, binary, arch

if __name__ == "__main__":
    for test_func, test_binary, test_arch in test_unique():
        test_func(test_binary, test_arch)
