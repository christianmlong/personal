import prettyprinter
prettyprinter.install_extras(
    include=[
        'python',
        'attrs',
        'django',
        'requests',
        'dataclasses',
    ],
    warn_on_error=True
)
