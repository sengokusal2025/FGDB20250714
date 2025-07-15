#!/usr/bin/env python3
"""
configure.py - FGDB Configuration Script

Functional Graph Database (FGDB) に関数と独立変数を登録するスクリプト
operation.txtファイルを読み込み、関数と独立変数をMGとOGに登録する
"""

import sys
import argparse
import os
from lib import FunctionalGraph, load_fgdb, save_fgdb, parse_operation_file


def configure_fgdb(operation_file: str, fgdb_file: str = "fgdb.pickle") -> None:
    """
    FGDBに関数と独立変数を設定する
    
    Args:
        operation_file: 関数定義ファイルのパス
        fgdb_file: FGDBファイルのパス
    """
    print("=" * 60)
    print("FUNCTIONAL GRAPH DATABASE (FGDB) CONFIGURATION")
    print("=" * 60)
    
    # FGDBファイルの読み込み
    if not os.path.exists(fgdb_file):
        print(f"Error: FGDB file '{fgdb_file}' not found.")
        print("Please run 'python init.py' first to initialize FGDB.")
        sys.exit(1)
    
    fgdb = load_fgdb(fgdb_file)
    if fgdb is None:
        print("Error: Failed to load FGDB file.")
        sys.exit(1)
    
    print(f"✓ FGDB loaded from: {fgdb_file}")
    
    # 関数定義ファイルの読み込み
    if not os.path.exists(operation_file):
        print(f"Error: Operation file '{operation_file}' not found.")
        sys.exit(1)
    
    operations = parse_operation_file(operation_file)
    if not operations:
        print("Error: No valid operations found in the file.")
        sys.exit(1)
    
    print(f"✓ Operation file parsed: {len(operations)} operations found")
    
    # 関数と独立変数の抽出
    functions = set()
    independent_variables = set()
    dependent_variables = set()
    
    for operation in operations:
        dependent_var, function_name, independent_vars = operation
        functions.add(function_name)
        dependent_variables.add(dependent_var)
        independent_variables.update(independent_vars)
    
    # 純粋な独立変数を特定（従属変数でもある変数を除外）
    pure_independent_vars = independent_variables - dependent_variables
    
    print(f"\nAnalysis results:")
    print(f"  Functions: {len(functions)} - {', '.join(sorted(functions))}")
    print(f"  Pure independent variables: {len(pure_independent_vars)} - {', '.join(sorted(pure_independent_vars))}")
    print(f"  All independent variables: {len(independent_variables)} - {', '.join(sorted(independent_variables))}")
    print(f"  Dependent variables: {len(dependent_variables)} - {', '.join(sorted(dependent_variables))}")
    
    # 関数をMGに登録
    print(f"\nRegistering functions to Management Graph:")
    for function_name in sorted(functions):
        fgdb.register_function(function_name)
    
    # 独立変数をMGとOGに登録
    print(f"\nRegistering independent variables to Management and Operation Graphs:")
    for var_name in sorted(pure_independent_vars):
        fgdb.register_independent_variable(var_name)
    
    # 中間変数（他の関数の出力でもある独立変数）もOGに登録
    intermediate_vars = independent_variables & dependent_variables
    if intermediate_vars:
        print(f"\nRegistering intermediate variables to Operation Graph:")
        for var_name in sorted(intermediate_vars):
            if var_name not in fgdb.operation_graph.nodes:
                fgdb.operation_graph.add_node(
                    var_name,
                    node_type="data_block",
                    data_type="intermediate",
                    created_at=None  # 実際の作成は operation 時
                )
                print(f"Intermediate variable registered: {var_name}")
    
    # FGDBを保存
    save_fgdb(fgdb, fgdb_file)
    print(f"✓ FGDB configuration saved")
    
    # 設定結果の表示
    print(f"\nConfiguration completed successfully!")
    print(f"Management Graph nodes: {fgdb.management_graph.number_of_nodes()}")
    print(f"Management Graph edges: {fgdb.management_graph.number_of_edges()}")
    print(f"Operation Graph nodes: {fgdb.operation_graph.number_of_nodes()}")
    print(f"Operation Graph edges: {fgdb.operation_graph.number_of_edges()}")
    
    print(f"\nNext steps:")
    print(f"1. Run 'python operation.py -i {operation_file}' to execute operations")
    print(f"2. Run 'python show_fgdb.py' to visualize the graphs")
    print("=" * 60)


def main():
    """メイン実行関数"""
    parser = argparse.ArgumentParser(
        description="Configure FGDB with functions and variables from operation file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python configure.py -i operation.txt
  python configure.py -i operation.txt -f my_fgdb.pickle
  python configure.py --input operation.txt --fgdb custom.pickle
        """
    )
    
    parser.add_argument(
        '-i', '--input',
        required=True,
        help='Input operation file (e.g., operation.txt)'
    )
    
    parser.add_argument(
        '-f', '--fgdb',
        default='fgdb.pickle',
        help='FGDB file path (default: fgdb.pickle)'
    )
    
    # ヘルプが要求された場合や引数がない場合
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    args = parser.parse_args()
    
    try:
        # FGDB設定の実行
        configure_fgdb(args.input, args.fgdb)
        
    except KeyboardInterrupt:
        print("\nConfiguration cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error during configuration: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
