"""Demonstrate manual instrumentation for library code.

Reference: https://opentelemetry.io/docs/languages/python/instrumentation/
"""
from timeit import default_timer as timer

from opentelemetry import trace, metrics
from opentelemetry.trace import Status, StatusCode

tracer = trace.get_tracer(__name__)  # provider shall be set only at application code
meter = metrics.get_meter(__name__)  # provider shall be set only at application code
counter = meter.create_counter(
    name="checker.counter",
    description="Counts amount of checker operation done",
    unit="1",
)
duration = meter.create_histogram(
    name="checker.duration",
    description="Measures the duration of the checker operation",
    unit="s",
)


@tracer.start_as_current_span("do_something")
def do_something(x: int):
    start = timer()
    counter.add(1, {"checker.type": "Valid topic"})
    main_span = trace.get_current_span()
    main_span.add_event("this is the beginning")
    with tracer.start_as_current_span("child_do_something"):
        cur_span = trace.get_current_span()
        cur_span.add_event("we are doing something here")
        # set attributes to current span
        cur_span.set_attribute("operation.value", 1)
        cur_span.set_attribute("operation.name", "Saying hello!")
        cur_span.set_attribute("operation.other-stuff", [1, 2, 3])
        try:
            x += 1

        except TypeError as e:
            cur_span.record_exception(e)
            cur_span.set_status(Status(StatusCode.ERROR))

    main_span.add_event("this is the ending")
    end = timer()
    duration.record(end - start, {})

    return x
