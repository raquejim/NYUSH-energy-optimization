# Optimization of NYU Shanghai’s Energy Performance: Course Scheduling for Heating/Cooling Management

This project presents an optimization model that aims to lower the energy consumption of HVAC technologies at the NYU Shanghai academic building through more efficient course scheduling of faculty. This approach was implemented solely to the Chinese Language Department. 

## Tools 
- Python
- Gurobi
  
## Files 
- `script.js` – main Python code
- `results/` – decision variables, parameter explanation table, schedule before and after optimization, and sensitivity analysis 
  
## Data Sourcing 
Since this model is targeted towards the NYU Shanghai academic building, most of the data was facilitated by the school’s Faculty Management team or collected through information available on the school’s Albert website.

## Results 
![Decision Variables](results/.png)
![Parameter Explanation Table](results/mean-values.png)
![Objective Function](results/surfacetemp-vs-builtuparea-plot.png)
![Non-optimized Schedule](results/.png)
![Optimized Schedule](results/.png)
![Sensitivity Analysis](results/.png)

The total energy cost (Zd) for the optimized schedule was projected to be 34,016 RMB. This is calculated by multiplying the cost per course with the number of courses’ groups. By performing the same calculation for the original schedule, we get that the Zd is 41,457 RMB. By reducing the number of courses’ groups from 39 (original schedule) to 32 (optimized schedule), NYU Shanghai could have saved approximately 7,441 RMB for 2025 spring semester just through heating/cooling of one department alone. Scaling this model across other departments could significantly reduce the school’s environmental footprint as well as increase its yearly budget. 

For more information, please refer to the full report down below. 

## Gurobi Code 
[Click here for the Python script](https://code.earthengine.google.com/7671ca8ea04cc0816d6e3dacc1dcacb2)

## Full Report 
[Click here for the full report](https://code.earthengine.google.com/7671ca8ea04cc0816d6e3dacc1dcacb2)
