# Fertility https://data.worldbank.org/indicator/SP.DYN.TFRT.IN?locations=CZ

from IPython.display import display
import pandas as pd
import matplotlib.pyplot as plt


print("Write correct name of country you want to show and thn press Enter.")
input_value = input()


mortality_df = pd.read_csv('Mortality_en_csv_v2.csv', skiprows=4, delimiter=',')
fertility_df = pd.read_csv('Fertility_en_csv_v2.csv', skiprows=4, delimiter=',')

mortality_cz_df = mortality_df[mortality_df['Country Name'] == input_value]
fertility_cz_df = fertility_df[fertility_df['Country Name'] == input_value]


#print(mortality_cz_df.columns.tolist())

# Drop unnecessary columns
mortality_cz_df = mortality_cz_df.drop(columns=['Country Code','Indicator Name','Indicator Code'])
fertility_cz_df = fertility_cz_df.drop(columns=['Country Code', 'Indicator Name', 'Indicator Code'])


#Transpone rest of data and use Country Name as Index
mortality_cz_df = mortality_cz_df.set_index('Country Name').T.rename_axis('Year').reset_index()

# Rename the 'Czechia' column to 'Value' in both datasets
mortality_cz_df = mortality_cz_df.rename(columns={input_value: 'Value'})


# Or use melt to unpivot table
value_vars = fertility_cz_df.drop(columns=['Country Name']).columns.tolist()
fertility_cz_df = pd.melt(fertility_cz_df,
                         id_vars=['Country Name'],
                         value_vars= value_vars,
                         var_name='Year',
                         value_name='Value')

# Convert 'Year' column to numeric for proper plotting
mortality_cz_df['Year'] = pd.to_numeric(mortality_cz_df['Year'], errors='coerce')
fertility_cz_df['Year'] = pd.to_numeric(fertility_cz_df['Year'], errors='coerce')
# Display the cleaned data
display(mortality_cz_df.head(),  fertility_cz_df.head())

# Plot both mortality and natality trends on the same plot
plt.figure(figsize=(15, 6))
plt.plot(mortality_cz_df['Year'], mortality_cz_df['Value'], label='Mortality Rate', color='red')
plt.plot(fertility_cz_df['Year'], fertility_cz_df['Value'], label='Fertility Rate', color='green')
print(mortality_cz_df)


# Add labels, title, and legend
plt.xlabel('Year')
plt.ylabel('Value')
plt.xlim(1960.0, 2020)
#plt.ylim(1960.0, 2020)
plt.title(f'Mortality and Natality Rates in {input_value} Over Time')
plt.legend()
plt.grid(True)

# Show the plot
plt.show()

print(mortality_cz_df.columns.tolist())


