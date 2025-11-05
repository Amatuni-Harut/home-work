import pandas as pd
import os
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from fastapi import FastAPI

app=FastAPI()
engine = create_engine('sqlite:///company.db')

df = pd.read_csv('employees.csv')
df.to_sql('employees', engine, if_exists='replace', index=False)

result = pd.read_sql_table('employees', engine)
print(result)

df = pd.read_sql_table('employees', engine)
result = df[df['salary'] > 5000].sort_values('salary', ascending=False)
print(result)


df = pd.read_csv('departments.csv')
df.to_sql('departments', engine, if_exists='replace', index=False)

employees = pd.read_sql_table('employees', engine)
depts = pd.read_sql_table('departments', engine)

merged = employees.merge(depts, left_on='department', right_on='department_name')
print(merged[['name', 'salary', 'department_name']])


avg_salary = merged.groupby('department_name')['salary'].mean()
print(avg_salary)


employees['salary'] = employees['salary'].astype(float)
employees.loc[employees['department'] == 'IT', 'salary'] *= 1.10
print(employees[employees['department'] == 'IT'])

updated = pd.read_sql_table('employees', engine)
print(updated[updated['department'] == 'IT'])


employees = pd.read_sql_table('employees', engine)
depts = pd.read_sql_table('departments', engine)

merged = employees.merge(depts, left_on='department', right_on='department_name')
avg_salary = merged.groupby('department_name')['salary'].mean()

avg_salary.plot(kind='bar')
plt.title('midle salary')
plt.xlabel("department")
plt.ylabel('midle salary')
plt.tight_layout()
graph_path = os.path.join( 'avg_salary.png')
plt.savefig(graph_path)

print(f"graph saved to {graph_path}")

# =================fastapi endpoints====================
@app.get("/employees")
def get_employees():
    df=pd.read_sql_table('employees', engine)
    return df.to_dict("records")

@app.get("/avg-salery")
def get_avg_salery():
    emp=pd.read_sql_table('employees', engine)
    deps=pd.read_sql_table('departments', engine)
    
    emp['department'] = emp['department'].astype(str)
    deps['department_name'] = deps['department_name'].astype(str)
    merged = emp.merge(deps, left_on='department', right_on='department_name')
    
    avg=merged.groupby('department_name')['salary'].mean().reset_index()
    return avg.to_dict("records")

@app.get("/top employees")
def get_top_employees():
    df=pd.read_sql_table('employees', engine)
    top=df.nlargest(3,'salary')
    return top.to_dict("records")
