from backend.docs_engine.loaders.aws_loaders import AWSLoader
from backend.docs_engine.loaders.base_loader import BaseDocLoader


# Register available loaders here
DOC_LOADERS = {
    "aws_doc": AWSLoader,
    # "terraform_doc": TerraformLoader,  # To be added later
}


class DocLoader:
    """
    Loader dispatcher that wraps a specific documentation loader implementation.
    """

    def __init__(self, loader_class: type[BaseDocLoader]):
        if not issubclass(loader_class, BaseDocLoader):
            raise TypeError("loader_class must be a subclass of BaseDocLoader")
        self.loader: BaseDocLoader = loader_class()
