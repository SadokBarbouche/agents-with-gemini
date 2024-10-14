# Notes

# Tracing and debugging :
# LangSmith provides detailed trace logs of your application's runs. 
# A "run" represents a unit of work or operation within your LLM application. 
# These runs are grouped into "traces" that encapsulate the entire operation triggered by a user request. 

# Evaluation and Testing: 
# LangSmith allows developers to create datasets made up of inputs and expected outputs.

# Monitoring and Observability: 
# LangSmith provides real-time monitoring capabilities. 
# It tracks key performance metrics such as latency, cost, and user feedback scores, 
# ensuring that any anomalies or performance issues are quickly identified and addressed.

# Collaboration and Feedback: 
# LangSmith fosters collaboration among developers by providing features like annotation queues and feedback collection. 
# These tools enable teams to add human insights and labels to traces, enhancing the debugging and evaluation processes.

# Versioning and Comparison: 
# As applications evolve, it's important to compare different versions to ensure improvements or identify regressions. 
# LangSmith offers a comparison view for side-by-side analysis of application versions, 
# making it easier to track changes and their impacts on performance.

# Langsmith jargon
# ----------------------------------------------------------
# A Project is a collection of traces. 
# A Trace is a collection of runs that are related to a single operation
# A Run is a span representing a single unit of work or operation within your LLM application. 
# Runs are bound to a trace by a unique trace ID.
# Tags are collections of strings that can be attached to runs.
# Metadata is a collection of key-value pairs that can be attached to runs.

# Project -> Trace -> Run -> Tags/Metadata