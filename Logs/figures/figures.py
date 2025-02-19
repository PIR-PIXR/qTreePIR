import os
import math
import matplotlib.pyplot as plt
from collections import defaultdict
from matplotlib.ticker import MaxNLocator

def calculate_expression(q, h):
    numerator = q * (q ** h - 1)
    denominator = (q - 1) * h
    result = numerator / denominator
    return result

# Given range for h with q = 2
h2 = range(10, 25)
color_size_2 = [math.ceil(calculate_expression(2, h)) for h in h2]

# Given range for h with q = 16
h16 = range(3, 7)
color_size_16 = [math.ceil(calculate_expression(16, h)) for h in h16]

# Given range for h with q = 128
h128 = range(2, 4)
color_size_128 = [math.ceil(calculate_expression(128, h)) for h in h128]

# Given range for h with q = 256
h256 = range(2, 4)
color_size_256 = [math.ceil(calculate_expression(256, h)) for h in h256]

pbc_size_2 = []
pbc_size_16 = []
pbc_size_128 = []
pbc_size_256 = []

directory = "/Users/quangnhat/Desktop/Logs_CTA"
for h in h2:
    filename = f"max_bucket_{h}_{2}.txt"
    filepath = os.path.join(directory, filename)

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            number = int(file.read().strip())
            pbc_size_2.append(number)
    else:
        print(f"File {filename} not found.")

for h in h16:
    filename = f"max_bucket_{h}_{16}.txt"
    filepath = os.path.join(directory, filename)

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            number = int(file.read().strip())
            pbc_size_16.append(number)
    else:
        print(f"File {filename} not found.")
for h in h128:
    filename = f"max_bucket_{h}_{128}.txt"
    filepath = os.path.join(directory, filename)

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            number = int(file.read().strip())
            pbc_size_128.append(number)
    else:
        print(f"File {filename} not found.")

for h in h256:
    filename = f"max_bucket_{h}_{256}.txt"
    filepath = os.path.join(directory, filename)

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            number = int(file.read().strip())
            pbc_size_256.append(number)
    else:
        print(f"File {filename} not found.")

# Plotting in subplots
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
#fig.suptitle("Comparative Analysis: Element Count in Color Database versus PBC Database", fontsize = 16)

axs[0, 0].plot(h2, color_size_2, label="Color Size (q=2)")
axs[0, 0].plot(h2, pbc_size_2, label="PBC Size (q=2)", linestyle='dashed')
# axs[0, 0].set_title("q=2")
axs[0, 0].set_xlabel('h', fontsize=14, weight='bold')
axs[0, 0].set_ylabel('MB', fontsize=14, weight='bold')
axs[0, 0].tick_params(axis='x', labelsize=14)
axs[0, 0].tick_params(axis='y', labelsize=14)
axs[0, 0].legend(fontsize=16)
axs[0, 0].set_yscale('log')
axs[0, 0].xaxis.set_major_locator(MaxNLocator(integer=True))

axs[0, 1].plot(h16, color_size_16, label="Color Size (q=16)")
axs[0, 1].plot(h16, pbc_size_16, label="PBC Size (q=16)", linestyle='dashed')
#axs[0, 1].set_title("q=16")
axs[0, 1].set_xlabel('h', fontsize=14, weight='bold')
axs[0, 1].set_ylabel('MB', fontsize=14, weight='bold')
axs[0, 1].tick_params(axis='x', labelsize=14)
axs[0, 1].tick_params(axis='y', labelsize=14)
axs[0, 1].legend(fontsize=16)
axs[0, 1].set_yscale('log')
axs[0, 1].xaxis.set_major_locator(MaxNLocator(integer=True))

axs[1, 0].plot(h128, color_size_128, label="Color Size (q=128)")
axs[1, 0].plot(h128, pbc_size_128, label="PBC Size (q=128)", linestyle='dashed')
#axs[1, 0].set_title("q=128")
axs[1, 0].set_xlabel('h', fontsize=14, weight='bold')
axs[1, 0].set_ylabel('MB', fontsize=14, weight='bold')
axs[1, 0].tick_params(axis='x', labelsize=14)
axs[1, 0].tick_params(axis='y', labelsize=14)
axs[1, 0].legend(fontsize=16)
axs[1, 0].set_yscale('log')
axs[1, 0].xaxis.set_major_locator(MaxNLocator(integer=True))

axs[1, 1].plot(h256, color_size_256, label="Color Size (q=256)")
axs[1, 1].plot(h256, pbc_size_256, label="PBC Size (q=256)", linestyle='dashed')
#axs[1, 1].set_title("q=256")
axs[1, 1].set_xlabel('h', fontsize=14, weight='bold')
axs[1, 1].set_ylabel('MB', fontsize=14, weight='bold')
axs[1, 1].tick_params(axis='x', labelsize=14)
axs[1, 1].tick_params(axis='y', labelsize=14)
axs[1, 1].legend(fontsize=16)
axs[1, 1].set_yscale('log')
axs[1, 1].xaxis.set_major_locator(MaxNLocator(integer=True))

for ax in axs.flat:
    ax.set(xlabel='h', ylabel='#')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("/Users/quangnhat/Desktop/Logs_CTA/figures/dbsize.pdf")

# Calculate the ratio between pbc_size and color_size for each q value
ratio_2 = [p / c for p, c in zip(pbc_size_2, color_size_2)]
ratio_16 = [p / c for p, c in zip(pbc_size_16, color_size_16)]
ratio_128 = [p / c for p, c in zip(pbc_size_128, color_size_128)]
ratio_256 = [p / c for p, c in zip(pbc_size_256, color_size_256)]

# Print the ratios
'''print("Ratio for q=2:", ratio_2)
print("Ratio for q=16:", ratio_16)
print("Ratio for q=128:", ratio_128)
print("Ratio for q=256:", ratio_256)'''

#################################### PBC LOGS (PBC_h_q_log.txt) #################################################
map_size_2 = []
map_size_16 = []
map_size_128 = []
map_size_256 = []

pbc_time_2 = []
pbc_time_16 = []
pbc_time_128 = []
pbc_time_256 = []

for h in h2:
    filename = f"PBC_{h}_{2}_log.txt"
    filepath = os.path.join(directory, filename)

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            content = file.read()

            # Split the content into lines
            lines = content.split('\n')

            # Process each line and extract relevant information
            for line in lines:
                if line.startswith("Map_Size"):
                    map_size = int(line.split(":")[1].split()[0])
                    map_size_2.append(map_size/1000000)
                elif line.startswith("Cuckoo_hash"):
                    time = int(line.split(":")[1].split()[0])
                    pbc_time_2.append(time/1000)
    else:
        print(f"File {filename} not found.")

for h in h16:
    filename = f"PBC_{h}_{16}_log.txt"
    filepath = os.path.join(directory, filename)

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            content = file.read()

            # Split the content into lines
            lines = content.split('\n')

            # Process each line and extract relevant information
            for line in lines:
                if line.startswith("Map_Size"):
                    map_size = int(line.split(":")[1].split()[0])
                    map_size_16.append(map_size/1000000)
                elif line.startswith("Cuckoo_hash"):
                    time = int(line.split(":")[1].split()[0])
                    pbc_time_16.append(time/1000)
    else:
        print(f"File {filename} not found.")

for h in h128:
    filename = f"PBC_{h}_{128}_log.txt"
    filepath = os.path.join(directory, filename)

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            content = file.read()

            # Split the content into lines
            lines = content.split('\n')

            # Process each line and extract relevant information
            for line in lines:
                if line.startswith("Map_Size"):
                    map_size = int(line.split(":")[1].split()[0])
                    map_size_128.append(map_size/1000000)
                elif line.startswith("Cuckoo_hash"):
                    time = int(line.split(":")[1].split()[0])
                    pbc_time_128.append(time/1000)
    else:
        print(f"File {filename} not found.")

for h in h256:
    filename = f"PBC_{h}_{256}_log.txt"
    filepath = os.path.join(directory, filename)

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            content = file.read()

            # Split the content into lines
            lines = content.split('\n')

            # Process each line and extract relevant information
            for line in lines:
                if line.startswith("Map_Size"):
                    map_size = int(line.split(":")[1].split()[0])
                    map_size_256.append(map_size/1000000)
                elif line.startswith("Cuckoo_hash"):
                    time = int(line.split(":")[1].split()[0])
                    pbc_time_256.append(time/1000)
    else:
        print(f"File {filename} not found.")

# Plotting
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Plot for h2
axes[0, 0].plot(h2, map_size_2, linestyle='--', color='#FF8C00')
axes[0, 0].set_xlabel('h')
axes[0, 0].set_ylabel('MB')
axes[0, 0].set_title('Map Size for q = 2')
axes[0, 0].xaxis.set_major_locator(MaxNLocator(integer=True))

# Plot for h16
axes[0, 1].plot(h16, map_size_16, linestyle='--', color='#FF8C00')
axes[0, 1].set_xlabel('h')
axes[0, 1].set_ylabel('MB')
axes[0, 1].set_title('Map Size for q = 16')
axes[0, 1].xaxis.set_major_locator(MaxNLocator(integer=True))

# Plot for h128
axes[1, 0].plot(h128, map_size_128, linestyle='--', color='#FF8C00')
axes[1, 0].set_xlabel('h')
axes[1, 0].set_ylabel('MB')
axes[1, 0].set_title('Map Size for q = 128')
axes[1, 0].xaxis.set_major_locator(MaxNLocator(integer=True))

# Plot for h256
axes[1, 1].plot(h256, map_size_256, linestyle='--', color='#FF8C00')
axes[1, 1].set_xlabel('h')
axes[1, 1].set_ylabel('GB')
axes[1, 1].set_title('Map Size for q = 256')
axes[1, 1].xaxis.set_major_locator(MaxNLocator(integer=True))

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("/Users/quangnhat/Desktop/Logs_CTA/figures/mapsize.pdf")

print("Map Size:")
print(map_size_2)
print(map_size_16)
print(map_size_128)
print(map_size_256)

#################################### pbc_indexing_h_q_log.txt #################################################
pbc_indexing_time_2 = []
pbc_indexing_time_16 = []
pbc_indexing_time_128 = []
pbc_indexing_time_256 = []

for h in h2:
    filename = f"pbc_indexing_{h}_{2}_log.txt"
    filepath = os.path.join(directory, filename)

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            content = file.read()

            # Split the content into lines
            lines = content.split('\n')

            # Process each line and extract relevant information
            for line in lines:
                if line.startswith("Average_Indexing_time"):
                    time = int(line.split(":")[1].split()[0])
                    pbc_indexing_time_2.append(time)
    else:
        print(f"File {filename} not found.")

for h in h16:
    filename = f"pbc_indexing_{h}_{16}_log.txt"
    filepath = os.path.join(directory, filename)

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            content = file.read()

            # Split the content into lines
            lines = content.split('\n')

            # Process each line and extract relevant information
            for line in lines:
                if line.startswith("Average_Indexing_time"):
                    time = int(line.split(":")[1].split()[0])
                    pbc_indexing_time_16.append(time)
    else:
        print(f"File {filename} not found.")

for h in h128:
    filename = f"pbc_indexing_{h}_{128}_log.txt"
    filepath = os.path.join(directory, filename)

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            content = file.read()

            # Split the content into lines
            lines = content.split('\n')

            # Process each line and extract relevant information
            for line in lines:
                if line.startswith("Average_Indexing_time"):
                    time = int(line.split(":")[1].split()[0])
                    pbc_indexing_time_128.append(time)
    else:
        print(f"File {filename} not found.")

for h in h256:
    filename = f"pbc_indexing_{h}_{256}_log.txt"
    filepath = os.path.join(directory, filename)

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            content = file.read()

            # Split the content into lines
            lines = content.split('\n')

            # Process each line and extract relevant information
            for line in lines:
                if line.startswith("Average_Indexing_time"):
                    time = int(line.split(":")[1].split()[0])
                    pbc_indexing_time_256.append(time)
    else:
        print(f"File {filename} not found.")

#################################### CTA_h_q_log.txt #################################################
cta_time_2 = []
cta_time_16 = []
cta_time_128 = []
cta_time_256 = []

for h in h2:
    filename = f"CTA_{h}_{2}_log.txt"
    filepath = os.path.join(directory, filename)

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            content = file.readlines()

        # Extract and calculate average CTA time
        cta_time = [int(line.split(":")[1].split()[0]) for line in content if "CTA:" in line]
        cta_average_time = sum(cta_time) / len(cta_time)
        cta_time_2.append(cta_average_time)

    else:
        print(f"File {filename} not found.")

for h in h16:
    filename = f"CTA_{h}_{16}_log.txt"
    filepath = os.path.join(directory, filename)

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            content = file.readlines()

        # Extract and calculate average CTA time
        cta_time = [int(line.split(":")[1].split()[0]) for line in content if "CTA:" in line]
        cta_average_time = sum(cta_time) / len(cta_time)
        cta_time_16.append(cta_average_time)

    else:
        print(f"File {filename} not found.")

for h in h128:
    filename = f"CTA_{h}_{128}_log.txt"
    filepath = os.path.join(directory, filename)

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            content = file.readlines()

        # Extract and calculate average CTA time
        cta_time = [int(line.split(":")[1].split()[0]) for line in content if "CTA:" in line]
        cta_average_time = sum(cta_time) / len(cta_time)
        cta_time_128.append(cta_average_time)

    else:
        print(f"File {filename} not found.")

for h in h256:
    filename = f"CTA_{h}_{256}_log.txt"
    filepath = os.path.join(directory, filename)

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            content = file.readlines()

        # Extract and calculate average CTA time
        cta_time = [int(line.split(":")[1].split()[0]) for line in content if "CTA:" in line]
        cta_average_time = sum(cta_time) / len(cta_time)
        cta_time_256.append(cta_average_time)

    else:
        print(f"File {filename} not found.")

# Plotting in subplots
fig, axs = plt.subplots(2, 2, figsize=(12, 8))

axs[0, 0].plot(h2, cta_time_2, label="CTA (q=2)")
axs[0, 0].plot(h2, pbc_time_2, label="PBC (q=2)", linestyle='dashed')
axs[0, 0].set_xlabel('h', fontsize=14, weight='bold')
axs[0, 0].set_ylabel('MB', fontsize=14, weight='bold')
axs[0, 0].tick_params(axis='x', labelsize=14)
axs[0, 0].tick_params(axis='y', labelsize=14)
axs[0, 0].legend(fontsize=16)
axs[0, 0].set_yscale('log')
axs[0, 0].xaxis.set_major_locator(MaxNLocator(integer=True))

axs[0, 1].plot(h16, cta_time_16, label="CTA (q=16)")
axs[0, 1].plot(h16, pbc_time_16, label="PBC (q=16)", linestyle='dashed')
axs[0, 1].set_xlabel('h', fontsize=14, weight='bold')
axs[0, 1].set_ylabel('MB', fontsize=14, weight='bold')
axs[0, 1].tick_params(axis='x', labelsize=14)
axs[0, 1].tick_params(axis='y', labelsize=14)
axs[0, 1].legend(fontsize=16)
axs[0, 1].set_yscale('log')
axs[0, 1].xaxis.set_major_locator(MaxNLocator(integer=True))

axs[1, 0].plot(h128, cta_time_128, label="CTA (q=128)")
axs[1, 0].plot(h128, pbc_time_128, label="PBC (q=128)", linestyle='dashed')
axs[1, 0].set_xlabel('h', fontsize=14, weight='bold')
axs[1, 0].set_ylabel('MB', fontsize=14, weight='bold')
axs[1, 0].tick_params(axis='x', labelsize=14)
axs[1, 0].tick_params(axis='y', labelsize=14)
axs[1, 0].legend(fontsize=16)
axs[1, 0].set_yscale('log')
axs[1, 0].xaxis.set_major_locator(MaxNLocator(integer=True))

axs[1, 1].plot(h256, cta_time_256, label="CTA (q=256)")
axs[1, 1].plot(h256, pbc_time_256, label="PBC (q=256)", linestyle='dashed')
axs[1, 1].set_xlabel('h', fontsize=14, weight='bold')
axs[1, 1].set_ylabel('MB', fontsize=14, weight='bold')
axs[1, 1].tick_params(axis='x', labelsize=14)
axs[1, 1].tick_params(axis='y', labelsize=14)
axs[1, 1].legend(fontsize=16)
axs[1, 1].set_yscale('log')
axs[1, 1].xaxis.set_major_locator(MaxNLocator(integer=True))

for ax in axs.flat:
    ax.set(xlabel='h', ylabel='ms')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("/Users/quangnhat/Desktop/Logs_CTA/figures/partitiontime.pdf")

print(pbc_time_2)
print(cta_time_2)
print(pbc_time_16)
print(cta_time_16)
print(pbc_time_128)
print(cta_time_128)
print(pbc_time_256)
print(cta_time_256)

#################################### CTAindexing_h_q_log.txt #################################################
cta_indexing_time_2 = []
cta_indexing_time_16 = []
cta_indexing_time_128 = []
cta_indexing_time_256 = []

for h in h2:
    filename = f"CTAindexing_{h}_{2}_log.txt"
    filepath = os.path.join(directory, filename)

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            content = file.readlines()

        # Extract and calculate average indexing time
        indexing_time = [int(line.split(":")[1].split()[0]) for line in content if "Indexing:" in line]
        indexing_average_time = sum(indexing_time) / len(indexing_time)
        cta_indexing_time_2.append(indexing_average_time/1000)

    else:
        print(f"File {filename} not found.")

for h in h16:
    filename = f"CTAindexing_{h}_{16}_log.txt"
    filepath = os.path.join(directory, filename)

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            content = file.readlines()

        # Extract and calculate average indexing time
        indexing_time = [int(line.split(":")[1].split()[0]) for line in content if "Indexing:" in line]
        indexing_average_time = sum(indexing_time) / len(indexing_time)
        cta_indexing_time_16.append(indexing_average_time/1000)

    else:
        print(f"File {filename} not found.")

for h in h128:
    filename = f"CTAindexing_{h}_{128}_log.txt"
    filepath = os.path.join(directory, filename)

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            content = file.readlines()

        # Extract and calculate average indexing time
        indexing_time = [int(line.split(":")[1].split()[0]) for line in content if "Indexing:" in line]
        indexing_average_time = sum(indexing_time) / len(indexing_time)
        cta_indexing_time_128.append(indexing_average_time/1000)

    else:
        print(f"File {filename} not found.")

for h in h256:
    filename = f"CTAindexing_{h}_{256}_log.txt"
    filepath = os.path.join(directory, filename)

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            content = file.readlines()

        # Extract and calculate average indexing time
        indexing_time = [int(line.split(":")[1].split()[0]) for line in content if "Indexing:" in line]
        indexing_average_time = sum(indexing_time) / len(indexing_time)
        cta_indexing_time_256.append(indexing_average_time/1000)

    else:
        print(f"File {filename} not found.")

# Plotting in subplots
fig, axs = plt.subplots(2, 2, figsize=(12, 8))

axs[0, 0].plot(h2, cta_indexing_time_2, label="CTA (q=2)")
axs[0, 0].plot(h2, pbc_indexing_time_2, label="PBC (q=2)", linestyle='dashed')
axs[0, 0].set_xlabel('h', fontsize=14, weight='bold')
axs[0, 0].set_ylabel('MB', fontsize=14, weight='bold')
axs[0, 0].tick_params(axis='x', labelsize=14)
axs[0, 0].tick_params(axis='y', labelsize=14)
axs[0, 0].legend(fontsize=16)
axs[0, 0].xaxis.set_major_locator(MaxNLocator(integer=True))

axs[0, 1].plot(h16, cta_indexing_time_16, label="CTA (q=16)")
axs[0, 1].plot(h16, pbc_indexing_time_16, label="PBC (q=16)", linestyle='dashed')
axs[0, 1].set_xlabel('h', fontsize=14, weight='bold')
axs[0, 1].set_ylabel('MB', fontsize=14, weight='bold')
axs[0, 1].tick_params(axis='x', labelsize=14)
axs[0, 1].tick_params(axis='y', labelsize=14)
axs[0, 1].legend(fontsize=16)
axs[0, 1].xaxis.set_major_locator(MaxNLocator(integer=True))

axs[1, 0].plot(h128, cta_indexing_time_128, label="CTA (q=128)")
axs[1, 0].plot(h128, pbc_indexing_time_128, label="PBC (q=128)", linestyle='dashed')
axs[1, 0].set_xlabel('h', fontsize=14, weight='bold')
axs[1, 0].set_ylabel('MB', fontsize=14, weight='bold')
axs[1, 0].tick_params(axis='x', labelsize=14)
axs[1, 0].tick_params(axis='y', labelsize=14)
axs[1, 0].legend(fontsize=16)
axs[1, 0].xaxis.set_major_locator(MaxNLocator(integer=True))

axs[1, 1].plot(h256, cta_indexing_time_256, label="CTA (q=256)")
axs[1, 1].plot(h256, pbc_indexing_time_256, label="PBC (q=256)", linestyle='dashed')
axs[1, 1].set_xlabel('h', fontsize=14, weight='bold')
axs[1, 1].set_ylabel('MB', fontsize=14, weight='bold')
axs[1, 1].tick_params(axis='x', labelsize=14)
axs[1, 1].tick_params(axis='y', labelsize=14)
axs[1, 1].legend(fontsize=16)
axs[1, 1].xaxis.set_major_locator(MaxNLocator(integer=True))

for ax in axs.flat:
    ax.set(xlabel='h', ylabel='ms')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("/Users/quangnhat/Desktop/Logs_CTA/figures/indexingtime.pdf")

'''print(cta_indexing_time_2)
print(pbc_indexing_time_2)
print(cta_indexing_time_16)
print(pbc_indexing_time_16)
print(cta_indexing_time_128)
print(pbc_indexing_time_128)
print(cta_indexing_time_256)
print(pbc_indexing_time_256)'''

#################################### PIR Server logs (color_h_q_log.txt/ pbc_h_q_log.txt) #################################################
color = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
         'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

server_color_reply_time_2 = []
server_color_reply_time_16 = []
server_color_reply_time_128 = []
server_color_reply_time_256 = []

server_color_reply_size_2 = []
server_color_reply_size_16 = []
server_color_reply_size_128 = []
server_color_reply_size_256 = []

for h in h2:
    average_reply_times = []
    average_reply_sizes = []
    for i in range(h):
        filename = f"color{color[i]}_{h}_{2}_log.txt"
        filepath = os.path.join(directory, filename)

        if os.path.exists(filepath):
            with open(filepath, "r") as file:
                content = file.read()

                reply_times = [int(line.split(":")[1].split()[0]) for line in content.split('\n') if
                               "reply_time:" in line]
                average_reply_time = sum(reply_times) / len(reply_times)
                average_reply_times.append(average_reply_time)

                reply_sizes = [int(line.split(":")[1].split()[0]) for line in content.split('\n') if
                               "reply_size:" in line]
                average_reply_size = sum(reply_sizes) / len(reply_sizes)
                average_reply_sizes.append(average_reply_size)
        else:
            print(f"File {filename} not found.")

    average_reply_time = sum(average_reply_times) / len(average_reply_times)
    server_color_reply_time_2.append(average_reply_time/1000)
    server_color_reply_size_2.append(sum(average_reply_sizes)/1000000)

for h in h16:
    average_reply_times = []
    average_reply_sizes = []
    for i in range(h):
        filename = f"color{color[i]}_{h}_{16}_log.txt"
        filepath = os.path.join(directory, filename)

        if os.path.exists(filepath):
            with open(filepath, "r") as file:
                content = file.read()

                reply_times = [int(line.split(":")[1].split()[0]) for line in content.split('\n') if
                               "reply_time:" in line]
                average_reply_time = sum(reply_times) / len(reply_times)
                average_reply_times.append(average_reply_time)

                reply_sizes = [int(line.split(":")[1].split()[0]) for line in content.split('\n') if
                               "reply_size:" in line]
                average_reply_size = sum(reply_sizes) / len(reply_sizes)
                average_reply_sizes.append(average_reply_size)
        else:
            print(f"File {filename} not found.")

    average_reply_time = sum(average_reply_times) / len(average_reply_times)
    server_color_reply_time_16.append(average_reply_time/1000)
    server_color_reply_size_16.append(sum(average_reply_sizes)/1000000)

for h in h128:
    average_reply_times = []
    average_reply_sizes = []
    for i in range(h):
        filename = f"color{color[i]}_{h}_{128}_log.txt"
        filepath = os.path.join(directory, filename)

        if os.path.exists(filepath):
            with open(filepath, "r") as file:
                content = file.read()

                reply_times = [int(line.split(":")[1].split()[0]) for line in content.split('\n') if
                               "reply_time:" in line]
                average_reply_time = sum(reply_times) / len(reply_times)
                average_reply_times.append(average_reply_time)

                reply_sizes = [int(line.split(":")[1].split()[0]) for line in content.split('\n') if
                               "reply_size:" in line]
                average_reply_size = sum(reply_sizes) / len(reply_sizes)
                average_reply_sizes.append(average_reply_size)
        else:
            print(f"File {filename} not found.")

    average_reply_time = sum(average_reply_times) / len(average_reply_times)
    server_color_reply_time_128.append(average_reply_time/1000)
    server_color_reply_size_128.append(sum(average_reply_sizes)/1000000)

for h in h256:
    average_reply_times = []
    average_reply_sizes = []
    for i in range(h):
        filename = f"color{color[i]}_{h}_{256}_log.txt"
        filepath = os.path.join(directory, filename)

        if os.path.exists(filepath):
            with open(filepath, "r") as file:
                content = file.read()

                reply_times = [int(line.split(":")[1].split()[0]) for line in content.split('\n') if
                               "reply_time:" in line]
                average_reply_time = sum(reply_times) / len(reply_times)
                average_reply_times.append(average_reply_time)

                reply_sizes = [int(line.split(":")[1].split()[0]) for line in content.split('\n') if
                               "reply_size:" in line]
                average_reply_size = sum(reply_sizes) / len(reply_sizes)
                average_reply_sizes.append(average_reply_size)
        else:
            print(f"File {filename} not found.")

    average_reply_time = sum(average_reply_times) / len(average_reply_times)
    server_color_reply_time_256.append(average_reply_time/1000)
    server_color_reply_size_256.append(sum(average_reply_sizes)/1000000)

server_pbc_reply_time_2 = []
server_pbc_reply_time_16 = []
server_pbc_reply_time_128 = []
server_pbc_reply_time_256 = []

server_pbc_reply_size_2 = []
server_pbc_reply_size_16 = []
server_pbc_reply_size_128 = []
server_pbc_reply_size_256 = []

for h in h2:
    average_reply_times = []
    average_reply_sizes = []
    for i in range(math.ceil(1.5 * h)):
        filename = f"pbc{i + 1}_{h}_{2}_log.txt"
        filepath = os.path.join(directory, filename)

        if os.path.exists(filepath):
            with open(filepath, "r") as file:
                content = file.read()

                reply_times = [int(line.split(":")[1].split()[0]) for line in content.split('\n') if
                               "reply_time:" in line]
                average_reply_time = sum(reply_times) / len(reply_times)
                average_reply_times.append(average_reply_time)

                reply_sizes = [int(line.split(":")[1].split()[0]) for line in content.split('\n') if
                               "reply_size:" in line]
                average_reply_size = sum(reply_sizes) / len(reply_sizes)
                average_reply_sizes.append(average_reply_size)
        else:
            print(f"File {filename} not found.")

    average_reply_time = sum(average_reply_times) / len(average_reply_times)
    server_pbc_reply_time_2.append(average_reply_time/1000)
    server_pbc_reply_size_2.append(sum(average_reply_sizes)/1000000)

for h in h16:
    average_reply_times = []
    average_reply_sizes = []
    for i in range(math.ceil(1.5 * h)):
        filename = f"pbc{i + 1}_{h}_{16}_log.txt"
        filepath = os.path.join(directory, filename)

        if os.path.exists(filepath):
            with open(filepath, "r") as file:
                content = file.read()

                reply_times = [int(line.split(":")[1].split()[0]) for line in content.split('\n') if
                               "reply_time:" in line]
                average_reply_time = sum(reply_times) / len(reply_times)
                average_reply_times.append(average_reply_time)

                reply_sizes = [int(line.split(":")[1].split()[0]) for line in content.split('\n') if
                               "reply_size:" in line]
                average_reply_size = sum(reply_sizes) / len(reply_sizes)
                average_reply_sizes.append(average_reply_size)
        else:
            print(f"File {filename} not found.")

    average_reply_time = sum(average_reply_times) / len(average_reply_times)
    server_pbc_reply_time_16.append(average_reply_time/1000)
    server_pbc_reply_size_16.append(sum(average_reply_sizes)/1000000)

for h in h128:
    average_reply_times = []
    average_reply_sizes = []
    for i in range(math.ceil(1.5 * h)):
        filename = f"pbc{i + 1}_{h}_{128}_log.txt"
        filepath = os.path.join(directory, filename)

        if os.path.exists(filepath):
            with open(filepath, "r") as file:
                content = file.read()

                reply_times = [int(line.split(":")[1].split()[0]) for line in content.split('\n') if
                               "reply_time:" in line]
                average_reply_time = sum(reply_times) / len(reply_times)
                average_reply_times.append(average_reply_time)

                reply_sizes = [int(line.split(":")[1].split()[0]) for line in content.split('\n') if
                               "reply_size:" in line]
                average_reply_size = sum(reply_sizes) / len(reply_sizes)
                average_reply_sizes.append(average_reply_size)
        else:
            print(f"File {filename} not found.")

    average_reply_time = sum(average_reply_times) / len(average_reply_times)
    server_pbc_reply_time_128.append(average_reply_time/1000)
    server_pbc_reply_size_128.append(sum(average_reply_sizes)/1000000)

for h in h256:
    average_reply_times = []
    average_reply_sizes = []
    for i in range(math.ceil(1.5 * h)):
        filename = f"pbc{i + 1}_{h}_{256}_log.txt"
        filepath = os.path.join(directory, filename)

        if os.path.exists(filepath):
            with open(filepath, "r") as file:
                content = file.read()

                reply_times = [int(line.split(":")[1].split()[0]) for line in content.split('\n') if
                               "reply_time:" in line]
                average_reply_time = sum(reply_times) / len(reply_times)
                average_reply_times.append(average_reply_time)

                reply_sizes = [int(line.split(":")[1].split()[0]) for line in content.split('\n') if
                               "reply_size:" in line]
                average_reply_size = sum(reply_sizes) / len(reply_sizes)
                average_reply_sizes.append(average_reply_size)
        else:
            print(f"File {filename} not found.")

    average_reply_time = sum(average_reply_times) / len(average_reply_times)
    server_pbc_reply_time_256.append(average_reply_time/1000)

    server_pbc_reply_size_256.append(sum(average_reply_sizes)/1000000)

# Plotting in subplots
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
#fig.suptitle("Server Eslapsed Time", fontsize = 16)

axs[0, 0].plot(h2, server_color_reply_time_2, label=r"$\mathbf{SEALPIR+}q\mathbf{TreePIR} (q=2)$")
axs[0, 0].plot(h2, server_pbc_reply_time_2, label="SEALPIR+PBC $(q=2)$", linestyle='dashed')
axs[0, 0].set_xlabel('h', fontsize=14, weight='bold')
axs[0, 0].set_ylabel('MB', fontsize=14, weight='bold')
axs[0, 0].tick_params(axis='x', labelsize=14)
axs[0, 0].tick_params(axis='y', labelsize=14)
axs[0, 0].legend(fontsize=16)
axs[0, 0].xaxis.set_major_locator(MaxNLocator(integer=True))

axs[0, 1].plot(h16, server_color_reply_time_16, label=r"$\mathbf{SEALPIR+}q\mathbf{TreePIR} (q=16)$")
axs[0, 1].plot(h16, server_pbc_reply_time_16, label="SEALPIR+PBC $(q=16)$", linestyle='dashed')
axs[0, 1].set_xlabel('h', fontsize=14, weight='bold')
axs[0, 1].set_ylabel('MB', fontsize=14, weight='bold')
axs[0, 1].tick_params(axis='x', labelsize=14)
axs[0, 1].tick_params(axis='y', labelsize=14)
axs[0, 1].legend(fontsize=16)
axs[0, 1].xaxis.set_major_locator(MaxNLocator(integer=True))

axs[1, 0].plot(h128, server_color_reply_time_128, label=r"$\mathbf{SEALPIR+}q\mathbf{TreePIR} (q=128)$")
axs[1, 0].plot(h128, server_pbc_reply_time_128, label="SEALPIR+PBC $(q=128)$", linestyle='dashed')
axs[1, 0].set_xlabel('h', fontsize=14, weight='bold')
axs[1, 0].set_ylabel('MB', fontsize=14, weight='bold')
axs[1, 0].tick_params(axis='x', labelsize=14)
axs[1, 0].tick_params(axis='y', labelsize=14)
axs[1, 0].legend(fontsize=16)
axs[1, 0].xaxis.set_major_locator(MaxNLocator(integer=True))

axs[1, 1].plot(h256, server_color_reply_time_256, label=r"$\mathbf{SEALPIR+}q\mathbf{TreePIR} (q=256)$")
axs[1, 1].plot(h256, server_pbc_reply_time_256, label="SEALPIR+PBC $(q=256)$", linestyle='dashed')
axs[1, 1].set_xlabel('h', fontsize=14, weight='bold')
axs[1, 1].set_ylabel('MB', fontsize=14, weight='bold')
axs[1, 1].tick_params(axis='x', labelsize=14)
axs[1, 1].tick_params(axis='y', labelsize=14)
axs[1, 1].legend(fontsize=16)
axs[1, 1].xaxis.set_major_locator(MaxNLocator(integer=True))

for ax in axs.flat:
    ax.set(xlabel='h', ylabel='ms')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("/Users/quangnhat/Desktop/Logs_CTA/figures/PIRservertime.pdf")

# Calculate the ratio between server_pbc_reply_time and server_color_reply_time for each q value
ratio_2 = [p / c for p, c in zip(server_pbc_reply_time_2, server_color_reply_time_2)]
ratio_16 = [p / c for p, c in zip(server_pbc_reply_time_16, server_color_reply_time_16)]
ratio_128 = [p / c for p, c in zip(server_pbc_reply_time_128, server_color_reply_time_128)]
ratio_256 = [p / c for p, c in zip(server_pbc_reply_time_256, server_color_reply_time_256)]

# Plotting in subplots
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
#fig.suptitle("Total Servers' Answer Costs", fontsize = 16)

axs[0, 0].plot(h2, server_color_reply_size_2, label=r"$\mathbf{SEALPIR+}q\mathbf{TreePIR} (q=2)$")
axs[0, 0].plot(h2, server_pbc_reply_size_2, label="SEALPIR+PBC $(q=2)$", linestyle='dashed')
axs[0, 0].set_xlabel('h', fontsize=14, weight='bold')
axs[0, 0].set_ylabel('MB', fontsize=14, weight='bold')
axs[0, 0].tick_params(axis='x', labelsize=14)
axs[0, 0].tick_params(axis='y', labelsize=14)
axs[0, 0].legend(fontsize=16)
axs[0, 0].xaxis.set_major_locator(MaxNLocator(integer=True))

axs[0, 1].plot(h16, server_color_reply_size_16, label=r"$\mathbf{SEALPIR+}q\mathbf{TreePIR} (q=16)$")
axs[0, 1].plot(h16, server_pbc_reply_size_16, label="SEALPIR+PBC $(q=16)$", linestyle='dashed')
axs[0, 1].set_xlabel('h', fontsize=14, weight='bold')
axs[0, 1].set_ylabel('MB', fontsize=14, weight='bold')
axs[0, 1].tick_params(axis='x', labelsize=14)
axs[0, 1].tick_params(axis='y', labelsize=14)
axs[0, 1].legend(fontsize=16)
axs[0, 1].xaxis.set_major_locator(MaxNLocator(integer=True))

axs[1, 0].plot(h128, server_color_reply_size_128, label=r"$\mathbf{SEALPIR+}q\mathbf{TreePIR} (q=128)$")
axs[1, 0].plot(h128, server_pbc_reply_size_128, label="SEALPIR+PBC $(q=128)$", linestyle='dashed')
axs[1, 0].set_xlabel('h', fontsize=14, weight='bold')
axs[1, 0].set_ylabel('MB', fontsize=14, weight='bold')
axs[1, 0].tick_params(axis='x', labelsize=14)
axs[1, 0].tick_params(axis='y', labelsize=14)
axs[1, 0].legend(fontsize=16)
axs[1, 0].xaxis.set_major_locator(MaxNLocator(integer=True))

axs[1, 1].plot(h256, server_color_reply_size_256, label=r"$\mathbf{SEALPIR+}q\mathbf{TreePIR} (q=256)$")
axs[1, 1].plot(h256, server_pbc_reply_size_256, label="SEALPIR+PBC $(q=256)$", linestyle='dashed')
axs[1, 1].set_xlabel('h', fontsize=14, weight='bold')
axs[1, 1].set_ylabel('MB', fontsize=14, weight='bold')
axs[1, 1].tick_params(axis='x', labelsize=14)
axs[1, 1].tick_params(axis='y', labelsize=14)
axs[1, 1].legend(fontsize=16)
axs[1, 1].xaxis.set_major_locator(MaxNLocator(integer=True))

for ax in axs.flat:
    ax.set(xlabel='h', ylabel='MB')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("/Users/quangnhat/Desktop/Logs_CTA/figures/PIRserverAnsSize.pdf")

# Calculate the ratio
ratio_2 = [p / c for p, c in zip(server_pbc_reply_size_2, server_color_reply_size_2)]
ratio_16 = [p / c for p, c in zip(server_pbc_reply_size_16, server_color_reply_size_16)]
ratio_128 = [p / c for p, c in zip(server_pbc_reply_size_128, server_color_reply_size_128)]
ratio_256 = [p / c for p, c in zip(server_pbc_reply_size_256, server_color_reply_size_256)]

#################################### PIR Client logs (color_client_h_q_log.txt/ pbc_client_h_q_log.txt) #################################################
client_color_query_time_2 = []
client_color_query_time_16 = []
client_color_query_time_128 = []
client_color_query_time_256 = []

client_color_extract_time_2 = []
client_color_extract_time_16 = []
client_color_extract_time_128 = []
client_color_extract_time_256 = []

client_color_query_size_2 = []
client_color_query_size_16 = []
client_color_query_size_128 = []
client_color_query_size_256 = []

for h in h2:
    host_data = defaultdict(lambda: {'query_sizes': [], 'query_times': [], 'extract_times': []})
    unique_hosts = set()
    filename = f"color_client_{h}_{2}_log.txt"
    filepath = os.path.join(directory, filename)
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            content = file.read()
            # Extract unique hosts from the log content
            lines = content.split("\n")
            current_host = None
            for line in lines:
                if "Host:" in line:
                    current_host = line.split(":")[1].strip()
                elif "query_size:" in line:
                    query_size = int(line.split(":")[1].strip().split()[0])
                    host_data[current_host]['query_sizes'].append(query_size)
                elif "query_time:" in line:
                    query_time = int(line.split(":")[1].strip().split()[0])
                    host_data[current_host]['query_times'].append(query_time)
                elif "extract_time:" in line:
                    extract_time = int(line.split(":")[1].strip().split()[0])
                    host_data[current_host]['extract_times'].append(extract_time)

            # Calculate the average values for each host
            for host, data in host_data.items():
                avg_query_size = sum(data['query_sizes']) / len(data['query_sizes']) if data['query_sizes'] else 0
                avg_query_time = sum(data['query_times']) / len(data['query_times']) if data['query_times'] else 0
                avg_extract_time = sum(data['extract_times']) / len(data['extract_times']) if data[
                    'extract_times'] else 0

    total_query_size = sum(sum(data['query_sizes']) for data in host_data.values())
    total_query_time = sum(sum(data['query_times']) for data in host_data.values())
    total_extract_time = sum(sum(data['extract_times']) for data in host_data.values())

    client_color_query_size_2.append(total_query_size/1000000)
    client_color_query_time_2.append(total_query_time/1000)
    client_color_extract_time_2.append(total_extract_time/1000)

for h in h16:
    host_data = defaultdict(lambda: {'query_sizes': [], 'query_times': [], 'extract_times': []})
    unique_hosts = set()
    filename = f"color_client_{h}_{16}_log.txt"
    filepath = os.path.join(directory, filename)
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            content = file.read()
            # Extract unique hosts from the log content
            lines = content.split("\n")
            current_host = None
            for line in lines:
                if "Host:" in line:
                    current_host = line.split(":")[1].strip()
                elif "query_size:" in line:
                    query_size = int(line.split(":")[1].strip().split()[0])
                    host_data[current_host]['query_sizes'].append(query_size)
                elif "query_time:" in line:
                    query_time = int(line.split(":")[1].strip().split()[0])
                    host_data[current_host]['query_times'].append(query_time)
                elif "extract_time:" in line:
                    extract_time = int(line.split(":")[1].strip().split()[0])
                    host_data[current_host]['extract_times'].append(extract_time)

            # Calculate the average values for each host
            for host, data in host_data.items():
                avg_query_size = sum(data['query_sizes']) / len(data['query_sizes']) if data['query_sizes'] else 0
                avg_query_time = sum(data['query_times']) / len(data['query_times']) if data['query_times'] else 0
                avg_extract_time = sum(data['extract_times']) / len(data['extract_times']) if data[
                    'extract_times'] else 0

    total_query_size = sum(sum(data['query_sizes']) for data in host_data.values())
    total_query_time = sum(sum(data['query_times']) for data in host_data.values())
    total_extract_time = sum(sum(data['extract_times']) for data in host_data.values())

    client_color_query_size_16.append(total_query_size/1000000)
    client_color_query_time_16.append(total_query_time/1000)
    client_color_extract_time_16.append(total_extract_time/1000)

for h in h128:
    host_data = defaultdict(lambda: {'query_sizes': [], 'query_times': [], 'extract_times': []})
    unique_hosts = set()
    filename = f"color_client_{h}_{128}_log.txt"
    filepath = os.path.join(directory, filename)
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            content = file.read()
            # Extract unique hosts from the log content
            lines = content.split("\n")
            current_host = None
            for line in lines:
                if "Host:" in line:
                    current_host = line.split(":")[1].strip()
                elif "query_size:" in line:
                    query_size = int(line.split(":")[1].strip().split()[0])
                    host_data[current_host]['query_sizes'].append(query_size)
                elif "query_time:" in line:
                    query_time = int(line.split(":")[1].strip().split()[0])
                    host_data[current_host]['query_times'].append(query_time)
                elif "extract_time:" in line:
                    extract_time = int(line.split(":")[1].strip().split()[0])
                    host_data[current_host]['extract_times'].append(extract_time)

            # Calculate the average values for each host
            for host, data in host_data.items():
                avg_query_size = sum(data['query_sizes']) / len(data['query_sizes']) if data['query_sizes'] else 0
                avg_query_time = sum(data['query_times']) / len(data['query_times']) if data['query_times'] else 0
                avg_extract_time = sum(data['extract_times']) / len(data['extract_times']) if data[
                    'extract_times'] else 0

    total_query_size = sum(sum(data['query_sizes']) for data in host_data.values())
    total_query_time = sum(sum(data['query_times']) for data in host_data.values())
    total_extract_time = sum(sum(data['extract_times']) for data in host_data.values())

    client_color_query_size_128.append(total_query_size/1000000)
    client_color_query_time_128.append(total_query_time/1000)
    client_color_extract_time_128.append(total_extract_time/1000)

for h in h256:
    host_data = defaultdict(lambda: {'query_sizes': [], 'query_times': [], 'extract_times': []})
    unique_hosts = set()
    filename = f"color_client_{h}_{256}_log.txt"
    filepath = os.path.join(directory, filename)
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            content = file.read()
            # Extract unique hosts from the log content
            lines = content.split("\n")
            current_host = None
            for line in lines:
                if "Host:" in line:
                    current_host = line.split(":")[1].strip()
                elif "query_size:" in line:
                    query_size = int(line.split(":")[1].strip().split()[0])
                    host_data[current_host]['query_sizes'].append(query_size)
                elif "query_time:" in line:
                    query_time = int(line.split(":")[1].strip().split()[0])
                    host_data[current_host]['query_times'].append(query_time)
                elif "extract_time:" in line:
                    extract_time = int(line.split(":")[1].strip().split()[0])
                    host_data[current_host]['extract_times'].append(extract_time)

            # Calculate the average values for each host
            for host, data in host_data.items():
                avg_query_size = sum(data['query_sizes']) / len(data['query_sizes']) if data['query_sizes'] else 0
                avg_query_time = sum(data['query_times']) / len(data['query_times']) if data['query_times'] else 0
                avg_extract_time = sum(data['extract_times']) / len(data['extract_times']) if data[
                    'extract_times'] else 0

    total_query_size = sum(sum(data['query_sizes']) for data in host_data.values())
    total_query_time = sum(sum(data['query_times']) for data in host_data.values())
    total_extract_time = sum(sum(data['extract_times']) for data in host_data.values())

    client_color_query_size_256.append(total_query_size/1000000)
    client_color_query_time_256.append(total_query_time/1000)
    client_color_extract_time_256.append(total_extract_time/1000)

client_pbc_query_time_2 = []
client_pbc_query_time_16 = []
client_pbc_query_time_128 = []
client_pbc_query_time_256 = []

client_pbc_extract_time_2 = []
client_pbc_extract_time_16 = []
client_pbc_extract_time_128 = []
client_pbc_extract_time_256 = []

client_pbc_query_size_2 = []
client_pbc_query_size_16 = []
client_pbc_query_size_128 = []
client_pbc_query_size_256 = []

for h in h2:
    host_data = defaultdict(lambda: {'query_sizes': [], 'query_times': [], 'extract_times': []})
    unique_hosts = set()
    filename = f"pbc_client_{h}_{2}_log.txt"
    filepath = os.path.join(directory, filename)
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            content = file.read()
            # Extract unique hosts from the log content
            lines = content.split("\n")
            current_host = None
            for line in lines:
                if "Host:" in line:
                    current_host = line.split(":")[1].strip()
                elif "query_size:" in line:
                    query_size = int(line.split(":")[1].strip().split()[0])
                    host_data[current_host]['query_sizes'].append(query_size)
                elif "query_time:" in line:
                    query_time = int(line.split(":")[1].strip().split()[0])
                    host_data[current_host]['query_times'].append(query_time)
                elif "extract_time:" in line:
                    extract_time = int(line.split(":")[1].strip().split()[0])
                    host_data[current_host]['extract_times'].append(extract_time)

            # Calculate the average values for each host
            for host, data in host_data.items():
                avg_query_size = sum(data['query_sizes']) / len(data['query_sizes']) if data['query_sizes'] else 0
                avg_query_time = sum(data['query_times']) / len(data['query_times']) if data['query_times'] else 0
                avg_extract_time = sum(data['extract_times']) / len(data['extract_times']) if data[
                    'extract_times'] else 0

    total_query_size = sum(sum(data['query_sizes']) for data in host_data.values())
    total_query_time = sum(sum(data['query_times']) for data in host_data.values())
    total_extract_time = sum(sum(data['extract_times']) for data in host_data.values())

    client_pbc_query_size_2.append(total_query_size/1000000)
    client_pbc_query_time_2.append(total_query_time/1000)
    client_pbc_extract_time_2.append(total_extract_time/1000)

for h in h16:
    host_data = defaultdict(lambda: {'query_sizes': [], 'query_times': [], 'extract_times': []})
    unique_hosts = set()
    filename = f"pbc_client_{h}_{16}_log.txt"
    filepath = os.path.join(directory, filename)
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            content = file.read()
            # Extract unique hosts from the log content
            lines = content.split("\n")
            current_host = None
            for line in lines:
                if "Host:" in line:
                    current_host = line.split(":")[1].strip()
                elif "query_size:" in line:
                    query_size = int(line.split(":")[1].strip().split()[0])
                    host_data[current_host]['query_sizes'].append(query_size)
                elif "query_time:" in line:
                    query_time = int(line.split(":")[1].strip().split()[0])
                    host_data[current_host]['query_times'].append(query_time)
                elif "extract_time:" in line:
                    extract_time = int(line.split(":")[1].strip().split()[0])
                    host_data[current_host]['extract_times'].append(extract_time)

            # Calculate the average values for each host
            for host, data in host_data.items():
                avg_query_size = sum(data['query_sizes']) / len(data['query_sizes']) if data['query_sizes'] else 0
                avg_query_time = sum(data['query_times']) / len(data['query_times']) if data['query_times'] else 0
                avg_extract_time = sum(data['extract_times']) / len(data['extract_times']) if data[
                    'extract_times'] else 0

    total_query_size = sum(sum(data['query_sizes']) for data in host_data.values())
    total_query_time = sum(sum(data['query_times']) for data in host_data.values())
    total_extract_time = sum(sum(data['extract_times']) for data in host_data.values())

    client_pbc_query_size_16.append(total_query_size/1000000)
    client_pbc_query_time_16.append(total_query_time/1000)
    client_pbc_extract_time_16.append(total_extract_time/1000)

for h in h128:
    host_data = defaultdict(lambda: {'query_sizes': [], 'query_times': [], 'extract_times': []})
    unique_hosts = set()
    filename = f"pbc_client_{h}_{128}_log.txt"
    filepath = os.path.join(directory, filename)
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            content = file.read()
            # Extract unique hosts from the log content
            lines = content.split("\n")
            current_host = None
            for line in lines:
                if "Host:" in line:
                    current_host = line.split(":")[1].strip()
                elif "query_size:" in line:
                    query_size = int(line.split(":")[1].strip().split()[0])
                    host_data[current_host]['query_sizes'].append(query_size)
                elif "query_time:" in line:
                    query_time = int(line.split(":")[1].strip().split()[0])
                    host_data[current_host]['query_times'].append(query_time)
                elif "extract_time:" in line:
                    extract_time = int(line.split(":")[1].strip().split()[0])
                    host_data[current_host]['extract_times'].append(extract_time)

            # Calculate the average values for each host
            for host, data in host_data.items():
                avg_query_size = sum(data['query_sizes']) / len(data['query_sizes']) if data['query_sizes'] else 0
                avg_query_time = sum(data['query_times']) / len(data['query_times']) if data['query_times'] else 0
                avg_extract_time = sum(data['extract_times']) / len(data['extract_times']) if data[
                    'extract_times'] else 0

    total_query_size = sum(sum(data['query_sizes']) for data in host_data.values())
    total_query_time = sum(sum(data['query_times']) for data in host_data.values())
    total_extract_time = sum(sum(data['extract_times']) for data in host_data.values())

    client_pbc_query_size_128.append(total_query_size/1000000)
    client_pbc_query_time_128.append(total_query_time/1000)
    client_pbc_extract_time_128.append(total_extract_time/1000)

for h in h256:
    host_data = defaultdict(lambda: {'query_sizes': [], 'query_times': [], 'extract_times': []})
    unique_hosts = set()
    filename = f"pbc_client_{h}_{256}_log.txt"
    filepath = os.path.join(directory, filename)
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            content = file.read()
            # Extract unique hosts from the log content
            lines = content.split("\n")
            current_host = None
            for line in lines:
                if "Host:" in line:
                    current_host = line.split(":")[1].strip()
                elif "query_size:" in line:
                    query_size = int(line.split(":")[1].strip().split()[0])
                    host_data[current_host]['query_sizes'].append(query_size)
                elif "query_time:" in line:
                    query_time = int(line.split(":")[1].strip().split()[0])
                    host_data[current_host]['query_times'].append(query_time)
                elif "extract_time:" in line:
                    extract_time = int(line.split(":")[1].strip().split()[0])
                    host_data[current_host]['extract_times'].append(extract_time)

            # Calculate the average values for each host
            for host, data in host_data.items():
                avg_query_size = sum(data['query_sizes']) / len(data['query_sizes']) if data['query_sizes'] else 0
                avg_query_time = sum(data['query_times']) / len(data['query_times']) if data['query_times'] else 0
                avg_extract_time = sum(data['extract_times']) / len(data['extract_times']) if data[
                    'extract_times'] else 0

    total_query_size = sum(sum(data['query_sizes']) for data in host_data.values())
    total_query_time = sum(sum(data['query_times']) for data in host_data.values())
    total_extract_time = sum(sum(data['extract_times']) for data in host_data.values())

    client_pbc_query_size_256.append(total_query_size/1000000)
    client_pbc_query_time_256.append(total_query_time/1000)
    client_pbc_extract_time_256.append(total_extract_time/1000)

# Plotting in subplots
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
#fig.suptitle("Total Client Queries Costs", fontsize = 16)

axs[0, 0].plot(h2, client_color_query_size_2, label=r"$\mathbf{SEALPIR+}q\mathbf{TreePIR} (q=2)$")
axs[0, 0].plot(h2, client_pbc_query_size_2, label="SEALPIR+PBC $(q=2)$", linestyle='dashed')
axs[0, 0].set_xlabel('h', fontsize=14, weight='bold')
axs[0, 0].set_ylabel('MB', fontsize=14, weight='bold')
axs[0, 0].tick_params(axis='x', labelsize=14)
axs[0, 0].tick_params(axis='y', labelsize=14)
axs[0, 0].legend(fontsize=16)
axs[0, 0].xaxis.set_major_locator(MaxNLocator(integer=True))

axs[0, 1].plot(h16, client_color_query_size_16, label=r"$\mathbf{SEALPIR+}q\mathbf{TreePIR} (q=16)$")
axs[0, 1].plot(h16, client_pbc_query_size_16, label="SEALPIR+PBC $(q=16)$", linestyle='dashed')
axs[0, 1].set_xlabel('h', fontsize=14, weight='bold')
axs[0, 1].set_ylabel('MB', fontsize=14, weight='bold')
axs[0, 1].tick_params(axis='x', labelsize=14)
axs[0, 1].tick_params(axis='y', labelsize=14)
axs[0, 1].legend(fontsize=16)
axs[0, 1].xaxis.set_major_locator(MaxNLocator(integer=True))

axs[1, 0].plot(h128, client_color_query_size_128, label=r"$\mathbf{SEALPIR+}q\mathbf{TreePIR} (q=128)$")
axs[1, 0].plot(h128, client_pbc_query_size_128, label="SEALPIR+PBC $(q=128)$", linestyle='dashed')
axs[1, 0].set_xlabel('h', fontsize=14, weight='bold')
axs[1, 0].set_ylabel('MB', fontsize=14, weight='bold')
axs[1, 0].tick_params(axis='x', labelsize=14)
axs[1, 0].tick_params(axis='y', labelsize=14)
axs[1, 0].legend(fontsize=16)
axs[1, 0].xaxis.set_major_locator(MaxNLocator(integer=True))

axs[1, 1].plot(h256, client_color_query_size_256, label=r"$\mathbf{SEALPIR+}q\mathbf{TreePIR} (q=256)$")
axs[1, 1].plot(h256, client_pbc_query_size_256, label="SEALPIR+PBC $(q=256)$", linestyle='dashed')
axs[1, 1].set_xlabel('h', fontsize=14, weight='bold')
axs[1, 1].set_ylabel('MB', fontsize=14, weight='bold')
axs[1, 1].tick_params(axis='x', labelsize=14)
axs[1, 1].tick_params(axis='y', labelsize=14)
axs[1, 1].legend(fontsize=16)
axs[1, 1].xaxis.set_major_locator(MaxNLocator(integer=True))

for ax in axs.flat:
    ax.set(xlabel='h', ylabel='MB')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("/Users/quangnhat/Desktop/Logs_CTA/figures/PIRClientQuerySize.pdf")

# Calculate the ratio
ratio_2 = [p / c for p, c in zip(client_pbc_query_size_2, client_color_query_size_2)]
ratio_16 = [p / c for p, c in zip(client_pbc_query_size_16, client_color_query_size_16)]
ratio_128 = [p / c for p, c in zip(client_pbc_query_size_128, client_color_query_size_128)]
ratio_256 = [p / c for p, c in zip(client_pbc_query_size_256, client_color_query_size_256)]

# Plotting in subplots
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
#fig.suptitle("Total Client Generated Queries Costs", fontsize = 16)

axs[0, 0].plot(h2, client_color_query_time_2, label=r"$\mathbf{SEALPIR+}q\mathbf{TreePIR} (q=2)$")
axs[0, 0].plot(h2, client_pbc_query_time_2, label="SEALPIR+PBC $(q=2)$", linestyle='dashed')
axs[0, 0].set_xlabel('h', fontsize=14, weight='bold')
axs[0, 0].set_ylabel('MB', fontsize=14, weight='bold')
axs[0, 0].tick_params(axis='x', labelsize=14)
axs[0, 0].tick_params(axis='y', labelsize=14)
axs[0, 0].legend(fontsize=16)
axs[0, 0].xaxis.set_major_locator(MaxNLocator(integer=True))

axs[0, 1].plot(h16, client_color_query_time_16, label=r"$\mathbf{SEALPIR+}q\mathbf{TreePIR} (q=16)$")
axs[0, 1].plot(h16, client_pbc_query_time_16, label="SEALPIR+PBC $(q=16)$", linestyle='dashed')
axs[0, 1].set_xlabel('h', fontsize=14, weight='bold')
axs[0, 1].set_ylabel('MB', fontsize=14, weight='bold')
axs[0, 1].tick_params(axis='x', labelsize=14)
axs[0, 1].tick_params(axis='y', labelsize=14)
axs[0, 1].legend(fontsize=16)
axs[0, 1].xaxis.set_major_locator(MaxNLocator(integer=True))

axs[1, 0].plot(h128, client_color_query_time_128, label=r"$\mathbf{SEALPIR+}q\mathbf{TreePIR} (q=128)$")
axs[1, 0].plot(h128, client_pbc_query_time_128, label="SEALPIR+PBC $(q=128)$", linestyle='dashed')
axs[1, 0].set_xlabel('h', fontsize=14, weight='bold')
axs[1, 0].set_ylabel('MB', fontsize=14, weight='bold')
axs[1, 0].tick_params(axis='x', labelsize=14)
axs[1, 0].tick_params(axis='y', labelsize=14)
axs[1, 0].legend(fontsize=16)
axs[1, 0].xaxis.set_major_locator(MaxNLocator(integer=True))

axs[1, 1].plot(h256, client_color_query_time_256, label=r"$\mathbf{SEALPIR+}q\mathbf{TreePIR} (q=256)$")
axs[1, 1].plot(h256, client_pbc_query_time_256, label="SEALPIR+PBC $(q=256)$", linestyle='dashed')
axs[1, 1].set_xlabel('h', fontsize=14, weight='bold')
axs[1, 1].set_ylabel('MB', fontsize=14, weight='bold')
axs[1, 1].tick_params(axis='x', labelsize=14)
axs[1, 1].tick_params(axis='y', labelsize=14)
axs[1, 1].legend(fontsize=16)
axs[1, 1].xaxis.set_major_locator(MaxNLocator(integer=True))

for ax in axs.flat:
    ax.set(xlabel='h', ylabel='ms')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("/Users/quangnhat/Desktop/Logs_CTA/figures/PIRClientQueryTime.pdf")

# Plotting in subplots
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
#fig.suptitle("Total Client Decoded Costs", fontsize = 16)

axs[0, 0].plot(h2, client_color_extract_time_2, label=r"$\mathbf{SEALPIR+}q\mathbf{TreePIR} (q=2)$")
axs[0, 0].plot(h2, client_pbc_extract_time_2, label="SEALPIR+PBC $(q=2)$", linestyle='dashed')
axs[0, 0].set_xlabel('h', fontsize=14, weight='bold')
axs[0, 0].set_ylabel('MB', fontsize=14, weight='bold')
axs[0, 0].tick_params(axis='x', labelsize=14)
axs[0, 0].tick_params(axis='y', labelsize=14)
axs[0, 0].legend(fontsize=16)
axs[0, 0].xaxis.set_major_locator(MaxNLocator(integer=True))

axs[0, 1].plot(h16, client_color_extract_time_16, label=r"$\mathbf{SEALPIR+}q\mathbf{TreePIR} (q=16)$")
axs[0, 1].plot(h16, client_pbc_extract_time_16, label="SEALPIR+PBC $(q=16)$", linestyle='dashed')
axs[0, 1].set_xlabel('h', fontsize=14, weight='bold')
axs[0, 1].set_ylabel('MB', fontsize=14, weight='bold')
axs[0, 1].tick_params(axis='x', labelsize=14)
axs[0, 1].tick_params(axis='y', labelsize=14)
axs[0, 1].legend(fontsize=16)
axs[0, 1].xaxis.set_major_locator(MaxNLocator(integer=True))

axs[1, 0].plot(h128, client_color_extract_time_128, label=r"$\mathbf{SEALPIR+}q\mathbf{TreePIR} (q=128)$")
axs[1, 0].plot(h128, client_pbc_extract_time_128, label="SEALPIR+PBC $(q=128)$", linestyle='dashed')
axs[1, 0].set_xlabel('h', fontsize=14, weight='bold')
axs[1, 0].set_ylabel('MB', fontsize=14, weight='bold')
axs[1, 0].tick_params(axis='x', labelsize=14)
axs[1, 0].tick_params(axis='y', labelsize=14)
axs[1, 0].legend(fontsize=16)
axs[1, 0].xaxis.set_major_locator(MaxNLocator(integer=True))

axs[1, 1].plot(h256, client_color_extract_time_256, label=r"$\mathbf{SEALPIR+}q\mathbf{TreePIR} (q=256)$")
axs[1, 1].plot(h256, client_pbc_extract_time_256, label="SEALPIR+PBC $(q=256)$", linestyle='dashed')
axs[1, 1].set_xlabel('h', fontsize=14, weight='bold')
axs[1, 1].set_ylabel('MB', fontsize=14, weight='bold')
axs[1, 1].tick_params(axis='x', labelsize=14)
axs[1, 1].tick_params(axis='y', labelsize=14)
axs[1, 1].legend(fontsize=16)
axs[1, 1].xaxis.set_major_locator(MaxNLocator(integer=True))

for ax in axs.flat:
    ax.set(xlabel='h', ylabel='ms')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("/Users/quangnhat/Desktop/Logs_CTA/figures/PIRClientExtractTime.pdf")


################################ Appendices
# Given range for h with q = 2
h2 = range(10, 33)

# Given range for h with q = 16
h16 = range(3, 9)

# Given range for h with q = 128
h128 = range(2, 5)

# Given range for h with q = 256
h256 = range(2, 5)

#################################### CTA_h_q_log.txt #################################################
cta_time_2 = []
cta_time_16 = []
cta_time_128 = []
cta_time_256 = []

for h in h2:
    filename = f"CTA_{h}_{2}_log.txt"
    filepath = os.path.join(directory, filename)

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            content = file.readlines()

        # Extract and calculate average CTA time
        cta_time = [int(line.split(":")[1].split()[0]) for line in content if "CTA:" in line]
        cta_average_time = sum(cta_time) / len(cta_time)
        cta_time_2.append(cta_average_time)

    else:
        print(f"File {filename} not found.")

for h in h16:
    filename = f"CTA_{h}_{16}_log.txt"
    filepath = os.path.join(directory, filename)

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            content = file.readlines()

        # Extract and calculate average CTA time
        cta_time = [int(line.split(":")[1].split()[0]) for line in content if "CTA:" in line]
        cta_average_time = sum(cta_time) / len(cta_time)
        cta_time_16.append(cta_average_time)

    else:
        print(f"File {filename} not found.")

for h in h128:
    filename = f"CTA_{h}_{128}_log.txt"
    filepath = os.path.join(directory, filename)

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            content = file.readlines()

        # Extract and calculate average CTA time
        cta_time = [int(line.split(":")[1].split()[0]) for line in content if "CTA:" in line]
        cta_average_time = sum(cta_time) / len(cta_time)
        cta_time_128.append(cta_average_time)

    else:
        print(f"File {filename} not found.")

for h in h256:
    filename = f"CTA_{h}_{256}_log.txt"
    filepath = os.path.join(directory, filename)

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            content = file.readlines()

        # Extract and calculate average CTA time
        cta_time = [int(line.split(":")[1].split()[0]) for line in content if "CTA:" in line]
        cta_average_time = sum(cta_time) / len(cta_time)
        cta_time_256.append(cta_average_time)

    else:
        print(f"File {filename} not found.")

#################################### CTAindexing_h_q_log.txt #################################################
cta_indexing_time_2 = []
cta_indexing_time_16 = []
cta_indexing_time_128 = []
cta_indexing_time_256 = []

# Given range for h with q = 2
h2 = range(10, 36)

for h in h2:
    filename = f"CTAindexing_{h}_{2}_log.txt"
    filepath = os.path.join(directory, filename)

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            content = file.readlines()

        # Extract and calculate average indexing time
        indexing_time = [int(line.split(":")[1].split()[0]) for line in content if "Indexing:" in line]
        indexing_average_time = sum(indexing_time) / len(indexing_time)
        cta_indexing_time_2.append(indexing_average_time/1000)

    else:
        print(f"File {filename} not found.")

for h in h16:
    filename = f"CTAindexing_{h}_{16}_log.txt"
    filepath = os.path.join(directory, filename)

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            content = file.readlines()

        # Extract and calculate average indexing time
        indexing_time = [int(line.split(":")[1].split()[0]) for line in content if "Indexing:" in line]
        indexing_average_time = sum(indexing_time) / len(indexing_time)
        cta_indexing_time_16.append(indexing_average_time/1000)

    else:
        print(f"File {filename} not found.")

for h in h128:
    filename = f"CTAindexing_{h}_{128}_log.txt"
    filepath = os.path.join(directory, filename)

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            content = file.readlines()

        # Extract and calculate average indexing time
        indexing_time = [int(line.split(":")[1].split()[0]) for line in content if "Indexing:" in line]
        indexing_average_time = sum(indexing_time) / len(indexing_time)
        cta_indexing_time_128.append(indexing_average_time/1000)

    else:
        print(f"File {filename} not found.")

for h in h256:
    filename = f"CTAindexing_{h}_{256}_log.txt"
    filepath = os.path.join(directory, filename)

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            content = file.readlines()

        # Extract and calculate average indexing time
        indexing_time = [int(line.split(":")[1].split()[0]) for line in content if "Indexing:" in line]
        indexing_average_time = sum(indexing_time) / len(indexing_time)
        cta_indexing_time_256.append(indexing_average_time/1000)

    else:
        print(f"File {filename} not found.")

'''print(cta_indexing_time_2)
print(cta_indexing_time_16)
print(cta_indexing_time_128)
print(cta_indexing_time_256)'''

'''print(cta_time_2)
print(cta_time_16)
print(cta_time_128)
print(cta_time_256)'''
