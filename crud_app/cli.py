from __future__ import annotations

from pathlib import Path
from typing import Callable, Dict

from crud_app.storage import TxtStorage

MENU = (
    "\n"
    "==== Agenda de Contatos ====\n"
    "1) Listar contatos\n"
    "2) Adicionar contato\n"
    "3) Atualizar contato\n"
    "4) Remover contato\n"
    "0) Sair\n"
)


def list_contacts(storage: TxtStorage) -> None:
    contacts = storage.list_contacts()
    if not contacts:
        print("\nNenhum contato cadastrado.")
        return
    print("\nID | Nome | Email | Telefone")
    print("-- | ---- | ----- | --------")
    for contact in contacts:
        print(f"{contact.id:>2} | {contact.name} | {contact.email} | {contact.phone}")


def add_contact(storage: TxtStorage) -> None:
    print("\nAdicionar novo contato")
    name = input("Nome: ").strip()
    if not name:
        print("Nome nao pode ser vazio.")
        return
    email = input("Email: ").strip()
    phone = input("Telefone: ").strip()
    contact = storage.add_contact(name=name, email=email, phone=phone)
    print(f"Contato criado com id {contact.id}.")


def update_contact(storage: TxtStorage) -> None:
    raw_id = input("\nID do contato a atualizar: ").strip()
    if not raw_id.isdigit():
        print("ID invalido.")
        return
    contact_id = int(raw_id)
    contact = storage.get_contact(contact_id)
    if contact is None:
        print("Contato nao encontrado.")
        return
    print("Pressione Enter para manter o valor atual.")
    name = input(f"Nome [{contact.name}]: ").strip()
    email = input(f"Email [{contact.email}]: ").strip()
    phone = input(f"Telefone [{contact.phone}]: ").strip()
    updated = storage.update_contact(
        contact_id,
        name=name or None,
        email=email or None,
        phone=phone or None,
    )
    if updated is None:
        print("Nao foi possivel atualizar o contato.")
        return
    print("Contato atualizado.")


def delete_contact(storage: TxtStorage) -> None:
    raw_id = input("\nID do contato a remover: ").strip()
    if not raw_id.isdigit():
        print("ID invalido.")
        return
    contact_id = int(raw_id)
    contact = storage.get_contact(contact_id)
    if contact is None:
        print("Contato nao encontrado.")
        return
    confirm = input(f"Remover {contact.name}? (s/N): ").strip().lower()
    if confirm != "s":
        print("Remocao cancelada.")
        return
    if storage.delete_contact(contact_id):
        print("Contato removido.")
    else:
        print("Falha ao remover o contato.")


def run_cli(data_file: Path | str) -> None:
    storage = TxtStorage(data_file)
    actions: Dict[str, Callable[[TxtStorage], None]] = {
        "1": list_contacts,
        "2": add_contact,
        "3": update_contact,
        "4": delete_contact,
    }
    while True:
        print(MENU)
        choice = input("Escolha uma opcao: ").strip()
        if choice == "0":
            print("Ate logo!")
            break
        action = actions.get(choice)
        if action is None:
            print("Opcao invalida. Tente novamente.")
            continue
        action(storage)


__all__ = ["run_cli"]
