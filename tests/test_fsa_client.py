from unittest.mock import patch, MagicMock

from extract.fsa_client import get_establishments

def _fake_page(rows, total_pages):
    resp = MagicMock()
    resp.json.return_value = {
        "establishments": rows,
        "meta": {"totalPages":total_pages},
    }
    resp.raise_for_status.return_value = None
    return resp

@patch("extract.fsa_client.requests.Session.get")
def test_pages_until_last(mock_get):
    mock_get.side_effect = [
            _fake_page([{"FHRSID":1}, {"FHRSID":2}], total_pages=2),
            _fake_page([{"FHRSID":3}], total_pages=2)
    ]
    out = list(get_establishments(authority_id=999, page_size=2))
    assert [e["FHRSID"] for e in out] == [1,2,3]
    assert mock_get.call_count == 2