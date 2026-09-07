import math

def calculate_thermal_shock_score(temperatures, times, material_properties):
    """
    Calculates a thermal shock score based on temperature changes and material properties.
    A higher score indicates a more severe thermal shock event.

    Args:
        temperatures (list[float]): A list of temperature readings in Celsius.
        times (list[float]): A list of corresponding timestamps in seconds.
        material_properties (dict): A dictionary containing material properties:
            - 'youngs_modulus' (float): Young's Modulus in Pascals (Pa).
            - 'thermal_expansion_coeff' (float): Thermal Expansion Coefficient in 1/K.
            - 'thermal_conductivity' (float): Thermal Conductivity in W/(m*K).
            - 'critical_shock_threshold' (float): A material-specific threshold for what constitutes a significant shock.

    Returns:
        tuple: (max_shock_score, peak_time, risk_level)
               max_shock_score (float): The highest calculated thermal shock index.
               peak_time (float): The time at which the highest score occurred.
               risk_level (str): Categorization of the risk ('Low', 'Medium', 'High').
    """
    if len(temperatures) < 2 or len(temperatures) != len(times):
        raise ValueError("Temperatures and times lists must have at least two elements and be of equal length.")

    max_shock_score = 0.0
    peak_time = times[0]

    E = material_properties['youngs_modulus']
    alpha = material_properties['thermal_expansion_coeff']
    k = material_properties['thermal_conductivity']
    critical_threshold = material_properties.get('critical_shock_threshold', 1e10) # Default threshold

    # The scoring algorithm is based on a simplified thermal stress rate potential.
    # Higher E, alpha, and abs(delta_T)/delta_t lead to higher scores.
    # Lower k leads to higher thermal gradients and thus higher scores.

    for i in range(1, len(temperatures)):
        delta_T = temperatures[i] - temperatures[i-1]
        delta_t = times[i] - times[i-1]

        if delta_t <= 0: # Avoid division by zero or non-positive time intervals
            continue

        # CORE ALGORITHM CONCEPT: Calculate the instantaneous thermal shock index for this interval.
        # This formula is a simplification, aiming to capture the essence of how material properties
        # and temperature change rate contribute to thermal stress and potential shock.
        # It's a proxy for the severity of thermal stress induced per unit time.
        instant_shock_index = (E * alpha * abs(delta_T)) / (k * delta_t)

        if instant_shock_index > max_shock_score:
            max_shock_score = instant_shock_index
            peak_time = times[i]

    # Determine risk level based on the maximum score and a material-specific threshold
    if max_shock_score < critical_threshold * 0.5:
        risk_level = "Low"
    elif max_shock_score < critical_threshold * 1.5:
        risk_level = "Medium"
    else:
        risk_level = "High"

    return max_shock_score, peak_time, risk_level

# --- Example Usage ---

# Define example material properties (simplified for demonstration)
# Values are illustrative and not necessarily precise for real materials.
material_A = { # Example: A more thermal-shock resistant material (e.g., specialized ceramic)
    'name': 'Special Ceramic A',
    'youngs_modulus': 300e9,       # Pa (300 GPa)
    'thermal_expansion_coeff': 5e-6, # 1/K
    'thermal_conductivity': 20.0,  # W/(m*K)
    'critical_shock_threshold': 5e10 # Higher threshold for resistance
}

material_B = { # Example: A less thermal-shock resistant material (e.g., common glass)
    'name': 'Common Glass B',
    'youngs_modulus': 70e9,        # Pa (70 GPa)
    'thermal_expansion_coeff': 8e-6, # 1/K
    'thermal_conductivity': 1.0,   # W/(m*K)
    'critical_shock_threshold': 1e10 # Lower threshold for susceptibility
}

# Scenario 1: Gradual temperature change (low shock potential)
temps_gradual = [20.0, 25.0, 30.0, 35.0, 40.0, 35.0, 30.0]
times_gradual = [0, 10, 20, 30, 40, 50, 60] # 10-second intervals

# Scenario 2: Rapid cooling (high shock potential)
temps_rapid_cool = [100.0, 95.0, 80.0, 30.0, 25.0, 20.0]
times_rapid_cool = [0, 1, 2, 3, 4, 5] # 1-second intervals, significant drop from 80 to 30

# Scenario 3: Rapid heating (high shock potential)
temps_rapid_heat = [20.0, 25.0, 70.0, 85.0, 90.0, 95.0]
times_rapid_heat = [0, 1, 2, 3, 4, 5] # 1-second intervals, significant jump from 25 to 70

print("--- Thermal Shock Scoring Algorithm Demo ---")
print("\nScenario 1: Gradual Temperature Change")
score_a_gradual, time_a_gradual, risk_a_gradual = calculate_thermal_shock_score(
    temps_gradual, times_gradual, material_A
)
score_b_gradual, time_b_gradual, risk_b_gradual = calculate_thermal_shock_score(
    temps_gradual, times_gradual, material_B
)
print(f"  Material '{material_A['name']}': Max Score = {score_a_gradual:.2e} at t={time_a_gradual}s, Risk = {risk_a_gradual}")
print(f"  Material '{material_B['name']}': Max Score = {score_b_gradual:.2e} at t={time_b_gradual}s, Risk = {risk_b_gradual}")

print("\nScenario 2: Rapid Cooling Event")
score_a_rapid_cool, time_a_rapid_cool, risk_a_rapid_cool = calculate_thermal_shock_score(
    temps_rapid_cool, times_rapid_cool, material_A
)
score_b_rapid_cool, time_b_rapid_cool, risk_b_rapid_cool = calculate_thermal_shock_score(
    temps_rapid_cool, times_rapid_cool, material_B
)
print(f"  Material '{material_A['name']}': Max Score = {score_a_rapid_cool:.2e} at t={time_a_rapid_cool}s, Risk = {risk_a_rapid_cool}")
print(f"  Material '{material_B['name']}': Max Score = {score_b_rapid_cool:.2e} at t={time_b_rapid_cool}s, Risk = {risk_b_rapid_cool}")

print("\nScenario 3: Rapid Heating Event")
score_a_rapid_heat, time_a_rapid_heat, risk_a_rapid_heat = calculate_thermal_shock_score(
    temps_rapid_heat, times_rapid_heat, material_A
)
score_b_rapid_heat, time_b_rapid_heat, risk_b_rapid_heat = calculate_thermal_shock_score(
    temps_rapid_heat, times_rapid_heat, material_B
)
print(f"  Material '{material_A['name']}': Max Score = {score_a_rapid_heat:.2e} at t={time_a_rapid_heat}s, Risk = {risk_a_rapid_heat}")
print(f"  Material '{material_B['name']}': Max Score = {score_b_rapid_heat:.2e} at t={time_b_rapid_heat}s, Risk = {risk_b_rapid_heat}")
