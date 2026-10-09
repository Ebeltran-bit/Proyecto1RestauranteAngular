def test_root_serves_the_waiter_interface(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "Pedidos de sala" in response.text


def test_interface_assets_are_served(client):
    for path, content_type in (("/static/app.js", "javascript"), ("/static/styles.css", "text/css")):
        response = client.get(path)
        assert response.status_code == 200
        assert content_type in response.headers["content-type"]


def test_interface_is_not_listed_in_the_api_docs(client):
    assert "/" not in client.get("/openapi.json").json()["paths"]
