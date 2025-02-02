import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math as m
from gurobipy import Model, GRB, quicksum



def print_new_assignment(model, x, SRs, bricks):
    
    if model.status == GRB.OPTIMAL:
        print("Optimal Value:", model.objVal)

        sr_assignments = {j: [] for j in SRs}
        for i in bricks:
            for j in SRs:
                if x[i, j].X > 0.5:
                    sr_assignments[j].append(i + 1)

        for j in SRs:
            print(f"SR {j+1} was assigned bricks:", sr_assignments[j])
    else:
        print("No optimal solution found.")


# Function to filter weakly non-dominated solutions
def filter_non_dominated(solutions):
    
    non_dominated = []
    for i, (epsilon_i, dist_i, disp_i, assign_i) in enumerate(solutions):
        dominated = False
        for j, (epsilon_j, dist_j, disp_j, assign_j) in enumerate(solutions):
            if i != j and dist_j <= dist_i and disp_j <= disp_i:
                dominated = True
                break
        if not dominated:
            non_dominated.append((epsilon_i, dist_i, disp_i, assign_i))
            
    return non_dominated


def find_pareto_solutions(workload_ranges, solver_function, assignment_type="binary", delta_epsilon=0.1):

    all_results = {}

    for workload_min, workload_max in workload_ranges:
        solutions = []
        epsilon = np.inf 

        while True:
            distance, disruption, assignment = solver_function(epsilon, workload_min, workload_max, assignment_type=assignment_type)
            if distance is not None:
                solutions.append((epsilon, distance, disruption, assignment))
                epsilon = disruption - delta_epsilon  # Reduce epsilon iteratively
            else:
                break

        non_dominated_solutions = filter_non_dominated(solutions)
        all_results[(workload_min, workload_max)] = non_dominated_solutions

    return all_results


def plot_decision_space(results, plot_title):
    
    plt.figure(figsize=(10, 7))
    
    for (workload_min, workload_max), solutions in results.items():
        distances = [dist for _, dist, _, _ in solutions]   
        disruptions = [disp for _, _, disp, _ in solutions]  
        
        plt.scatter(distances, disruptions, label=f"[{workload_min}, {workload_max}]")
    
    plt.title(plot_title)
    plt.xlabel("Distance (f₁)")
    plt.ylabel("Disruption (f₂)")
    plt.legend(title="Workload Ranges")
    plt.grid(True)
    plt.show()


def plot_non_dominated_across_all_offices(total_results):
    
    cmap = plt.cm.get_cmap("tab20", len(total_results)) 
    plt.figure(figsize=(10, 7))

    for idx, (i, solutions) in enumerate(total_results.items()):
        distances = [dist for _, dist, _, _ in solutions]   
        disruptions = [disp for _, _, disp, _ in solutions]  
        
        plt.scatter(distances, disruptions, label=f"Office = {str(int(i)+1)}", color=cmap(idx))

    plt.title("Non-Dominated Solutions in the Decision Space")
    plt.xlabel("Distance (f₁)")
    plt.ylabel("Disruption (f₂)")
    plt.legend(title="Possible offices", bbox_to_anchor=(1.05, 1), loc="upper left") 
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_globally_non_dominated_across_all_offices(total_results):
    
    total_solutions = [sol for i in range(18) for sol in list(total_results.values())[i]]
    saved_solutions = filter_non_dominated(total_solutions)
    
    liste = []

    for i, sol in enumerate(saved_solutions): 
        for idx, (j, solutions) in enumerate(total_results.items()):
            if sol in solutions:
                liste.append((idx, sol))
                
    cmap = plt.cm.get_cmap("tab20", len(total_results)) 
    plt.figure(figsize=(10, 7))

    for (idx, sol) in liste:
        dist = sol[1] 
        disp = sol[2] 
        
        plt.scatter(dist, disp, label=f"Office = {str(idx+1)}", color=cmap(idx))

    plt.title("Non-Dominated Solutions in the Decision Space")
    plt.xlabel("Distance (f₁)")
    plt.ylabel("Disruption (f₂)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    