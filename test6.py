import pandas as pd

dictTest = {"title":"abc","url":"xyz","review":['a','b','c','d']}
df = pd.DataFrame(dictTest)
df.to_excel('text.xlsx',merge_cells= True)