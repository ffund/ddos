# Distributed Denial of Service Attacks
Using GENI to reproduce the results of:
[1] Lau, Felix, et al. "Distributed denial of service attacks." Systems, Man, and Cybernetics, 2000 IEEE International Conference on. Vol. 3. IEEE, 2000.

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
As shown in the figure, a client tries to reach a service through a single hop network with a router connecting it to the server.
Assuming that an attacker takes control of a set of zombie machines connected to the same router, we simulate how he/she can make the service unavailable to the client by targeting the router and overwhelming its queue.
As an outcome, packets will be droped while the attack is in progress and the client will experience a considerable drop in its bandwidth.

![sample.png](https://raw.githubusercontent.com/aaghdai/ddos/master/Figures/sample.png)

The ultimate goal of the router is to forward packets from ligitimate users.
Therefore, the key metric in this experiment is the rate at which client communicates with the server while the attack is in progress.
A rate of zero indicates no connectivity and a rate drop indicates service degradation.

In this project we are interested to reproduce two specific figures from Lau et. al paper.
Figures 4 and 5, which show the performance of the router under DropTail and Random Early Detection (RED) buffer management policies.
Authors of the original paper show that under DropTail attackers can fully deny the client of access to the server, however, under RED, client can still communicate with the server, although at a slower pace and with degraded quality of service.
### Results ###
Figure 4 of [1]:
![fig4.png](https://raw.githubusercontent.com/aaghdai/ddos/master/Figures/fig4.png)

Figure 5 of [1]:
![fig5.png](https://raw.githubusercontent.com/aaghdai/ddos/master/Figures/fig5.png)

### Run My Experiment ###
<ol>
<li>Create an architecture with a client, a server, and 12 attackers all connected to a router in a star network. An RSPEC for this topology is included in GENI folder.</li>
<li>Install prerequierements:
<ol>
<li>Install D-ITG on client, server, and attackers:
<pre><code> $ sudo apt-get update
 $ sudo apt-get install d-itg </code></pre></li>
<li> In order to capture and analyze the traces router needs scapy and matplotlib packages:
<pre><code> $ sudo apt-get update
 $ sudo apt-get install python-scapy python-matplotlib </code></pre></li>
</ol>
</li>
</ol>

### Notes ###


