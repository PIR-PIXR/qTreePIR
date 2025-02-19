<p align="center">
  <img width="250" height="230" src="https://github.com/PIR-PIXR/Certificate-Transparency-Logs/assets/102839948/530caacf-868e-464c-995b-04e995bc02bc">
</p>

# *q*TreePIR: Efficient Private Retrieval for Verkle Proofs via Ancestral $q$-ary Tree Coloring

## Abstract
The paper introduces innovative privacy mechanisms for enabling light clients to securely retrieve inclusion proof along arbitrary root-to-leaf path in $q$-ary trees, such as Verkle trees. *q*TreePIR, which develops from TreePIR, outperforms the state-of-the-art Probabilistic Batch Codes (PBC) ([Angel et al. IEEE S&P'18](https://doi.ieeecomputersociety.org/10.1109/SP.2018.00062)) in all metrics, achieving $3\times$ lower total storage and $1.5\times$ less communication cost and $1.5-2\times$ faster max/total server computation time and client query generation time. *q*TreePIR achieves a complexity of $\mathcal{O}(nh(\log_2 q + \log_2 h))$ in partition the tree in $h$ balance sub-databases. It can efficiently generate balanced sub-databases for a perfect 256-ary tree containing $2^{32}$ leaves in under 30 seconds. Additionally, the *q*TreePIR-Indexing algorithm allocates an arbitrary node's position in the path within its sub-database. With a complexity of $\mathcal{O}(qh^2)$ for this algorithm, it showcases impressive speed by indexing inclusion proof nodes for the ideal 256-ary tree of $2^{32}$ leaves in approximately two milliseconds. Most notably, *q*TreePIR's *polylog*-complexity indexing algorithm is $500\times$ faster than PBC for 256-ary tree of $2^{24}$ leaves.

---
## Experimental setup
Our experiments ran within Ubuntu 22.04 LTS environments. Our local machine (Intel® Core™ i5-1035G1 CPU @ 1.00GHz×8, 15GB System memory) served as the infrastructure for running the PIR Client, Orchestrator, ATC, *q*TreePIR-Indexing, and PBC (refer to Figure 1). For PIR Servers, we ran our experiments using up to 36 PIR servers on the Amazon m5.8xlarge instance (Intel® Xeon® Platinum 8175M CPU @ 2.50GHz, 32 vCPUs, 128GB System memory) that cost around $\$1.92$ per hour, using only one core. In Table 1}, we used until $36$ instances because, with $h = 24$, PBC generates $\lceil 1.5 \times h \rceil = 36$ databases, each of server processed a PIR database in parallel while our *q*TreePIR employed only $24$ servers. We choose an arbitrary C-PIR such as SealPIR \cite{angel2018} for our baseline implementations. In our experiments, the Verkle tree nodes are 32 bytes in size. Each experiment was repeated ten times for each tree's size in the Table \ref{table:expTrees}, changing the number of leaves ($n$) from $2^{10}$ to $2^{24}$ and the number of children ($q$) in the set $\{2, 16, 128, 256\}$. The average values were then calculated. We also utilize the HTTP/2 protocol in conjunction with gRPC version 35.0.0, developed by Google, to connect client and servers in the parallel PIR phase.


<p align="center">
  <img width="600" height="300" src="https://github.com/user-attachments/assets/f56fb51e-0672-44ee-a574-f2cd6f764828">
</p>
<p align="center"><b>Figure 1: Process Architecture</b></p>


**Table 1**: A comprehensive experimental evaluation across varying $q$-ary tree sizes (from $2^{10}$ to $2^{24}$ leaves ($n$)), children numbers (from $2$ to $256$ ($q$)), and tree heights ($h$) corresponding with number of PIR servers are required to handle concurrent client queries.

| **n**  | $2^{10}$ | $2^{11}$ | $2^{12}$ | $2^{13}$ | $2^{14}$ | $2^{15}$ | $2^{16}$ | $2^{17}$ | $2^{18}$ | $2^{19}$ | $2^{20}$ | $2^{21}$ | $2^{22}$ | $2^{23}$ | $2^{24}$ |
|--------|----------|----------|----------|----------|----------|----------|----------|----------|----------|----------|----------|----------|----------|----------|----------|
| **q = 2** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **h**  | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 |
| $m_{qTreePIR}$ | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 |
| $m_{PBC}$ | 15 | 17 | 18 | 20 | 21 | 23 | 24 | 26 | 27 | 29 | 30 | 32 | 33 | 35 | 36 |
| **q = 16** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **h**  |  |  | 3 |  |  |  | 4 |  |  |  | 5 |  |  |  | 6 |
| $m_{qTreePIR}$ |  |  | 3 |  |  |  | 4 |  |  |  | 5 |  |  |  | 6 |
| $m_{PBC}$ |  |  | 5 |  |  |  | 6 |  |  |  | 8 |  |  |  | 9 |
| **q = 128** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **h**  |  |  |  |  |  | 2 |  |  |  |  |  | 3 |  |  |  |
| $m_{qTreePIR}$ |  |  |  |  |  | 2 |  |  |  |  |  | 3 |  |  |  |
| $m_{PBC}$ |  |  |  |  |  | 3 |  |  |  |  |  | 5 |  |  |  |
| **q = 256** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **h**  |  |  |  |  |  |  |  | 2 |  |  |  |  |  | 3 |  |
| $m_{qTreePIR}$ |  |  |  |  |  |  |  | 2 |  |  |  |  |  | 3 |  |
| $m_{PBC}$ |  |  |  |  |  |  |  | 3 |  |  |  |  |  | 5 |  |

---
## Installing Libraries

- ##### Javac
      $ sudo apt update
      $ sudo apt upgrade
      $ sudo apt install default-jdk

- ##### SEAL 4.0.0
      $ sudo apt install build-essential cmake clang git g++ libssl-dev libgmp3-dev
      $ sudo apt update
      $ sudo apt upgrade
      $ git clone https://github.com/cnquang/SEAL-4.0.0.git
      $ cd SEAL-4.0.0
      $ cmake -S . -B build
      $ cmake --build build
      $ sudo cmake --install build

- ##### JSON
      $ sudo apt-get install curl zip unzip tar
      $ sudo apt-get install pkg-config
      $ git clone https://github.com/microsoft/vcpkg
      $ ./vcpkg/bootstrap-vcpkg.sh
      $ cd vcpkg
      $ ./vcpkg install rapidjson

- ##### Google gRPC
      $ sudo apt install -y build-essential autoconf libtool pkg-config
      $ git clone --recurse-submodules -b v1.58.0 --depth 1 --shallow-submodules https://github.com/grpc/grpc
      $ cd grpc
      $ mkdir -p cmake/build
      $ pushd cmake/build
      $ cmake -DgRPC_INSTALL=ON \
        -DgRPC_BUILD_TESTS=OFF \
        ../..
      $ make -j 4
      $ sudo make install
      $ popd
  
- ##### Boost.Asio
      $ sudo apt-get install libboost-all-dev

- ##### scp
      $ sudo apt install python3-pip
      $ pip install scp
      $ pip3 install scp
  
---
## Network Settings
      
- ### On AWS
  Create EC2 instances on AWS, the number of instances based on the tree's height (See Table 5 and Table 6).
  Ensure all the instances have TCP allow ports in the 0 to 65535 range. Connect all instances via SSH (See Figure below - Edit inbound rules).

<p align="center">
  <img width="600" height="300" src="https://github.com/cnquang/cnquang/assets/87842051/b1df7d72-a07a-44d2-812b-0d9fb7770efb">
</p>

- ### On the local machine
  Open the **Orchestrator folder** and add the list of Public IPv4 addresses of each instance in each line of the *list_servers_IPs.txt*.
  
  #### Open the terminal
      $ cd Orchestrator
      $ python3 orchestrator.py <parameter1: (h)> <parameter2: (q)>
      $ Example: python3 orchestrator.py 4 4
  All the local machine and instances' logs will be stored in the Logs folder.

  #### Plotting
      $ cd Logs/figures
      $ python3 figures.py
  All the figures will be created the same as in the report.
  
---
## ACKNOWLEDGMENTS 
This work was supported by the Australian Research Council through the Discovery Project under Grant DP200100731. Additionally, it was supported through Academic Grants Round 2022 by the Ethereum Foundation and received support from the RACE Merit Allocation Scheme (RMAS) in 2024 via the RMIT AWS Cloud Supercomputing Hub in Melbourne, Victoria, Australia, with the grant number RMAS00012.

---
## REFERENCES

[[SealPIR+PBC](https://doi.ieeecomputersociety.org/10.1109/SP.2018.00062)] Angel, S., Chen, H., Laine, K., & Setty, S. (2018, May). PIR with compressed queries and amortized query processing. In 2018 IEEE symposium on security and privacy (SP) (pp. 962-979). [GitHub](https://github.com/microsoft/SealPIR).

[[VBPIR](https://doi.ieeecomputersociety.org/10.1109/SP46215.2023.10179329)] Mughees, M. H., & Ren, L. (2023, May). Vectorized batch private information retrieval. In 2023 IEEE Symposium on Security and Privacy (SP) (pp. 437-452). [GitHub](https://github.com/mhmughees/vectorized_batchpir).
