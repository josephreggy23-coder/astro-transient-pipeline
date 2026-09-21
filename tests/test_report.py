from astro_transient_pipeline.report import build_report


def test_report_writes_reproducible_artifacts(tmp_path):
    summary = build_report(tmp_path, alert_count=50, seed=3)
    assert summary["alert_count"] == 50
    assert sum(summary["classification_counts"].values()) == 50
    assert (tmp_path / "alerts.csv").exists()
    assert (tmp_path / "classification_distribution.svg").exists()

