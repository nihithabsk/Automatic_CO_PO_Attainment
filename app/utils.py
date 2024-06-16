import pandas as pd
def cal(file_path, sheet_name, class_strength,co_mapping):
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=0)
    co_mapping = dict(co_mapping)
    max_marks = df.iloc[0]
    df.columns = df.columns.str.strip()
    highest_marks = {}
    for co, questions in co_mapping.items():
        marks = 0
        for q in questions:
            if q in df.columns:
                max_mark = df.loc[df['Parameters'] == 'Max Marks', q]
                if not max_mark.empty:
                    marks += max_mark.values[0]
        highest_marks[co] = marks
    
    student_rows = df[df['Parameters'] != 'Max Marks'].copy()
    student_rows.dropna(axis=1, how='all', inplace=True)
    student_rows.reset_index(drop=True, inplace=True)
    
    for co, questions in co_mapping.items():
        for q in questions:
            student_rows[q] = pd.to_numeric(student_rows[q], errors='coerce')
    
    student_scores = pd.DataFrame(student_rows['Parameters'])
    for co, questions in co_mapping.items():
        student_scores[co] = student_rows[questions].sum(axis=1)
    
    student_scores.rename(columns={'Parameters': 'Student'}, inplace=True)
    
    renaming_map = {co: co.replace(' ', '_') for co in co_mapping.keys()}
    
    for co in co_mapping.keys():
        student_scores.rename(columns={co: renaming_map[co]}, inplace=True)
        student_scores.rename(columns={f'{co} Percentage': f'{renaming_map[co]}_Percentage'}, inplace=True)
    
    for co in co_mapping.keys():
        percentage_column = f'{renaming_map[co]}_Percentage'
        student_scores[percentage_column] = (student_scores[renaming_map[co]] / highest_marks[co]) * 100
    
    questions = [q for questions in co_mapping.values() for q in questions]
    student_question_scores = student_rows.copy()
    
    if 'Student' not in student_question_scores.columns:
        student_question_scores['Student'] = student_rows['Parameters']
    student_question_scores.set_index('Student', inplace=True)
    
    question_columns = [q for questions in co_mapping.values() for q in questions]
    student_question_scores = student_question_scores[question_columns]
    student_question_scores = student_question_scores.iloc[:-17]
    
    stud_marks_in_each_ques = {col.strip(): student_question_scores[col].sum() for col in student_question_scores.columns}
    
    max_marks.index = max_marks.index.str.strip()
    marks_studA = {}
    marks_studB = {}
    for ques, sm in stud_marks_in_each_ques.items():
        ques = ques.strip()
        if ques in max_marks.index:
            marks_studA[ques] = max_marks[ques] * class_strength
            marks_studB[ques] = sm
    
    percentage_of_attainment = {}
    for ques in marks_studA.keys():
        percentage_of_attainment[ques] = (marks_studB[ques] / marks_studA[ques]) * 100
    
    avg_cos = {}
    for co in co_mapping.keys():
        sumb = 0
        suma = 0
        for q in co_mapping[co]:
            q = q.strip()
            sumb += marks_studB[q]
            suma += marks_studA[q]
        avg_cos[co] = (sumb / suma) * 100
    
    threshold_of_cos = {co: avg * (30 / 40) for co, avg in avg_cos.items()}
    
    student_scores = student_scores.iloc[:-17]
    
    students_above_threshold = {}
    for co, threshold in threshold_of_cos.items():
        percentage_column = f'{renaming_map[co]}_Percentage'
        if percentage_column in student_scores.columns:
            count_above_threshold = (student_scores[percentage_column] > threshold).sum()
            students_above_threshold[co] = count_above_threshold
        else:
            print(f"Percentage column for {co} not found in student_scores.")
    
    percentage_above_threshold = {}
    for co, count in students_above_threshold.items():
        percentage_above_threshold[co] = (count / class_strength) * 100
    
    avg = sum(percentage_above_threshold.values()) / len(percentage_above_threshold)
    avg = round(avg,2)
    for co, percentage in avg_cos.items():
        avg_cos[co] = round(percentage, 2)
    avg_co_levels = {}
    for co in percentage_above_threshold.keys():
        if percentage_above_threshold[co] < 60:
            avg_co_levels[co] = "Level 0"
        elif 60 <= percentage_above_threshold[co] <= 70:
            avg_co_levels[co] = "Level 1"
        elif 70 < percentage_above_threshold[co] <= 80:
            avg_co_levels[co] = "Level 2"
        else:
            avg_co_levels[co] = "Level 3"  
    if avg < 60:
        ans = "Level 0"
    elif 60 <= avg <= 70:
        ans = "Level 1"
    elif 70 < avg <= 80:
        ans = "Level 2"
    else:
        ans = "Level 3"    
    return avg, ans,avg_cos,avg_co_levels,sheet_name