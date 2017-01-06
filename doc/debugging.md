![Imagination Technologies Limited logo](images/img.png)

# Creator System Test Framework

## Debugging

Both the output of the helpers and the System Test Manager should be monitored.
The helpers call the API and will return AwaErrors to the System Test Manager process.
Depending on whether the problem is within the test framework or the API determines
which debugging method should be used.

### Debugging the Test Framework

Insert the following line into a test case or any of the handler files:

    import pdb; pdb.set_trace()

PDB can also be automatically started by nose on test error or failure if the `--pdb` option
is provided to noserunner.py.

### Debugging the API through the Gateway Client/Server Helpers

Replace the file, line number and path_to_helpers.

    gdb python
    break define_common.c:69
    run /{path_to_helpers}/gateway_client_test_helper.py

### Debugging the API through the client / server daemons

* Start a server and client daemon on the same ports that the target test would use.
* Make sure the client endpoint name is the same.
* Start the helpers and then the Test Manager.
* Instead of the helpers launching Daemons, they will use the existing daemons, which can
  be debugged using gdb.

Note: Daemon startup/teardown must be disabled within the helpers. (In the future an argument
should be added to disable launching/killing daemons)
