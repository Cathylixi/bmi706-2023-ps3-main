import altair as alt
import pandas as pd
import streamlit as st

### P1.2 ###

# Move this code into `load_data` function {{

# }}


@st.cache
def load_data():
    ## {{ CODE HERE }} ##
    cancer_df = pd.read_csv("https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/cancer_ICD10.csv").melt(  # type: ignore
        id_vars=["Country", "Year", "Cancer", "Sex"],
        var_name="Age",
        value_name="Deaths",
    )

    pop_df = pd.read_csv("https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/population.csv").melt(  # type: ignore
        id_vars=["Country", "Year", "Sex"],
        var_name="Age",
        value_name="Pop",
    )

    df = pd.merge(left=cancer_df, right=pop_df, how="left")
    df["Pop"] = df.groupby(["Country", "Sex", "Age"])["Pop"].fillna(method="bfill")
    df.dropna(inplace=True)

    df = df.groupby(["Country", "Year", "Cancer", "Age", "Sex"]).sum().reset_index()
    df["Rate"] = df["Deaths"] / df["Pop"] * 100_000

    return df


# Uncomment the next line when finished
df = load_data()

### P1.2 ###


st.write("## Age-specific cancer mortality rates")

### P2.1 ###
# replace with st.slider
year = st.slider('Year', min_value=df['Year'].min(), max_value=df['Year'].max(), value=df['Year'].min())
subset = df[df['Year'] == year]
### P2.1 ###


### P2.2 ###
# replace with st.radio
sex = st.radio("Sex", options= ['F','M'])
subset = df[df['Sex'] == sex]

### P2.2 ###


### P2.3 ###
# replace with st.multiselect
# (hint: can use current hard-coded values below as as `default` for selector)
countries = [
    "Austria",
    "Germany",
    "Iceland",
    "Spain",
    "Sweden",
    "Thailand",
    "Turkey",
]
countries_subset = st.multiselect('Countries', options=subset['Country'].unique(), default=countries)
subset = subset[subset['Country'].isin(countries_subset)]
### P2.3 ###


### P2.4 ###
# replace with st.selectbox
cancer = subset['Cancer'].unique()
cancer_type = st.selectbox('Cancer', options=cancer)
subset = subset[subset['Cancer'] == cancer_type]
### P2.4 ###


### P2.5 ###
ages = [
    "Age <5",
    "Age 5-14",
    "Age 15-24",
    "Age 25-34",
    "Age 35-44",
    "Age 45-54",
    "Age 55-64",
    "Age >64",
]

chart = alt.Chart(subset).mark_rect().encode(
    x=alt.X("Age", sort=ages),
    y=alt.Y('Country:N', title="Country"),
    color=alt.Color('Rate:Q', title="Mortality rate per 100k",
                scale=alt.Scale(type='log', domain=(0.01, 100), clamp=True)),
    tooltip=[alt.Tooltip('Rate:Q', title="Mortality Rate per 100k")]
).properties(
    title=f"{cancer_type} mortality rates for {'males' if sex == 'M' else 'females'} in {year}"
)
### P2.5 ###

st.altair_chart(chart, use_container_width=True)

countries_in_subset = subset["Country"].unique()
if len(countries_in_subset) != len(countries):
    if len(countries_in_subset) == 0:
        st.write("No data avaiable for given subset.")
    else:
        missing = set(countries) - set(countries_in_subset)
        st.write("No data available for " + ", ".join(missing) + ".")



