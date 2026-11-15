"""Pharmacie Nabeul : liste des pharmacies de garde de Nabeul.

Application volontairement minimale : seule la chaîne DevOps est évaluée.
"""
import os

from flask import Flask, jsonify, request
from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    insert,
    select,
    text,
)
from sqlalchemy.pool import StaticPool

metadata = MetaData()
pharmacies = Table(
    "pharmacies",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("nom", String(120), nullable=False),
    Column("quartier", String(80), nullable=False),
    Column("telephone", String(30), nullable=False, default=""),
    Column("de_garde", Boolean, nullable=False, default=True),
)


def make_engine(url):
    if url.startswith("sqlite"):
        # Base en mémoire pour les tests : une seule connexion partagée.
        return create_engine(
            url,
            poolclass=StaticPool,
            connect_args={"check_same_thread": False},
        )
    return create_engine(url, pool_pre_ping=True)


def create_app(database_url=None):
    app = Flask(__name__)
    url = database_url or os.environ.get("DATABASE_URL", "sqlite:///:memory:")
    engine = make_engine(url)
    metadata.create_all(engine)
    version = os.environ.get("APP_VERSION", "dev")

    @app.get("/health")
    def health():
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
        except Exception:
            return jsonify(status="error", database="down", version=version), 503
        return jsonify(status="ok", database="up", version=version, service="pharmacie-nabeul")

    @app.get("/pharmacies")
    def liste():
        query = select(pharmacies).where(pharmacies.c.de_garde.is_(True))
        quartier = request.args.get("quartier")
        if quartier:
            query = query.where(pharmacies.c.quartier == quartier)
        with engine.connect() as conn:
            rows = conn.execute(query.order_by(pharmacies.c.nom)).mappings().all()
        return jsonify([dict(r) for r in rows])

    @app.post("/pharmacies")
    def ajoute():
        data = request.get_json(silent=True) or {}
        nom = str(data.get("nom", "")).strip()
        quartier = str(data.get("quartier", "")).strip()
        if not nom or not quartier:
            return jsonify(erreur="nom et quartier sont obligatoires"), 400
        values = {
            "nom": nom,
            "quartier": quartier,
            "telephone": str(data.get("telephone", "")).strip(),
            "de_garde": bool(data.get("de_garde", True)),
        }
        with engine.begin() as conn:
            new_id = conn.execute(insert(pharmacies).values(**values)).inserted_primary_key[0]
        return jsonify(id=new_id, **values), 201

    return app