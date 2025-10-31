from log_analyzer import normalizeError, parseLogs

def test_normalize_error_simple():
    line = "[2025-10-14 08:02:11] [ERROR] Database connection failed: timeout 123"
    sig = normalizeError(line)
    assert '<NUM>' in sig or 'Database connection failed' in sig

def test_parse_logs(tmp_path):
    p = tmp_path / "sample.log"
    p.write_text("[2025-10-14 08:02:11] [ERROR] Timeout occurred\n[INFO] ok\n")
    result = parseLogs(str(tmp_path))
    assert any('Timeout occurred' in s for s in result.keys())

