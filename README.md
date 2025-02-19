<p align="center">
  <img width="250" height="230" src="https://github.com/PIR-PIXR/Certificate-Transparency-Logs/assets/102839948/530caacf-868e-464c-995b-04e995bc02bc">
</p>

# *q*TreePIR: Efficient Private Retrieval for Verkle Proofs via Ancestral $q$-ary Tree Coloring

## Abstract
The paper introduces innovative privacy mechanisms for enabling light clients to securely retrieve inclusion proof along arbitrary root-to-leaf path in $q$-ary trees, such as Verkle trees. $q$TreePIR, which develops from TreePIR, outperforms the state-of-the-art Probabilistic Batch Codes (PBC) ([Angel et al. IEEE S&P'18](https://doi.ieeecomputersociety.org/10.1109/SP.2018.00062)) in all metrics, achieving $3\times$ lower total storage and $1.5\times$ less communication cost and $1.5-2\times$ faster max/total server computation time and client query generation time. $q$TreePIR achieves a complexity of $\mathcal{O}(nh(\log_2 q + \log_2 h))$ in partition the tree in $h$ balance sub-databases. It can efficiently generate balanced sub-databases for a perfect 256-ary tree containing $2^{32}$ leaves in under 30 seconds. Additionally, the $q$TreePIR-Indexing algorithm allocates an arbitrary node's position in the path within its sub-database. With a complexity of $\mathcal{O}(qh^2)$ for this algorithm, it showcases impressive speed by indexing inclusion proof nodes for the ideal 256-ary tree of $2^{32}$ leaves in approximately two milliseconds. Most notably, *q*TreePIR's *polylog*-complexity indexing algorithm is $500\times$ faster than PBC for 256-ary tree of $2^{24}$ leaves.

---
## Experimental setup
Our experiments ran within Ubuntu 22.04 LTS environments. Our local machine (Intel® Core™ i5-1035G1 CPU @ 1.00GHz×8, 15GB System memory) served as the infrastructure for running the PIR Client, Orchestrator, ATC, *q*TreePIR-Indexing, and PBC (refer to Figure 1). For PIR Servers, we ran our experiments using up to 36 PIR servers on the Amazon m5.8xlarge instance (Intel® Xeon® Platinum 8175M CPU @ 2.50GHz, 32 vCPUs, 128GB System memory) that cost around $\$1.92$ per hour, using only one core. In Table 1}, we used until $36$ instances because, with $h = 24$, PBC generates $\lceil 1.5 \times h \rceil = 36$ databases, each of server processed a PIR database in parallel while our $q$TreePIR employed only $24$ servers. We choose an arbitrary C-PIR such as SealPIR \cite{angel2018} for our baseline implementations. In our experiments, the Verkle tree nodes are 32 bytes in size. Each experiment was repeated ten times for each tree's size in the Table \ref{table:expTrees}, changing the number of leaves ($n$) from $2^{10}$ to $2^{24}$ and the number of children ($q$) in the set $\{2, 16, 128, 256\}$. The average values were then calculated. We also utilize the HTTP/2 protocol in conjunction with gRPC version 35.0.0 \cite{gRPC}, developed by Google, to connect client and servers in the parallel PIR phase.


<p align="center">
  <img width="600" height="350" src="https://github.com/user-attachments/assets/f56fb51e-0672-44ee-a574-f2cd6f764828">
</p>

**Figure 1:** Process Architecture.


**Table 1**: Experimental Evaluation

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
### Dataset
Download the dataset from [Google Drive](https://drive.google.com/file/d/1VzdnIZK5nXA-kihbjMM_KNTrlwgzWJYs/view?usp=sharing) and overwrite the downloaded file to CSA/xenon2024/xenon2024_log_entries. The new file has a size of around 2GB.

You can also download Certificate Transparency logs from our [Github](https://github.com/PIR-PIXR/Certificate-Transparency-Logs).

---
### Installing Libraries

- #### Javac
      $ sudo apt update
      $ sudo apt upgrade
      $ sudo apt install default-jdk
- #### Python3
      $ sudo apt update
      $ sudo apt upgrade
      $ sudo apt install python3 
- #### SEAL 4.0.0
      $ sudo apt install build-essential cmake clang git g++ libssl-dev libgmp3-dev
      $ sudo apt update
      $ sudo apt upgrade
      $ git clone https://github.com/cnquang/SEAL-4.0.0.git
      $ cd SEAL-4.0.0
      $ cmake -S . -B build
      $ cmake --build build
      $ sudo cmake --install build
- #### JSON
      $ git clone https://github.com/microsoft/vcpkg
      $ ./vcpkg/bootstrap-vcpkg.sh
      $ ./vcpkg install rapidjson
- #### Google gRPC
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

---
### Executing SealPIR+PBC and SealPIR+TreePIR
      $ git clone https://github.com/newPIR/TreePIR.git
      $ cd TreePIR/SealPIR-Orchestrator
      $ python3 orchestrator.py <tree height> /Path/To/TreePIR
For example, with tree height $h = 10$, 
      python3 orchestrator.py 10 /Path/To/TreePIR.

---
### Executing Spiral+PBC and Spiral+TreePIR

- ##### Docker
      $ cd TreePIR/Spiral
      $ sudo docker build -t spiral_toolchain .
      $ sudo apt-get install libstdc++-11-dev
      $ sudo docker run -it \
        -u root \
        -v /Path/To/TreePIR/Spiral:/tmp/Spiral \
        -v /Path/To/TreePIR/Spiral/Process_Workspace:/home/ubuntu/Process_Workspace \
        --rm spiral_toolchain:latest \
        /bin/bash -c "cd /tmp/Spiral; exec bash"
      $ cd Evaluation
      $ python3 evaluate.py

To execute Spiral+PBC, open the evaluation.py and active line 23: "mode: typing.Final[Mode] = Mode.PBC". In the file TreePIR/Spiral/Seperate/src/spiral.cpp, active line 1140.

To execute Spiral+TreePIR, open the evaluation.py and active line 22: "mode: typing.Final[Mode] = Mode.COLOURING". In the file TreePIR/Spiral/Seperate/src/spiral.cpp, active line 1139.

---
### Executing VBPIR+PBC
      $ cd TreePIR/VBPIR_PBC
      $ cmake -S . -B build
      $ cmake --build build
      $ ./build/bin/vbpir_pbc
      
---
### Executing VBPIR+TreePIR
      $ cd TreePIR/VBPIR_TreePIR
      $ cmake -S . -B build
      $ cmake --build build
      $ ./build/bin/vbpir_treepir

---
## Performance
The performance of a batch-code-based batch-PIR depends on the number of sub-databases and their sizes, and on the performance of the underlying PIR scheme. Moreover, it also depends on the dimension $d$ that PIR sub-databases are represented, e.g., $d=1$ for PIRANA, $d=2$ for SealPIR, $d=2, 3$ for VBPIR, and $d=4$ for Spiral. Theoretically, as TreePIR uses $1.5\times$ fewer sub-databases of size $2\times$ smaller compared to PBC, theoretically, TreePIR uses $3\times$ less storage, with $\sqrt[d]{2}\times$ faster max server computation, $1.5\sqrt[d]{2}\times$ faster total server computation, and $1.5 \times$ faster client query-generation time (except for VBPIR and PIRANA, the speedup for client query-generation time is $\sqrt[d]{2}\times$ and $\sqrt[k]{3}\times$, respectively). The client answer-extraction times are similar for both as dummy responses are ignored in PBC. These theoretical gains were also reflected in the experiments.

TreePIR has significantly faster setup and indexing thanks to its efficient coloring and indexing algorithms on trees. In particular, for trees with $2^{10} - 2^{24}$ leaves, TreePIR's setup and indexing are $8$-$60\times$ and $19 - 160\times$ faster than PBC's, respectively. TreePIR still works well beyond that range, requiring $180$ seconds to setup a tree of $2^{30}$ leaves, and only $0.7$ milliseconds to index in a tree of $2^{36}$ leaves.

**Table 1:** A comparison of the *setup* time between TreePIR and PBC for various tree heights. TreePIR's setup is $8 - 60\times$ faster for trees of $2^{10} - 2^{24}$ leaves.

| $h$ | 10 | 12 | 14 | 16 | 18 | 20 | 22 | 24 |
|-----|----|----|----|----|----|----|----|----|
| PBC (ms) | 3.4 | 8.9 | 53.1 | 406 | 2132 | 9259 | 37591 | 159814 |
| **TreePIR** (ms) | 0.4 | 2.4 | 7.6 | 39.1 | 56.1 | 179 | 600 | 2700 |
| $h$ | 26 |    |    | 28 |    | 29 |    | 30 |
| **TreePIR** (sec) | 9.6 |    |    | 37.3 |    | 77.1 |    | 179.4 |

**Table 2:** A comparison of the *indexing* times of TreePIR and PBC. Despite ignoring the download time of its (large) index, PBC's indexing is still 19 - $160\times$ slower than TreePIR's indexing.

| $h$ | 10 | 12 | 14 | 16 | 18 | 20 | 22 | 24 |
|-----|----|----|----|----|----|----|----|----|
| Indexing PBC (ms) | 4 | 4 | 4 | 4 | 5 | 11 | 22 | 74 |
| **TreePIR** (ms) | 0.21 | 0.24 | 0.25 | 0.32 | 0.34 | 0.38 | 0.41 | 0.46 |
| $h$ | 26 | 28 |  | 30 | 32 | | 34 | 36 |
| **TreePIR** (ms) | 0.47 | 0.48 |  | 0.51 | 0.52 | | 0.61 | 0.69 |

**Table 3:** The client *query-generation* times of TreePIR and PBC when combined with SealPIR, Spiral, VBPIR, and PIRANA.

| $h$ | 10 | 12 | 14 | 16 | 18 | 20 |
|-----|----|----|----|----|----|----|
| SealPIR+PBC (ms) | 21 | 24 | 28 | 31 | 37 | 40 |
| **SealPIR+TreePIR** (ms) | 13 | 16 | 18 | 21 | 24 | 27 |
| Spiral+PBC (ms) | 33 | 39 | 46 | 54 | 62 | 66 |
| **Spiral+TreePIR** (ms) | 20 | 24 | 29 | 33 | 37 | 41 |
| VBPIR+PBC (ms) | 5.1 | 5.1 | 7.0 | 7.0 | 7.3 | 7.5 |
| **VBPIR+TreePIR** (ms) | 4.1 | 4.1 | 4.3 | 6.2 | 6.4 | 6.6 |
| PIRANA+PBC (ms) | 4.1 | 5.6 | 8.6 | 14 | 24 | 45 |
| **PIRANA+TreePIR** (ms) | 3.3 | 3.9 | 5.6 | 8 | 15 | 28 |

**Table 4:** The client *answer-extraction* times of TreePIR and PBC when combined with SealPIR, Spiral, VBPIR, and PIRANA are similar.

| $h$ | 10  | 12  | 14  | 16  | 18  | 20  |
|-----|-----|-----|-----|-----|-----|-----|
| SealPIR+PBC (ms) | 12.4 | 14.9 | 17.3 | 19.4 | 22.4 | 24.6 |
| **SealPIR+TreePIR** (ms) | 12.6 | 15.0 | 17.2 | 19.4 | 22.2 | 24.3 |
| Spiral+PBC (ms) | 6.7 | 7.9 | 9.4 | 10.4 | 10.9 | 12.2 |
| **Spiral+TreePIR** (ms) | 5.8 | 7.2 | 8.4 | 9.6 | 10.5 | 12.2 |
| VBPIR+PBC (ms) | 1.3 | 1.3 | 0.7 | 0.7 | 0.7 | 0.7 |
| **VBPIR+TreePIR** (ms) | 1.3 | 1.3 | 1.3 | 0.7 | 0.7 | 0.7 |
| PIRANA+PBC (ms) | 6.1 | 6.1 | 6.1 | 6.1 | 6.1 | 6.1 |
| **PIRANA+TreePIR** (ms) | 6.1 | 6.1 | 6.1 | 6.1 | 6.1 | 6.1 |

**Table 5:** Theoretically, TreePIR's max server computation time is $\sqrt[d]{2} \times$ faster than PBC. This is reflected correctly in the table with $d = 2$ for SealPIR and $d=4$ for Spiral.

| $h$ | 10 | 12 | 14 | 16 | 18 | 20 |
|-----|----|----|----|----|----|----|
| SealPIR+PBC (ms) | 6.0 | 6.2 | 12.4 | 21.3 | 60 | 107 |
| **SealPIR+TreePIR** (ms) | 5.8 | 5.8 | 9.1 | 18.9 | 36 | 76 |
| Spriral+PBC (ms) | 33 | 34 | 34 | 34 | 35 | 39 |
| **Spiral+TreePIR** (ms) | 30 | 31 | 31 | 31 | 32 | 33 |

**Table 6:** TreePIR's total server computation time is $1.5$ - $3\times$ faster than PBC for larger trees. Theoretically, it is $1.5 \sqrt[d]{2} \times$ faster.

| $h$ | 10 | 12 | 14 | 16 | 18 | 20 |
|-----|----|----|----|----|----|----|
| SealPIR+PBC (ms) | 69 | 99 | 235 | 486 | 1185 | 2916 |
| **SealPIR+TreePIR** (ms) | 47 | 55 | 104 | 233 | 531 | 1250 |
| Spiral+PBC (ms) | 501 | 613 | 700 | 805 | 916 | 1151 |
| **Spiral+TreePIR** (ms) | 309 | 373 | 429 | 507 | 561 | 663 |
| VBPIR+PBC (ms) | 399 | 405 | 586 | 969 | 2357 | 7481 |
| **VBPIR+TreePIR** (ms) | 396 | 397 | 415 | 588 | 1372 | 3871 |
| PIRANA+PBC (ms) | 46 | 76 | 189 | 570 | 1851 | 6796 |
| **PIRANA+TreePIR** (ms) | 26 | 42 | 91 | 218 | 696 | 2377 |


<p align="center">
  <img width="600" height="350" src="https://github.com/user-attachments/assets/9dec3668-cba6-4cb2-a22b-ed057541f34f">
</p>

**Figure 1:** TreePIR's communication cost is about $1.5\times$ lower than PBC's as expected for most combinations (except VBPIR).

---
## ACKNOWLEDGMENTS 
This work was supported by the Australian Research Council through the Discovery Project under Grant DP200100731.

---
## REFERENCES

[[SealPIR+PBC](https://doi.ieeecomputersociety.org/10.1109/SP.2018.00062)] Angel, S., Chen, H., Laine, K., & Setty, S. (2018, May). PIR with compressed queries and amortized query processing. In 2018 IEEE symposium on security and privacy (SP) (pp. 962-979). [GitHub](https://github.com/microsoft/SealPIR).

[[Spiral](https://doi.ieeecomputersociety.org/10.1109/SP46214.2022.9833700)] Menon, S. J., & Wu, D. J. (2022, May). Spiral: Fast, high-rate single-server PIR via FHE composition. In 2022 IEEE Symposium on Security and Privacy (SP) (pp. 930-947). [GitHub](https://github.com/menonsamir/spiral).

[[VBPIR](https://doi.ieeecomputersociety.org/10.1109/SP46215.2023.10179329)] Mughees, M. H., & Ren, L. (2023, May). Vectorized batch private information retrieval. In 2023 IEEE Symposium on Security and Privacy (SP) (pp. 437-452). [GitHub](https://github.com/mhmughees/vectorized_batchpir).

[[PIRANA](https://doi.ieeecomputersociety.org/10.1109/SP54263.2024.00039)] J. Liu, J. Li, D. Wu and K. Ren, (2024), PIRANA: Faster Multi-query PIR via Constant-weight Codes, in 2024 IEEE Symposium on Security and Privacy (SP), (pp. 43-43). [GitHub](https://github.com/zju-abclab/PIRANA).
