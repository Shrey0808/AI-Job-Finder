import pandas as pd


# Provide the full path to the CSV file
file_path = r"C:\Users\KIIT\OneDrive - kiit.ac.in\Desktop\Desktop Items\Upflairs Internship\jobfilter\Job-scrapper-front-end\job.csv"

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Convert the DataFrame to a dictionary
dc = df.to_dict()

for i,(k,v) in enumerate(dc.items()):
    if i in [0,1,2,3,4,5,6]:
        continue
    print(k)
    print(v)
    break

# {
#     'title':{0:'dfsf',1:'sfdaf'},
#     'sdfdaf':{0:'dfsf',1:'sfdaf'},
#     'sdfdawf':{0:'dfsf',1:'sfdaf'},
#     'fasfwdfs':{0:'dfsf',1:'sfdaf'}
# }