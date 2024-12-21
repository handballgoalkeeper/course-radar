from dataclasses import dataclass

@dataclass
class PackageIncludeDTO:
    __table__ = 'package_includes'
    id: int = None
    package_id: int = None
    text: str = None