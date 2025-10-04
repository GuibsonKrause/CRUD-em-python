from __future__ import annotations

from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for

from crud_app.storage import TxtStorage

BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__, template_folder=str(BASE_DIR / "crud_app" / "templates"))
app.config["SECRET_KEY"] = "dev-secret-key"  # troque em producao

storage = TxtStorage(BASE_DIR / "data.txt")


@app.route("/")
def home():
    contacts = storage.list_contacts()
    return render_template("index.html", contacts=contacts)


@app.route("/contatos/novo", methods=["GET", "POST"])
def create_contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        if not name:
            flash("Nome nao pode ser vazio.")
            return render_template("form.html", title="Novo contato", contact=None)
        contact = storage.add_contact(name=name, email=email, phone=phone)
        flash(f"Contato {contact.name} criado com sucesso.")
        return redirect(url_for("home"))
    return render_template("form.html", title="Novo contato", contact=None)


@app.route("/contatos/<int:contact_id>/editar", methods=["GET", "POST"])
def edit_contact(contact_id: int):
    contact = storage.get_contact(contact_id)
    if contact is None:
        flash("Contato nao encontrado.")
        return redirect(url_for("home"))
    if request.method == "POST":
        name = request.form.get("name", "").strip() or contact.name
        email = request.form.get("email", "").strip() or contact.email
        phone = request.form.get("phone", "").strip() or contact.phone
        updated = storage.update_contact(contact_id, name=name, email=email, phone=phone)
        if updated is None:
            flash("Nao foi possivel atualizar o contato.")
        else:
            flash("Contato atualizado com sucesso.")
        return redirect(url_for("home"))
    return render_template("form.html", title="Editar contato", contact=contact)


@app.route("/contatos/<int:contact_id>/excluir", methods=["POST"])
def delete_contact(contact_id: int):
    deleted = storage.delete_contact(contact_id)
    if deleted:
        flash("Contato removido.")
    else:
        flash("Contato nao encontrado.")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
