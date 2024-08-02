import pandas as pd
def po(file_name,sheet_name):
    df = pd.read_excel(file_name,sheet_name=sheet_name)
    df = df.fillna(0)
    subject_correlation_dict = df.set_index('Subject Name')['Correlation'].to_dict()
    data_dict = df.set_index('Subject Name').T.to_dict('list')
    mapping_correlation = {}
    for k,v in data_dict.items():
        if k not in mapping_correlation.keys():
            mapping_correlation[k] = []
        for val in v:
            if val == 0:
                mapping_correlation[k].append(0)
            else:
                mapping_correlation[k].append(subject_correlation_dict[k])
    final_po = {}
    for k,v in subject_correlation_dict.items():
        if k not in final_po.keys():
            final_po[k] = []
        for i in range(15):
            ans = (float(mapping_correlation[k][i])*float(data_dict[k][i]))/3
            ans = round(ans,2)
            final_po[k].append(ans)
    avg_of_pos = []
    l = len(final_po.keys())
    for i in range(15):
        s = 0
        for k in final_po.keys():
            s += final_po[k][i]
        ans = s/l
        ans = round(ans,2)
        avg_of_pos.append(ans)
    return avg_of_pos