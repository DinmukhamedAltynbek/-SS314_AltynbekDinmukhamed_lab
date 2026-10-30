
import hashlib
import argparse
import json
from pathlib import Path


def get_student_params(student_id: str):
    h = int(
        hashlib.sha256(student_id.encode("utf-8")).hexdigest()[:8],
        16
    )

    N = 1024 + ((h % 9) * 64)
    buffer_elements = 16_777_216
    seed = h % 100_007

    return {
        "student_id": student_id,
        "N": N,
        "buffer_elements": buffer_elements,
        "seed": seed
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--student-id", required=True)
    args = parser.parse_args()

    params = get_student_params(args.student_id)

    project_dir = Path(__file__).resolve().parent.parent
    results_dir = project_dir / "results"
    results_dir.mkdir(exist_ok=True)

    output_path = results_dir / "salted_params.json"

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(params, file, indent=4)

    print("Salted parameters:", params)
    print("Saved to:", output_path)
