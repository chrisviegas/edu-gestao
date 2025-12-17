from dataclasses import dataclass

@dataclass(frozen=True)
class Address:
    street: str
    number: str
    neighborhood: str
    city: str
    state: str
    zip_code: str

    def __composite_values__(self):
        return (
            self.street,
            self.number,
            self.neighborhood,
            self.city,
            self.state,
            self.zip_code,
        )
