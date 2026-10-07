import argparse
import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", nargs="?", default="load_bad.csv")
    input_path = Path(parser.parse_args().csv_file)
    if not input_path.is_absolute():
        input_path = Path(__file__).resolve().parent / input_path

    result_path = Path(__file__).with_name("load_result.csv")
    plot_path = Path(__file__).with_name("stress_plot.png")
    cross_section_area_mm2 = 200
    threshold_stress_mpa = 6

    with input_path.open("r", newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        required_columns = {"time_s", "force_N"}
        if not required_columns.issubset(reader.fieldnames or []):
            print("CSV 파일에 time_s와 force_N 열이 필요합니다.")
            return

        data = []
        result_rows = []
        excluded_rows = 0
        for row_number, row in enumerate(reader, start=2):
            values = {}
            row_issues = []
            for column in ("time_s", "force_N"):
                raw_value = row.get(column)
                if raw_value is None or not raw_value.strip():
                    row_issues.append((column, raw_value, "빈칸"))
                    continue
                try:
                    value = float(raw_value)
                except ValueError:
                    row_issues.append((column, raw_value, "숫자가 아님"))
                    continue
                if not math.isfinite(value):
                    row_issues.append((column, raw_value, "유한한 숫자가 아님"))
                    continue
                values[column] = value

            if row_issues:
                excluded_rows += 1
                for column, raw_value, reason in row_issues:
                    print(
                        f"문제 행: {row_number}행, {column} 값={raw_value!r} ({reason})"
                    )
                continue

            time_s = values["time_s"]
            force_n = values["force_N"]
            data.append((time_s, force_n))
            row["stress_MPa"] = f"{force_n / cross_section_area_mm2:g}"
            result_rows.append(row)

    if not data:
        print(f"제외한 행 수: {excluded_rows}개")
        print("유효한 데이터 수: 0개")
        print("유효한 데이터가 없어 계산과 그래프 생성을 중단합니다.")
        return

    max_time_s, max_force_n = max(data, key=lambda item: item[1])
    max_stress_time_s, max_stress_mpa = max(
        ((time_s, force_n / cross_section_area_mm2) for time_s, force_n in data),
        key=lambda item: item[1],
    )

    fieldnames = [
        column for column in reader.fieldnames if column != "stress_MPa"
    ] + ["stress_MPa"]
    with result_path.open("w", newline="", encoding="utf-8-sig") as result_file:
        writer = csv.DictWriter(result_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(result_rows)

    time_values = [time_s for time_s, _ in data]
    stress_values = [
        force_n / cross_section_area_mm2 for _, force_n in data
    ]
    over_threshold_count = sum(
        stress_mpa > threshold_stress_mpa for stress_mpa in stress_values
    )
    plt.plot(time_values, stress_values, marker="o", linestyle="-")
    plt.scatter(
        [max_stress_time_s],
        [max_stress_mpa],
        color="red",
        zorder=3,
    )
    plt.annotate(
        f"{max_stress_mpa:g} MPa",
        (max_stress_time_s, max_stress_mpa),
        xytext=(8, 8),
        textcoords="offset points",
        color="red",
    )
    plt.xlabel("Time (s)")
    plt.ylabel("Stres (MPa)")
    plt.tight_layout()
    plt.savefig(plot_path, dpi=300)
    plt.close()

    print(f"데이터 개수: {len(data)}개")
    print(f"최대하중: {max_force_n:g} N")
    print(f"최대하중 시각: {max_time_s:g} s")
    print(f"최대응력: {max_stress_mpa:g} MPa")
    print(f"최대응력 시각: {max_stress_time_s:g} s")
    print(
        f"기준 응력({threshold_stress_mpa:g} MPa) 초과 데이터 개수: "
        f"{over_threshold_count}개"
    )
    print(f"제외한 행 수: {excluded_rows}개")
    print(f"유효한 데이터 수: {len(data)}개")
    print(f"결과 파일: {result_path.name}")
    print(f"그래프 파일: {plot_path.name}")


if __name__ == "__main__":
    main()