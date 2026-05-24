"""主程序：串联所有子问题"""
import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("=" * 70)
    print("  绿电直连型电氢氨园区优化运行 - 全问题求解")
    print("=" * 70)

    from problem1 import solve_problem1
    from problem2 import solve_problem2
    from problem3 import solve_problem3
    from problem4 import solve_problem4
    from sensitivity import run_sensitivity

    results = {}

    print("\n\n" + "▶" * 30 + " 问题一 " + "◀" * 30)
    results["problem1"] = solve_problem1()

    print("\n\n" + "▶" * 30 + " 问题二 " + "◀" * 30)
    results["problem2"] = solve_problem2()

    print("\n\n" + "▶" * 30 + " 问题三 " + "◀" * 30)
    results["problem3"] = solve_problem3()

    print("\n\n" + "▶" * 30 + " 问题四 " + "◀" * 30)
    results["problem4"] = solve_problem4()

    print("\n\n" + "▶" * 30 + " 灵敏度分析 " + "◀" * 30)
    results["sensitivity"] = run_sensitivity()

    # 汇总关键结果
    summary = {
        "problem1": {
            "E_total": results["problem1"]["energy"]["E_total"],
            "E_RE": results["problem1"]["energy"]["E_RE"],
            "R1": results["problem1"]["indicators"]["R1"],
            "R2": results["problem1"]["indicators"]["R2"],
            "R3": results["problem1"]["indicators"]["R3"],
            "C_ton": results["problem1"]["cost"]["C_ton"],
        },
        "problem2": {
            "best_typical_production": results["problem2"]["best_typical_production"],
            "best_typical_cost": results["problem2"]["best_typical_cost"],
            "annual_cost": results["problem2"]["annual_analysis"]["annual_cost_per_ton"],
            "full_satisfy": results["problem2"]["annual_analysis"]["full_satisfy"],
            "partial_satisfy": results["problem2"]["annual_analysis"]["partial_satisfy"],
            "none_satisfy": results["problem2"]["annual_analysis"]["none_satisfy"],
        },
        "problem3": {
            "annual_cost": results["problem3"]["annual_analysis"]["annual_cost_per_ton"],
            "full_satisfy": results["problem3"]["annual_analysis"]["full_satisfy"],
            "partial_satisfy": results["problem3"]["annual_analysis"]["partial_satisfy"],
            "none_satisfy": results["problem3"]["annual_analysis"]["none_satisfy"],
        },
        "problem4": {
            "offgrid_annual_prod": results["problem4"]["offgrid_stats"]["total_annual_production"],
            "offgrid_capacity_util": results["problem4"]["offgrid_stats"]["avg_capacity_util"],
            "best_storage_MWh": results["problem4"]["storage_optimization"]["best_C_sto_MWh"],
            "storage_annual_prod": results["problem4"]["storage_stats"]["total_annual_production"],
        },
        "sensitivity": {
            "base_cost": results["sensitivity"]["base_cost"],
            "most_sensitive": "光伏装机容量",
        },
    }

    # Save all_results.json
    import numpy as np
    class NpEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (np.integer,)): return int(obj)
            if isinstance(obj, (np.floating,)): return float(obj)
            if isinstance(obj, np.ndarray): return obj.tolist()
            return super().default(obj)

    with open("../figures/all_results.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2, cls=NpEncoder)

    print("\n\n" + "=" * 70)
    print("  所有问题求解完成！")
    print("=" * 70)
    print(f"\n关键结果汇总:")
    print(f"  问题一: 吨氨成本={summary['problem1']['C_ton']:.0f}元/吨, R1={summary['problem1']['R1']*100:.1f}%")
    print(f"  问题二: 全年吨氨成本={summary['problem2']['annual_cost']:.0f}元/吨")
    print(f"  问题三: 全年吨氨成本={summary['problem3']['annual_cost']:.0f}元/吨 (改善{(summary['problem2']['annual_cost']-summary['problem3']['annual_cost'])/summary['problem2']['annual_cost']*100:.1f}%)")
    print(f"  问题四: 离网年产量={summary['problem4']['offgrid_annual_prod']:.0f}t, 最优储能={summary['problem4']['best_storage_MWh']}MWh")

    return summary

if __name__ == "__main__":
    main()
