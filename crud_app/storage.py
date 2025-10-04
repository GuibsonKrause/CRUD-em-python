from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

FIELD_SEPARATOR = "|"


@dataclass
class Contact:
    id: int
    name: str
    email: str
    phone: str

    def to_line(self) -> str:
        return f"{self.id}{FIELD_SEPARATOR}{self.name}{FIELD_SEPARATOR}{self.email}{FIELD_SEPARATOR}{self.phone}"

    @classmethod
    def from_line(cls, line: str) -> "Contact":
        parts = line.strip().split(FIELD_SEPARATOR)
        if len(parts) != 4:
            raise ValueError(f"Invalid record: {line!r}")
        id_str, name, email, phone = parts
        return cls(id=int(id_str), name=name, email=email, phone=phone)


class TxtStorage:
    def __init__(self, file_path: Path | str) -> None:
        self.file_path = Path(file_path)
        self.file_path.touch(exist_ok=True)

    def list_contacts(self) -> List[Contact]:
        raw = self.file_path.read_text(encoding="utf-8")
        contacts: List[Contact] = []
        for line in raw.splitlines():
            if not line.strip():
                continue
            try:
                contacts.append(Contact.from_line(line))
            except ValueError:
                # Skip broken lines instead of crashing the program.
                continue
        return contacts

    def _write_all(self, contacts: List[Contact]) -> None:
        data = "\n".join(contact.to_line() for contact in contacts)
        if data:
            data += "\n"
        self.file_path.write_text(data, encoding="utf-8")

    @staticmethod
    def _next_id(contacts: List[Contact]) -> int:
        return max((contact.id for contact in contacts), default=0) + 1

    def get_contact(self, contact_id: int) -> Optional[Contact]:
        for contact in self.list_contacts():
            if contact.id == contact_id:
                return contact
        return None

    def add_contact(self, *, name: str, email: str, phone: str) -> Contact:
        contacts = self.list_contacts()
        new_contact = Contact(
            id=self._next_id(contacts),
            name=name.strip(),
            email=email.strip(),
            phone=phone.strip(),
        )
        contacts.append(new_contact)
        self._write_all(contacts)
        return new_contact

    def update_contact(
        self,
        contact_id: int,
        *,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
    ) -> Optional[Contact]:
        contacts = self.list_contacts()
        updated: Optional[Contact] = None
        for index, contact in enumerate(contacts):
            if contact.id != contact_id:
                continue
            updated = Contact(
                id=contact.id,
                name=contact.name if name is None else name.strip(),
                email=contact.email if email is None else email.strip(),
                phone=contact.phone if phone is None else phone.strip(),
            )
            contacts[index] = updated
            break
        if updated is None:
            return None
        self._write_all(contacts)
        return updated

    def delete_contact(self, contact_id: int) -> bool:
        contacts = self.list_contacts()
        new_contacts = [c for c in contacts if c.id != contact_id]
        if len(new_contacts) == len(contacts):
            return False
        self._write_all(new_contacts)
        return True
