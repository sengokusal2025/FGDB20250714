#!/usr/bin/env python3
"""
operation.py - FGDB Operation Execution Script

Functional Graph Database (FGDB) で関数の実行履歴を管理するスクリプト
operation.txtファイルを読み込み、各関数の実行結果をタイムスタンプ付きで記録する
また、operation.txtからbatch file を生成する機能も提供する
"""

import sys
import argparse
import os
import datetime
from lib import FunctionalGraph, load_fgdb, save_fgdb, parse_operation_file, generate_batch_file


def execute_operations(operation_file: str, fgdb_file: str = "fgdb.pickle") -> None:
    """
    FGDBで関数の実行操作を記録する
    
    Args:
        operation_file: 関数定義ファイルのパス
        fgdb_file: FGDBファイルのパス
    """
    print("=" * 60)
    print("FUNCTIONAL GRAPH DATABASE (FGDB) OPERATION EXECUTION")
    print("=" * 60)
    
    # FGDBファイルの読み込み
    if not os.path.exists(fgdb_file):
        print(f"Error: FGDB file '{fgdb_file}' not found.")
        print("Please run 'python init.py' and 'python configure.py' first.")
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
    
    # バッチファイルの生成（常に実行）
    operation_name = os.path.splitext(os.path.basename(operation_file))[0]
    generate_batch_file(operations, operation_name)
    
    # 各操作の実行とFGDBへの記録
    print(f"\nExecuting operations and recording to FGDB:")
    executed_vars = []
    
    for i, operation in enumerate(operations, 1):
        dependent_var, function_name, independent_vars = operation
        
        print(f"\nOperation {i}: {dependent_var} = {function_name}({', '.join(independent_vars)})")
        
        # 独立変数の存在確認
        missing_vars = []
        for var in independent_vars:
            if var not in fgdb.operation_graph.nodes:
                missing_vars.append(var)
        
        if missing_vars:
            print(f"  Warning: Independent variables not found in OG: {missing_vars}")
            # 自動的に中間変数として追加
            for var in missing_vars:
                fgdb.operation_graph.add_node(
                    var,
                    node_type="data_block",
                    data_type="intermediate",
                    created_at=datetime.datetime.now()
                )
                print(f"  Added missing variable to OG: {var}")
        
        # 関数の存在確認
        if function_name not in fgdb.function_blocks:
            print(f"  Warning: Function '{function_name}' not registered. Adding automatically.")
            fgdb.register_function(function_name)
        
        # 操作の実行とOGへの記録
        try:
            timestamped_var = fgdb.execute_operation(function_name, independent_vars, dependent_var)
            executed_vars.append(timestamped_var)
            print(f"  ✓ Executed: {timestamped_var}")
            
        except Exception as e:
            print(f"  ✗ Error executing operation: {e}")
            continue
    
    # FGDBを保存
    save_fgdb(fgdb, fgdb_file)
    print(f"✓ FGDB operations saved")
    
    # 実行結果の表示
    print(f"\nOperation execution completed!")
    print(f"Executed operations: {len(executed_vars)}")
    print(f"Generated variables: {', '.join(executed_vars[:5])}{'...' if len(executed_vars) > 5 else ''}")
    print(f"Management Graph nodes: {fgdb.management_graph.number_of_nodes()}")
    print(f"Management Graph edges: {fgdb.management_graph.number_of_edges()}")
    print(f"Operation Graph nodes: {fgdb.operation_graph.number_of_nodes()}")
    print(f"Operation Graph edges: {fgdb.operation_graph.number_of_edges()}")
    
    print(f"\nNext steps:")
    print(f"1. Run 'python show_fgdb.py' to visualize the execution results")
    operation_name = os.path.splitext(os.path.basename(operation_file))[0]
    print(f"2. Execute '{operation_name}.bat' to run actual function implementations")
    print("=" * 60)


def main():
    """メイン実行関数"""
    parser = argparse.ArgumentParser(
        description="Execute operations and record execution history in FGDB",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python operation.py -i operation.txt
  python operation.py -i operation.txt -f my_fgdb.pickle
  python operation.py -i operation.txt --batch
  python operation.py --input operation.txt --fgdb custom.pickle --batch
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
    
    parser.add_argument(
        '--batch',
        action='store_true',
        help='[DEPRECATED] Batch file generation is now automatic'
    )
    
    # ヘルプが要求された場合や引数がない場合
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    args = parser.parse_args()
    
    try:
        # 操作実行の実行
        execute_operations(args.input, args.fgdb)
        
    except KeyboardInterrupt:
        print("\nOperation execution cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error during operation execution: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
