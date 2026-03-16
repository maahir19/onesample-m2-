import streamlit as st
import numpy as np
from scipy.stats import t
from statistics import stdev

# Function
def One_Sample_T_Test_with_data(x, Mu, alternative):
    n = len(x)
    x_bar = np.mean(x)
    sd = stdev(x)
    alpha = 0.05
    df = n - 1
    sd_error = sd / np.sqrt(n)

    t_cal = (x_bar - Mu) / sd_error

    result = {}
    result["t_cal"] = t_cal

    if alternative == "less":
        p_value = t.cdf(t_cal, df)
        t_left = t.ppf(alpha, df)

        result["p_value"] = p_value
        result["t_left"] = t_left
        result["decision"] = "Hypothesis rejected" if t_cal < t_left else "Hypothesis not rejected"

    elif alternative == "greater":
        p_value = 1 - t.cdf(t_cal, df)
        t_right = t.ppf(1 - alpha, df)

        result["p_value"] = p_value
        result["t_right"] = t_right
        result["decision"] = "Hypothesis rejected" if t_cal > t_right else "Hypothesis not rejected"

    elif alternative == "two-sided":
        p_value = 2 * (1 - t.cdf(abs(t_cal), df))
        t_left = t.ppf(alpha/2, df)
        t_right = t.ppf(1 - alpha/2, df)

        result["p_value"] = p_value
        result["t_left"] = t_left
        result["t_right"] = t_right
        result["decision"] = "Hypothesis rejected" if (t_cal < t_left or t_cal > t_right) else "Hypothesis not rejected"

    return result


# Streamlit UI
st.title("One Sample T-Test Calculator")

data_input = st.text_input(
    "Enter data values separated by commas",
    "52,55,49,50,58,54,53,51"
)

mu = st.number_input("Enter Hypothesized Mean (Mu)", value=50.0)

alternative = st.selectbox(
    "Select Alternative Hypothesis",
    ["less", "greater", "two-sided"]
)

if st.button("Run Test"):

    data = [float(i) for i in data_input.split(",")]

    result = One_Sample_T_Test_with_data(data, mu, alternative)

    st.subheader("Results")

    st.write("t_cal =", result["t_cal"])
    st.write("p_value =", result["p_value"])

    if "t_left" in result:
        st.write("t_left =", result["t_left"])

    if "t_right" in result:
        st.write("t_right =", result["t_right"])

    st.success(result["decision"])