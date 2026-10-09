def test_select_table(client):
    response = client.get("/tables/4")
    assert response.status_code == 200
    assert response.json() == {"id": 4, "name": "Terraza 1"}


def test_unknown_table_returns_404(client):
    response = client.get("/tables/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "No existe la mesa con id 999"}
