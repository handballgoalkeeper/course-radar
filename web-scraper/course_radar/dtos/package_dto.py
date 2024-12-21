from dataclasses import dataclass

@dataclass
class PackageDTO:
    __table__ = "packages"
    id: int = None
    name: str = None
    description: str = None
    original_price: float = None
    discounted_price: float = None
    discount: float = None
    package_includes: list[str] = None
    course_id: int = None