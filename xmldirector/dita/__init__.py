# placeholder

try:
    import xmldirector.plonecore
    have_xmldirector = True
except ImportError:
    have_xmldirector = False

if have_xmldirector:

    import os
    from xmldirector.plonecore.transformer_registry import TransformerRegistryUtility
    from xmldirector.plonecore.validator_registry import ValidatorRegistryUtility

    cwd = os.path.dirname(__file__)

    TransformerRegistryUtility.register_transformation(
        'dita', 'html2dita', os.path.join(cwd, 'converters', 'h2d', 'h2d.xsl'))

