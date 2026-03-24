import gurobipy as gp
from gurobipy import GRB

# 1. Input data

teachers = ["Bi","Chai", "Gu_B","Gu_X", "Huang", "Jin_M","Jin_X", "Li", "Lian","Liu_D", "Liu_F",
            "Liu_Q", "Lu", "Song", "Xia", "Yuan", "Zhang", "Zhao", "Zou"]

courses = {
    "Elementary Chinese I",
    "Elementary Chinese II",
    "Intermediate Chinese I",
    "Intermediate Chinese II",
    "Advanced Chinese I",
    "Advanced Chinese II",
    "Elementary Chinese for Advanced Beginners",
    "Intermediate Chinese for Advanced Beginners",
    "Advanced Chinese II for Heritage Learners",
    "Accelerated Intermediate Chinese I & II",
    "Shanghai Architecture for Chinese Language Learners",
    "Introduction to Conversational Chinese",
    "Introduction to Conversational Chinese - 4 credits",
    "Readings in contemporary Chinese Culture",
    "Performing Chinese Drama for Improved Oral Proficiency"
}

slot_energy_cost = 1063  # Based on previous calculations
course_cost = {c: slot_energy_cost for c in courses}

teacher_courses  = {
    "Bi": ["Advanced Chinese I", "Advanced Chinese II"],
    "Chai": ["Elementary Chinese II"],
    "Gu_B": ["Shanghai Architecture for Chinese Language Learners"],
    "Gu_X": ["Intermediate Chinese I", "Elementary Chinese for Advanced Beginners"],
    "Huang": ["Elementary Chinese I", "Intermediate Chinese for Advanced Beginners"],
    "Jin_M": ["Intermediate Chinese II", "Intermediate Chinese for Advanced Beginners"],
    "Jin_X": ["Elementary Chinese I", "Elementary Chinese II"],
    "Li": ["Elementary Chinese II"],
    "Lian": ["Intermediate Chinese II"],
    "Liu_D": ["Elementary Chinese II", "Intermediate Chinese II"],
    "Liu_F": ["Elementary Chinese II", "Introduction to Conversational Chinese"],
    "Liu_Q": ["Advanced Chinese II", "Intermediate Chinese for Advanced Beginners"],
    "Lu": ["Intermediate Chinese II", "Advanced Chinese II for Heritage Learners"],
    "Song": ["Intermediate Chinese I"],
    "Xia": ["Elementary Chinese II", "Introduction to Conversational Chinese - 4 credits"],
    "Yuan": ["Elementary Chinese II", "Intermediate Chinese II"],
    "Zhang": ["Intermediate Chinese II", "Readings in contemporary Chinese Culture"],
    "Zhao": ["Accelerated Intermediate Chinese I & II", "Performing Chinese Drama for Improved Oral Proficiency"],
    "Zou": ["Elementary Chinese II"]

}

time_slots = ["8:15-9:30", "9:45-11:00","11:15-12:30", "12:45-2:00", "2:15-3:30", "3:45-5:00", "5:15-6:30"]
days = ["Mon", "Tue", "Wed", "Thu", "Fri"]

capacities = {
    ("Mon", "8:15-9:30"): 6, ("Mon", "9:45-11:00"): 4, ("Mon", "11:15-12:30"): 9,
    ("Mon", "12:45-2:00"): 5, ("Mon", "2:15-3:30"): 6, ("Mon", "3:45-5:00"): 4, ("Mon", "5:15-6:30"): 2,
    ("Tue", "8:15-9:30"): 5, ("Tue", "9:45-11:00"): 5, ("Tue", "11:15-12:30"): 9,
    ("Tue", "12:45-2:00"): 5, ("Tue", "2:15-3:30"): 5, ("Tue", "3:45-5:00"): 5, ("Tue", "5:15-6:30"): 2,
    ("Wed", "8:15-9:30"): 6, ("Wed", "9:45-11:00"): 4, ("Wed", "11:15-12:30"): 9,
    ("Wed", "12:45-2:00"): 5, ("Wed", "2:15-3:30"): 6, ("Wed", "3:45-5:00"): 4, ("Wed", "5:15-6:30"): 2,
    ("Thu", "8:15-9:30"): 5, ("Thu", "9:45-11:00"): 5, ("Thu", "11:15-12:30"): 9,
    ("Thu", "12:45-2:00"): 5, ("Thu", "2:15-3:30"): 5, ("Thu", "3:45-5:00"): 4, ("Thu", "5:15-6:30"): 2,
    ("Fri", "8:15-9:30"): 1, ("Fri", "9:45-11:00"): 0, ("Fri", "11:15-12:30"): 2,
    ("Fri", "12:45-2:00"): 1, ("Fri", "2:15-3:30"): 0, ("Fri", "3:45-5:00"): 0, ("Fri", "5:15-6:30"): 0
}

blocked_slots = [("Fri", "2:15-3:30"), ("Fri", "3:45-5:00"), ("Fri", "5:15-6:30")] # Potential times for university meetings (assumption)

unavailable_teachers = {} # Left empty due to uncertainty, can be modified for future improvements

# 2. Create model
model = gp.Model("CourseSchedulingEnergy")

# 3. Decision variables
x = model.addVars(
    [(t, c, d, s)
     for t in teachers
     for c in teacher_courses[t]
     for d in days
     for s in time_slots],
    vtype=GRB.BINARY,
    name="x"
)

# 4. Objective: minimize total energy cost
model.setObjective(
    gp.quicksum(course_cost[c] * x[t, c, d, s] for t, c, d, s in x),
    sense=GRB.MINIMIZE
)

# 5. Constraints

# (1.1) Blocked time slots
for t in teachers:
    for c in teacher_courses[t]:
        for d, s in blocked_slots:
            if (t, c, d, s) in x:
                model.addConstr(x[t, c, d, s] == 0, name=f"blocked_{t}_{c}_{d}_{s}")

# (1.2) Unavailable teacher time slots
for t in unavailable_teachers:
    for d, s in unavailable_teachers[t]:
        for c in teacher_courses[t]:
            if (t, c, d, s) in x:
                model.addConstr(x[t, c, d, s] == 0, name=f"unavailable_{t}_{c}_{d}_{s}")

# (2) Each course must be scheduled at least once
for c in courses:
    model.addConstr(
        gp.quicksum(x[t, c, d, s]
                    for t in teachers if c in teacher_courses[t]
                    for d in days for s in time_slots) >= 1,
        name=f"schedule_course_{c}"
    )

# (3) Each course taught by a teacher is assigned exactly once
for t in teachers:
    for c in teacher_courses[t]:
        model.addConstr(
            gp.quicksum(x[t, c, d, s] for d in days for s in time_slots) == 1,
            name=f"unique_slot_{t}_{c}"
        )

# (4) A teacher cannot teach more than one course per time slot
for t in teachers:
    for d in days:
        for s in time_slots:
            model.addConstr(
                gp.quicksum(x[t, c, d, s] for c in teacher_courses[t] if (t, c, d, s) in x) <= 1,
                name=f"one_course_{t}_{d}_{s}"
            )

# (5) Capacity constraint for each time slot
for d in days:
    for s in time_slots:
        model.addConstr(
            gp.quicksum(x[t, c, d, s] for t in teachers for c in teacher_courses[t] if (t, c, d, s) in x) <= capacities[d, s],
            name=f"capacity_{d}_{s}"
        )

# 6. Results
model.optimize()

if model.status == GRB.OPTIMAL:
    print(f"\nOptimal solution found! Total energy cost: {model.objVal:.2f} RMB\n")
    print("Optimized schedule:")
    for t in teachers:
        for c in teacher_courses[t]:
            for d in days:
                for s in time_slots:
                    if x[t, c, d, s].X > 0.5:
                        print(f"{t}: {c} at {s} on {d}")
else:
    print("\nNo feasible solution found.")

# Count unique (day, slot) pairs in the optimized schedule
used_slots = set()

for t in teachers:
    for c in teacher_courses[t]:
        for d in days:
            for s in time_slots:
                if x[t, c, d, s].X > 0.5:
                    used_slots.add((d, s))

print(f"\nOptimized schedule uses {len(used_slots)} unique room-time sessions.")

