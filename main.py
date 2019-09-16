from jfkairport.collect import *

for entry in collect_security_wait_times():
    print(
        "{:<1} {:<12}     {:5} seconds".format(
            entry.terminal, entry.queue_type.name, entry.wait_time_seconds
        )
    )

