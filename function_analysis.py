import re

def analyze_functions(file_path):
    """
    関数の記述が書かれたファイルを読み込み、従属変数、関数、独立変数のリストを作成する
    
    Args:
        file_path (str): 関数記述ファイルのパス
        
    Returns:
        list: ope_list - 各関数の[従属変数, 関数名, 独立変数]のリスト
    """
    # ファイルの読み込み
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"エラー: {file_path} というファイルが見つかりません。")
        return []
    
    # 解析結果を格納するリスト
    ope_list = []
    
    # 各行を解析
    for line in lines:
        # 空行やコメント行をスキップ
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        # 正規表現を使用して関数式を解析
        # パターン: y変数=f関数(x変数[,x変数]...)
        pattern = r'([a-zA-Z0-9_]+)\s*=\s*([a-zA-Z0-9_]+)\s*\(\s*([a-zA-Z0-9_,\s]+)\s*\)'
        match = re.match(pattern, line)
        
        if match:
            y_var = match.group(1)  # 従属変数
            f_func = match.group(2)  # 関数
            x_vars = match.group(3).strip()  # 独立変数（カンマ区切りの文字列）
            
            # 結果をリストに追加
            ope_list.append([y_var, f_func, x_vars])
        else:
            print(f"警告: 行 '{line}' は解析できませんでした。")
    
    return ope_list


def display_ope_list(ope_list):
    """
    ope_listを見やすく表示する関数
    
    Args:
        ope_list (list): 解析結果のリスト
    """
    print("\n関数解析結果:")
    print("-" * 50)
    print(f"{'従属変数':<10} | {'関数':<10} | {'独立変数':<20}")
    print("-" * 50)
    
    for item in ope_list:
        print(f"{item[0]:<10} | {item[1]:<10} | {item[2]:<20}")
    
    print("-" * 50)


def get_independent_vars_list(ope_list):
    """
    ope_listから独立変数のリストを取得し、カンマで分割した新しいリストを作成
    
    Args:
        ope_list (list): 解析結果のリスト
        
    Returns:
        list: x_dush - すべての独立変数を含むリスト
    """
    # 各関数の独立変数をカンマで分割してリストに格納
    split_lists = []
    
    for item in ope_list:
        # 独立変数の文字列を取得
        x_vars = item[2]
        # カンマで分割してスペースを除去
        split_vars = [x.strip() for x in x_vars.split(',')]
        # リストに追加
        split_lists.append(split_vars)
    
    # 全てのリストを一つに連結
    x_dush = []
    for sublist in split_lists:
        x_dush.extend(sublist)
    
    return x_dush


def find_pure_independent_vars(ope_list):
    """
    純粋な独立変数（x_dush - (x_dush ∩ y)）を見つける
    
    Args:
        ope_list (list): 解析結果のリスト
        
    Returns:
        list: xmy - 純粋な独立変数のリスト
    """
    # 全ての独立変数リストを取得
    x_dush = get_independent_vars_list(ope_list)
    
    # 全ての従属変数リストを取得
    y_list = [item[0] for item in ope_list]
    
    # 差集合を計算 (x_dush - (x_dush ∩ y))
    xmy = [x for x in x_dush if x not in y_list]
    
    return xmy


def main():
    """
    メイン実行関数
    """
    file_path = 'operation.txt'
    
    # 1. ファイルを読み込み解析
    ope_list = analyze_functions(file_path)
    
    # 2. 解析結果を表示
    display_ope_list(ope_list)
    
    # 3. 全ての独立変数を取得
    x_dush = get_independent_vars_list(ope_list)
    print("\n全ての独立変数 (x_dush):")
    print(x_dush)
    
    # 4. 純粋な独立変数を取得
    xmy = find_pure_independent_vars(ope_list)
    print("\n純粋な独立変数 (xmy = x_dush - (x_dush ∩ y)):")
    print(xmy)


if __name__ == "__main__":
    main()
