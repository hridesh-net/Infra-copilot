class BaseDocLoader:
    """
    Base interface for documentation loaders (e.g., AWS, Terraform).
    """
    def load(self, url: str) -> str:
        raise NotImplementedError("Must implement in subclass")
