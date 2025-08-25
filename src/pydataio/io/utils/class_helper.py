from importlib import import_module

from pydataio.io import IO_BASENAME


def getClass(identifier, package):
    """
    Dynamically imports and returns a class from a specified module.

    Args:
        identifier (str): The identifier for the class, in the format 'batch.FileSystemInput'.
        package (str, optional): The sub package, i.e.  "outputs".

    Returns:
        type: The class specified by the pipe_identifier.

    Raises:
        ValueError: If the pipe_identifier does not contain a dot separating the module and class name.
    """
    if "." in identifier:
        module, className = identifier.rsplit(".", 1)
        mod = import_module(f"{IO_BASENAME}.{module}.{package}")
        classType = getattr(mod, className)
    else:
        raise ValueError(f"Invalid pipe identifier: {identifier}")
    return classType
