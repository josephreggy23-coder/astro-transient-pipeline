from astro_transient_pipeline.pipeline import run


def test_pipeline_is_deterministic_and_ranked():
    targets = run(20, seed=9)
    assert len(targets) == 10
    assert targets == sorted(targets, key=lambda target: target.priority, reverse=True)
