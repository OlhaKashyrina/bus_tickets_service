def test_healthcheck(client):
    resp = client.get("/api/v1/healthcheck")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
