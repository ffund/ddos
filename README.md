# Distributed Denial of Service Attacks
Reproducing the results of: Lau, Felix, et al. "Distributed denial of service attacks." Systems, Man, and Cybernetics, 2000 IEEE International Conference on. Vol. 3. IEEE, 2000.
Using GENI.

### Introduction ###
Here we reproduce Figures 4 and 5 of Distributed Denial of Service Attacks paper.
The objective of this experiment is to show how effective Distributed Denial of Service (DDOS) attacks are under two different queueing schemes: Drop Tail and Random Early Detection.
It shows whether or not legitimate users can obtain desired service while a DDOS attack is in process.
Results are verified using a GENI testbed.

It takes about 30 minutes to reproduce my results.

### Background ###
A Denial of Service (DoS) attack is defined as an attempt to make a machine or a resource unavailable to its legitimate users.
When we have more than one source attacing the target, it is called a Distributed DoS (DDoS).
Typically, attackers try to take control of a lot of unique IP addresses (Zombie Machines) and use them to exhaust a resource either on the target machine, or the network that connects legitimate users to the target machine/s.

In this context, it is intersting to see how queueing networks will perform if they are targeted by a DDOS attacks.
Felix Lau et. al tried to find an answer to this question in 2000, and published their results in the paper we cite today.

In their experiment, they have simulated the simplest of DDOS attacks, when a router is targeted by the attacker aiming at overwhelming its queues and authors have analyzed how different queueing management techniques perform under the DDOS attack.
![sample.png](https://raw.githubusercontent.com/aaghdai/ddos/master/Figures/sample.png)
As shown in the figure, a client tries to reach a service through a single hop network with a router connecting it to the server.
Assuming that an attacker takes control of a set of zombie machines connected to the same router, we simulate how he/she can make the service unavailable to the client by targeting the router and overwhelming its queue.
As an outcome, packets will be droped while the attack is in progress and the client will experience a considerable drop in its bandwidth.

The ultimate goal of the router is to forward packets from ligitimate users.
Therefore, the key metric in this experiment is the rate at which client communicates with the server while the attack is in progress.
A rate of zero indicates no connectivity and a rate drop indicates service degradation.

In this project we are interested to reproduce two specific figures from Lau et. al paper.
Figures 4 and 5, which show the performance of the router under DropTail and Random Early Detection (RED) buffer management policies.
### Results ###

### Run My Experiment ###

### Notes ###


