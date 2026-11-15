import pytest

from app import create_app


@pytest.fixture()
def client():
    app = create_app("sqlite:///:memory:")
    return app.test_client()


def test_health_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"
    assert r.get_json()["database"] == "up"


def test_ajout_et_liste(client):
    r = client.post(
        "/pharmacies",
        json={"nom": "Pharmacie Centrale", "quartier": "Centre-ville", "telephone": "72 000 000"},
    )
    assert r.status_code == 201
    liste = client.get("/pharmacies").get_json()
    assert [p["nom"] for p in liste] == ["Pharmacie Centrale"]


def test_filtre_par_quartier(client):
    client.post("/pharmacies", json={"nom": "A", "quartier": "Centre-ville"})
    client.post("/pharmacies", json={"nom": "B", "quartier": "Dar Chaabane"})
    liste = client.get("/pharmacies?quartier=Dar Chaabane").get_json()
    assert [p["nom"] for p in liste] == ["B"]


def test_pharmacie_hors_garde_non_listee(client):
    client.post("/pharmacies", json={"nom": "A", "quartier": "Centre-ville", "de_garde": False})
    assert client.get("/pharmacies").get_json() == []


def test_ajout_invalide_rejete(client):
    r = client.post("/pharmacies", json={"nom": "Sans quartier"})
    assert r.status_code == 400
