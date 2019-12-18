import pandas as pd
import functools
import operator
import numpy as np



# PM_PATH = 'process_metrics/spring-framework-5.1.0.RELEASE251345pmetrics.csv'
# CM_PATH = 'code_metrics/spring-framework-5.1.0.RELEASE.csv'
# BUG_PATH = 'defects/spring-framework_v5.1.0.RELEASE.._bug251448'
# EXPORT_PATH = 'labeled_dataset/spring-framework_v5.1.0.csv'
# LAN = '.java'

PM_PATH = 'process_metrics/maven-maven-3.0251350pmetrics.csv'
CM_PATH = 'code_metrics/maven-maven-3.0.csv'
BUG_PATH = 'defects/maven_maven-3.0.._bug251434'
EXPORT_PATH = 'labeled_dataset/maven3.0.csv'
LAN = '.java'

# PM_PATH = 'process_metrics/maven-maven-3.3.0232311pmetrics.csv'
# CM_PATH = 'code_metrics/maven-maven-3.3.0.csv'
# BUG_PATH = 'defects/maven_maven-3.3.0.._bug222230'
# EXPORT_PATH = 'labeled_dataset/maven3.3.0.csv'
# LAN = '.java'

# PM_PATH = 'process_metrics/spring-boot-1.4.0.RELEASE232326pmetrics.csv'
# CM_PATH = 'code_metrics/spring-boot-1.4.0.RELEASE.csv'
# BUG_PATH = 'defects/spring-boot_v1.4.0.RELEASE.._bug222222'
# EXPORT_PATH = 'labeled_dataset/spring-boot_v1.4.0.csv'
# LAN = '.java'

# PM_PATH = 'process_metrics/guava-20.0251403pmetrics.csv'
# CM_PATH = 'code_metrics/guava-20.0.csv'
# BUG_PATH = 'defects/guava_v20.0.._bug222319'
# EXPORT_PATH = 'labeled_dataset/guava_v20.0.csv'
# LAN = '.java'

# PM_PATH = 'process_metrics/' + 'freeradius-server-release_3_0_0252114pmetrics' + '.csv'
# CM_PATH = 'code_metrics/'+'freeradius-server-release_3_0_0.csv'
# BUG_PATH = 'defects/'+'freeradius-server_release_3_0_0.._bug252115'
# EXPORT_PATH = 'labeled_dataset/freeradius-server-release_3_0_0'+'-label.csv'
# LAN = '.c'

# PM_PATH = 'process_metrics/' + 'git-2.11.0252126pmetrics' + '.csv'
# CM_PATH = 'code_metrics/'+'git-2.11.0.csv'
# BUG_PATH = 'defects/'+'git_v2.11.0.._bug252120'
# EXPORT_PATH = 'labeled_dataset/git_v2.11.0'+'-label.csv'
# LAN = '.c'

# PM_PATH = 'process_metrics/' + 'freeswitch-1.5.0252111pmetrics' + '.csv'
# CM_PATH = 'code_metrics/'+'freeswitch-1.5.0.csv'
# BUG_PATH = 'defects/'+'freeswitch_v1.5.0.._bug252034'
# EXPORT_PATH = 'labeled_dataset/freeswitch_v1.5.0'+'-label.csv'
# LAN = '.c'

# PM_PATH = 'process_metrics/' + 'mpv-0.3.0252110pmetrics' + '.csv'
# CM_PATH = 'code_metrics/'+'mpv-0.3.0.csv'
# BUG_PATH = 'defects/'+'mpv_v0.3.0.._bug252116'
# EXPORT_PATH = 'labeled_dataset/mpv_v0.3.0'+'-label.csv'
# LAN = '.c'

# PM_PATH = 'process_metrics/' + 'neovim-0.2.0252052pmetrics' + '.csv'
# CM_PATH = 'code_metrics/'+'neovim-0.2.0.csv'
# BUG_PATH = 'defects/'+'neovim_v0.2.0.._bug252028'
# EXPORT_PATH = 'labeled_dataset/neovim_v0.2.0'+'-label.csv'
# LAN = '.c'

# PM_PATH = 'process_metrics/' + 'openssl-OpenSSL_1_1_0252107pmetrics' + '.csv'
# CM_PATH = 'code_metrics/'+'openssl-OpenSSL_1_1_0.csv'
# BUG_PATH = 'defects/'+'openssl_OpenSSL_1_1_0.._bug252035'
# EXPORT_PATH = 'labeled_dataset/openssl_OpenSSL_1_1_0'+'-label.csv'
# LAN = '.c'


# ========================================================


def convertTuple(tup):
    str = functools.reduce(operator.add, (tup))
    return str


def get_class_metrics(df_raw):
    lselect = [
        'File',
        'CountClassCoupled',
        'CountDeclClassMethod',
        'CountDeclClassVariable',
        'CountDeclMethodAll',
        'CountDeclMethodPrivate',
        'CountDeclMethodPublic',
        'MaxInheritanceTree',
        'PercentLackOfCohesion',
        'CountDeclInstanceMethod',
        'CountDeclInstanceVariable'
    ]
    # df_class = df_raw[df_raw.Kind == 'Class']
    df_class = df_raw.loc[:, lselect]

    df_select_metrics = df_class.dropna(axis='rows')

    df_min = df_select_metrics.groupby(['File']).agg([np.min]).reset_index()
    df_min.columns = [convertTuple(key) for key in df_min.keys()]
    # df_min.columns = [key+'_min' for key in df_min.keys()]

    df_max = df_select_metrics.groupby(['File']).agg([np.max]).reset_index()
    df_max.columns = [convertTuple(key) for key in df_max.keys()]
    # df_max.columns = [key+'_max' for key in df_max.keys()]

    df_avg = df_select_metrics.groupby(['File']).agg([np.average]).reset_index()
    df_avg.columns = [convertTuple(key) for key in df_avg.keys()]
    # df_avg.columns = [key+'_avg' for key in df_avg.keys()]
    df_merge = pd.merge(df_min, df_max, how='inner', on='File')
    df_merge = pd.merge(df_merge, df_avg, how='inner', on='File')
    df_merge = df_merge.rename(columns={'File': 'Name'})
    return df_merge


def get_file_metrics(df):
    df_ret = df[df.Kind == 'File']
    df_ret = df_ret[df_ret.Name.str.endswith(LAN)]
    df_ret = df_ret.dropna(axis='columns')
    return df_ret


def generate_dataset():
    # process metrics
    df_process = pd.read_csv(PM_PATH)
    # code metrics
    df2 = pd.read_csv(CM_PATH)
    # class metrics
    df_class = get_class_metrics(df2)
    df_file = get_file_metrics(df2)
    # df2 = df2[df2.Name.str.endswith(LAN)]
    # df2 = df2[df2.Kind == 'File']
    # df2 = df2.dropna(axis='columns')

    df3 = pd.merge(df_process, df_file, how='inner', on='Name')
    df3 = pd.merge(df3, df_class, how='inner', on='Name')
    bug_files = [line.rstrip('\n') for line in open(BUG_PATH)]
    all_files = df_file.Name.to_list()
    #
    bugs = []
    for file in all_files:
        is_bug = 0
        for i, file2 in enumerate(bug_files, 1):
            if file.endswith(file2):
                is_bug = 1
                break
        bugs.append(is_bug)
    data = {'Name': all_files, 'Label': bugs}
    df4 = pd.DataFrame.from_dict(data)
    df5 = pd.merge(df3, df4, how='inner', on='Name')
    df5 = df5.drop('Kind', 1)
    df5 = df5.drop('File', 1)
    df5.to_csv(EXPORT_PATH)


def main():
    generate_dataset()


if __name__ == '__main__':
    main()
