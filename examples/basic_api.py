from __future__ import annotations

from pathlib import Path

from visionlabelops import audit_dataset, compute_stats, read_dataset


def main() -> None:
    dataset_root = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "labelme"
    dataset = read_dataset(dataset_root, "labelme")
    stats = compute_stats(dataset)
    audit = audit_dataset(dataset)

    print(f"images={dataset.image_count}")
    print(f"annotations={stats.annotation_count}")
    print(f"issues={audit.summary['issue_count']}")


if __name__ == "__main__":
    main()
