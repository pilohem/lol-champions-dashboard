import pandas as pd

def get_champion(data_json, name):
    """Get champion's data"""
    return data_json['data'][name]

def get_champion_stats(data, name):
    """Get champions data as DataFrame"""
    _name = pd.DataFrame({'name': f'[{name}](/{name})'}, index=[0])
    stats_temp = pd.DataFrame(data['data'][name]['stats'], index=[0])
    return pd.concat([_name, stats_temp], axis=1, ignore_index=False)

def get_all_champion_stats(data, champions_list):
    """Get full list of champions stats"""
    stats_all = pd.DataFrame()
    for champion in champions_list:
        stats = get_champion_stats(data, champion)
        stats_all = pd.concat([stats_all, stats], ignore_index=True)
    return stats_all