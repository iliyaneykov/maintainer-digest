from maintainer_digest.labels import suggest_labels


def test_security_label_suggested():
    assert "security" in suggest_labels("Possible token vulnerability", "token leak in logs")


def test_existing_label_not_repeated():
    labels = suggest_labels("README typo", existing=["documentation"])
    assert "documentation" not in labels
