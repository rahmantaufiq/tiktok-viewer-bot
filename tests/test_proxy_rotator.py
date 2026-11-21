from src.core.config_loader import ProxyCfg
from src.core.services.proxy_rotator import ProxyRotator, _parse_line


def test_parse_plain_proxy():
    entry = _parse_line("1.2.3.4:8080")
    assert entry is not None
    assert entry.host == "1.2.3.4"
    assert entry.port == 8080
    assert entry.user is None


def test_parse_proxy_with_creds():
    entry = _parse_line("user:pass@10.0.0.1:3128")
    assert entry is not None
    assert entry.user == "user"
    assert entry.password == "pass"


def test_rotator_disabled_returns_none(tmp_path):
    cfg = ProxyCfg(enabled=False)
    rotator = ProxyRotator(cfg)
    assert rotator.next() is None