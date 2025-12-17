# Structure
Order matters for readability (even if it doesn't affect semantics). On the first read, a file is read top-down, so put important things near the top. The main function goes first.

# Control Flow
Use only very simple, explicit control flow for clarity. Do not use recursion to ensure that all executions that should be bounded are bounded. Use only a minimum of excellent abstractions but only if they make the best sense of the domain. Abstractions are never zero cost. Every abstraction introduces the risk of a leaky abstraction.

# Data Structures
All loops and all queues must have a fixed upper bound to prevent infinite loops or tail latency spikes. This follows the “fail-fast” principle so that violations are detected sooner rather than later. Where a loop cannot terminate (e.g. an event loop), this must be asserted.

# Error Handling
All errors must be handled. An analysis of production failures in distributed data-intensive systems found that the majority of catastrophic failures could have been prevented by simple testing of error handling code.

# Naming
Add units or qualifiers to variable names, and put the units or qualifiers last, sorted by descending significance, so that the variable starts with the most significant word, and ends with the least significant word. For example, latency_ms_max rather than max_latency_ms. This will then line up nicely when latency_ms_min is added, as well as group all variables that relate to latency.

When choosing related names, try hard to find names with the same number of characters so that related variables all line up in the source. For example, source and target are better than src and dest because they have the second-order effect that any related variables such as source_offset and target_offset will all line up in calculations and slices. This makes the code symmetrical, with clean blocks that are easier for the eye to parse and for the reader to check.

When a single function calls out to a helper function or callback, prefix the name of the helper function with the name of the calling function to show the call history. For example, read_sector() and read_sector_callback().

A noun is often a better descriptor than an adjective or present participle, because a noun can be directly used in correspondence without having to be rephrased.


# Types
Use the smallest type that can represent the value. Every variable, parameter, and return value must have an explicit type.

