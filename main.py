import numpy as np
import matplotlib.pyplot as plt

simulations = 50
p = float(input('Probability of immunisation: '))
efficacy = float(input('Vaccine efficacy: '))
mortality = float(input('Mortality rate: '))
p_immune = 1 - efficacy

# Lists for unimmunsed, infected
list_unvaxxed = np.zeros(simulations)
list_infected = np.zeros(simulations)
list_deceased = np.zeros(simulations)
list_fraction_unvaxxed = np.zeros(simulations)
list_fraction_total = np.zeros(simulations)
list_fraction_deceased = np.zeros(simulations)

for sim_count in range(simulations):
    # Empty nxn lattice of patients
    size = 25
    patients = np.zeros((size, size))

    # Function for spreading infection
    def infect(x, y):
        def check(x, y):
            if patients[x][y] == 0:
                patients[x][y] = 2
                infect(x, y)
            elif patients[x][y] == 1 and np.random.rand() < p_immune:
                patients[x][y] = 2
                infect(x, y)
            elif patients[x][y] == 2 and np.random.rand() < mortality:
                patients[x][y] = 3

        if y < (size - 1) and patients[x][y+1] == 0:
            patients[x][y+1] = 2
            infect(x, y+1)
        if y > 0 and patients[x][y-1] == 0:
            patients[x][y-1] = 2
            infect(x, y-1)
        if x < (size - 1) and patients[x+1][y] == 0:
            patients[x+1][y] = 2
            infect(x+1, y)
        if x > 0 and patients[x-1][y] == 0:
            patients[x-1][y] = 2
            infect(x-1, y)

    # Number of immunised patients
    vaxxed = int(p * (size**2))

    # Fill in immunised patients
    while np.count_nonzero(patients == 1) <= vaxxed:
        # Generate random numbers
        randnum = np.random.rand()
        x = int(randnum*(size**2)) % size
        y = int(randnum*(size**2)) // size
    
        # Vaccinate
        patients[x][y] = 1

    #Count initial number of immunised patients and add to array
    total_unvaxxed = np.count_nonzero(patients == 0)
    list_unvaxxed[sim_count] = total_unvaxxed

    # Find patient zero
    for k in range(size**2):
        m = np.random.randint(0, size)
        n = np.random.randint(0, size)

        if patients[m][n] == 1:
            continue
        else:
            patients[m][n] = 2
        break

    # Define start point
    x = m
    y = n

    # Spread infection
    infect(m,n)

    #Count final number of infected patients and add to array
    infection_count = np.count_nonzero(patients == 2)
    list_infected[sim_count] = infection_count

    # Plot all simulations to one diagram
    plt.subplot(5, 10, (sim_count+1))
    plt.imshow(patients)
    plt.axis('off')
    plt.set_cmap('OrRd')
    plt.savefig('infection.png')

# Calculate fraction who get infected
for k in range(simulations):
    # Fraction of unimmunised who get infected
    list_fraction_unvaxxed[k] = list_infected[k] / list_unvaxxed[k]

    # Fraction of total population who get infected
    list_fraction_total[k] = list_infected[k] / (size**2)

    # Fraction of total population who perish
    list_fraction_deceased[k] = list_deceased[k] / (size**2)

# Calculate mean and stdev for unimmunised
mean_fraction_unvaxxed = np.mean(list_fraction_unvaxxed)
print('Mean fraction of unvaccinated who get infected: ', mean_fraction_unvaxxed)
stdev_fraction_unvaxxed = np.std(list_fraction_unvaxxed)
print('Standard deviation unvaxxed: ', stdev_fraction_unvaxxed)
# Plot histogram of unimmunised population
plt.figure()
plt.hist(list_fraction_unvaxxed, color='maroon')
plt.xlabel('Fraction of unimmunised population infected')
plt.ylabel('Number of simulations')
plt.xlim([0, 1])
plt.title('Probability Distribution for Infection of Unimmunised Population')
plt.savefig('histogram_unvaxxed.png')

# Calculate mean and stdev for mortality
mean_fraction_deceased = np.mean(list_fraction_deceased)
print('Mean fraction of total population who perish: ', mean_fraction_deceased)
stdev_fraction_deceased = np.std(list_fraction_deceased)
print('Standard deviation deceased: ', stdev_fraction_deceased)
# Plot histogram of perished population
plt.figure()
plt.hist(list_fraction_deceased, color='maroon')
plt.xlabel('Fraction of total population perished')
plt.ylabel('Number of simulations')
plt.xlim([0, 1])
plt.title('Probability Distribution for Mortality of Total Population')
plt.savefig('histogram_deceased.png')

# Calculate mean and stdev for total
mean_fraction_total = np.mean(list_fraction_total)
print('Mean fraction of total population who get infected: ', mean_fraction_total)
stdev_fraction_total = np.std(list_fraction_total)
print('Standard deviation total: ', stdev_fraction_total)
# Plot histogram of total population
plt.figure()
plt.hist(list_fraction_total, color='maroon')
plt.xlabel('Fraction of total population infected')
plt.ylabel('Number of simulations')
plt.xlim([0, 1])
plt.title('Probability Distribution for Infection of Total Population')
plt.savefig('histogram_total.png')