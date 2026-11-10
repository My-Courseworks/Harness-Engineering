"""Data access: the only layer that talks to the operations database.

Tools say what they want in domain terms and call a function here. Each function
is one unit of work: it opens a session, reads or writes through the models, and
commits or rolls back as a whole. Nothing in this package knows about agents,
tools, or what the model is shown; shaping results for the model is the tool's job.

One module per domain, mirroring ``models/`` and ``tools/``.
"""
