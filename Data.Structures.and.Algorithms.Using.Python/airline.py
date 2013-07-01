from simulation import TicketCounterSimulation
def main():
    numMins = int(raw_input("Number of minutes to simulate: "))
    numAgents = int(raw_input("Number of ticket agents: "))
    serviceTime = int(raw_input("Average service time per passenger: "))
    arrivalTime = int(raw_input("Average time between passenger arrival: "))

    sim = TicketCounterSimulation(numAgents, numMins, arrivalTime, serviceTime)
    sim.run()
    sim.printResults()

main()
