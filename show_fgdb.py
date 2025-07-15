#!/usr/bin/env python3
"""
show_fgdb.py - FGDB Visualization Script

Functional Graph Database (FGDB) の可視化を行うスクリプト
fgdb.pickleを読み込み、Management Graph と Operation Graph を
matplotlibを使用して表示する
"""

import sys
import argparse
import os
import matplotlib.pyplot as plt
from lib import (FunctionalGraph, load_fgdb, show_management_graph, 
                 show_operation_graph, show_fgdb_summary)


def visualize_fgdb(fgdb_file: str = "fgdb.pickle", 
                  show_mg: bool = True, 
                  show_og: bool = True, 
                  save_mg: str = None, 
                  save_og: str = None,
                  show_summary: bool = True) -> None:
    """
    FGDBの可視化を実行する
    
    Args:
        fgdb_file: FGDBファイルのパス
        show_mg: Management Graphを表示するかどうか
        show_og: Operation Graphを表示するかどうか
        save_mg: Management Graphの保存パス
        save_og: Operation Graphの保存パス
        show_summary: サマリーを表示するかどうか
    """
    print("=" * 60)
    print("FUNCTIONAL GRAPH DATABASE (FGDB) VISUALIZATION")
    print("=" * 60)
    
    # FGDBファイルの読み込み
    if not os.path.exists(fgdb_file):
        print(f"Error: FGDB file '{fgdb_file}' not found.")
        print("Please run the following commands first:")
        print("1. python init.py")
        print("2. python configure.py -i operation.txt")
        print("3. python operation.py -i operation.txt")
        sys.exit(1)
    
    fgdb = load_fgdb(fgdb_file)
    if fgdb is None:
        print("Error: Failed to load FGDB file.")
        sys.exit(1)
    
    print(f"✓ FGDB loaded from: {fgdb_file}")
    
    # サマリー情報の表示
    if show_summary:
        show_fgdb_summary(fgdb)
    
    # グラフが空でないかチェック
    if fgdb.management_graph.number_of_nodes() <= 1:
        print("Warning: Management Graph appears to be empty or contains only root node.")
        print("Make sure you have run configure.py and operation.py.")
    
    if fgdb.operation_graph.number_of_nodes() <= 1:
        print("Warning: Operation Graph appears to be empty or contains only root node.")
        print("Make sure you have run configure.py and operation.py.")
    
    # matplotlib設定
    plt.style.use('default')  # デフォルトスタイルを使用
    
    try:
        # Management Graph の可視化
        if show_mg:
            print("\nDisplaying Management Graph (MG)...")
            show_management_graph(fgdb, save_mg)
        
        # Operation Graph の可視化
        if show_og:
            print("\nDisplaying Operation Graph (OG)...")
            show_operation_graph(fgdb, save_og)
        
        # 保存結果の表示
        if save_mg:
            print(f"✓ Management Graph saved to: {save_mg}")
        if save_og:
            print(f"✓ Operation Graph saved to: {save_og}")
        
        print(f"\nVisualization completed successfully!")
        
    except Exception as e:
        print(f"Error during visualization: {e}")
        print("Note: Make sure you have matplotlib properly installed.")
        raise


def main():
    """メイン実行関数"""
    parser = argparse.ArgumentParser(
        description="Visualize FGDB graphs using matplotlib",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python show_fgdb.py
  python show_fgdb.py -f my_fgdb.pickle
  python show_fgdb.py --mg-only
  python show_fgdb.py --og-only
  python show_fgdb.py --save-mg mg_graph.png --save-og og_graph.png
  python show_fgdb.py --no-summary
        """
    )
    
    parser.add_argument(
        '-f', '--fgdb',
        default='fgdb.pickle',
        help='FGDB file path (default: fgdb.pickle)'
    )
    
    parser.add_argument(
        '--mg-only',
        action='store_true',
        help='Show only Management Graph'
    )
    
    parser.add_argument(
        '--og-only',
        action='store_true',
        help='Show only Operation Graph'
    )
    
    parser.add_argument(
        '--save-mg',
        help='Save Management Graph to file (e.g., mg_graph.png)'
    )
    
    parser.add_argument(
        '--save-og',
        help='Save Operation Graph to file (e.g., og_graph.png)'
    )
    
    parser.add_argument(
        '--no-summary',
        action='store_true',
        help='Skip showing FGDB summary'
    )
    
    args = parser.parse_args()
    
    # 表示オプションの決定
    show_mg = True
    show_og = True
    
    if args.mg_only:
        show_og = False
    elif args.og_only:
        show_mg = False
    
    show_summary = not args.no_summary
    
    try:
        # FGDB可視化の実行
        visualize_fgdb(
            fgdb_file=args.fgdb,
            show_mg=show_mg,
            show_og=show_og,
            save_mg=args.save_mg,
            save_og=args.save_og,
            show_summary=show_summary
        )
        
    except KeyboardInterrupt:
        print("\nVisualization cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error during visualization: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
