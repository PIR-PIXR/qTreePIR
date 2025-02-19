import java.io.*;
import java.util.*;
import java.util.stream.*;
import java.util.Random;
import com.google.gson.*;
import java.security.SecureRandom;

public class ATC {
    public static void main(String[] args) {
        final String PATH = "/qTreePIR/ATC/";

        AncestralTreeColoringAlgorithm ATC = new AncestralTreeColoringAlgorithm();
        byte h = 0; //h is the height of a tree
        int q = 0; //q is the number of children of a non-leaf node
        int[] path;
        long[] pathID;
        Random random = new Random();
        NodesSet[] NodesSets = new NodesSet[0]; //Color sequence of balanced/unbalanced sets
        List<NumColor> c = new ArrayList<>(); //List of color sequence c
        ArrayList<Integer> vectorC = new ArrayList<>(); //The color sequence c = [c1,...,ch]
        char[] color = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q'
                , 'R','S', 'T', 'U', 'V','W', 'X', 'Y', 'Z','0', '1', '2', '3', '4', '5', '6', '7','8', '9'};

        if (args.length >= 2) {
            h = (byte) Integer.parseInt(args[0]);
            q = Integer.parseInt(args[1]);
        }
        else {
            h = h(); //Enter the height of a tree "h" from keyboard
            q = q(); //Enter the value q-ary of a tree "q" from keyboard
        }

        long N = (long) (q * (Math.pow(q, h) - 1) / (q - 1)); //Tree size = # nodes except the root node
        int[] a = ATC.SplitColor(h, N, q, 1);
        for (int i = 0; i < a.length; i++) {
            c.add(new NumColor(color[i], a[i]));
        }

        c.forEach(x -> vectorC.add(x.getSize()));
        System.out.println("*** Input:");
        System.out.println("    Tree height: h = " + h);
        System.out.println("    q-Ary      : q = " + q);
        System.out.println("    c = " + vectorC);

        PrintWriter logATC = null;
        PrintWriter logIndex = null;
	try {
    	    logATC = new PrintWriter(new FileWriter(PATH + "ATC_" + h + "_" + q + "_log.txt"));
    	    logIndex = new PrintWriter(new FileWriter(PATH + "ATCindexing_" + h + "_" + q + "_log.txt"));
	} catch (IOException e) {
    	    e.printStackTrace();
	}

	String filePath = "list_TXs_" + h + "_" + q + ".txt";
        List<Long> randIndices = new ArrayList<>();

        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
            String line;
            while ((line = reader.readLine()) != null) {
                randIndices.add(Long.parseLong(line.trim()));
            }
        } catch (IOException | NumberFormatException e) {
            e.printStackTrace();
        }

        // Testing
        for (Long j : randIndices) {
            ////////////////////////////////////////Coloring Tree Algorithm/////////////////////////////////////////////
            long startTime = System.nanoTime(); //************************** START *************************
            NodesSets = ATC.ColoringTree(h, q, c); //Coloring q-ary Tree Algorithm
            long endTime = System.nanoTime(); //***************************** END **************************
            long timeElapsed = (endTime - startTime) / 1000000;
            System.out.println("*** Output:");
            System.out.println("    Coloring q-ary Tree - Execution time in milliseconds: " + timeElapsed);
            logATC.println("ATC: " + timeElapsed + " (ms)");

            ////////////////////////////////////////Sub-Indices Algorithm///////////////////////////////////////////////
            SubIndices sb = new SubIndices(h, q, j);
            path = sb.Path();
            pathID = sb.PathID();

            long start = System.nanoTime(); // ************************** START *************************
            LinkedHashMap<Character, Integer> indices = sb.mapIndices(path, pathID, c);
            long end = System.nanoTime(); // ***************************** END **************************
            long elapsed = (end - start) / 1000;
            System.out.println("    Indexing q-ary Tree - Execution time in microseconds: " + elapsed);
            logIndex.println("Indexing: " + elapsed + " (us)");

            HashMap<Character, Long> NodeID = new HashMap<>();
            int k = 0;
            for (Map.Entry<Character, Integer> entry : indices.entrySet()) {
                NodeID.put(entry.getKey(), pathID[k]);
                k++;
            }

            String idxName = "color_indices_" + h + "_" + q + ".txt";
            saveRandIndices (color, NodeID, indices, h, q, idxName, j);
        }

        logATC.close();
        logIndex.close();

        ////////////////////////////////////////Generate Database///////////////////////////////////////////////////

        genColorDB(h, q, 32, PATH, NodesSets);
    }

    private static void genColorDB(int height, int q_size, int SIZE, String PATH, NodesSet[] NodesSets) {
        Gson gson = new Gson();
        Arrays.stream(NodesSets).forEach(s -> {
            // Create a JSON array to hold NodeID-value pairs
            JsonArray nodeValueArray = new JsonArray();
            JsonObject nodeValueObject = new JsonObject();
            Arrays.stream(s.getAddNodes()).forEach(r -> nodeValueObject.addProperty(String.valueOf(r), getRandomString(SIZE)));
            nodeValueArray.add(nodeValueObject);
            // Serialize the JSON array to a string
            String jsonString = gson.toJson(nodeValueArray);
            // Specify the file path where you want to write the JSON data
            String filePath = PATH + "color" + s.getColorSet() + "_" + height + "_" + q_size + ".json";
            // Write the JSON data to the file
            try (FileWriter fileWriter = new FileWriter(filePath)) {
                fileWriter.write(jsonString);
                System.out.println("JSON data written to " + filePath);
            } catch (IOException e) {
                e.printStackTrace();
            }
        });
    }

    private static void saveRandIndices(char[] color, HashMap<Character, Long> nodeID, LinkedHashMap<Character, Integer> indices, byte h, int q, String filePath, long j) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filePath, true))) {
            writer.write("TX_index: " + j);
            writer.newLine();
            for (int i = 0; i < nodeID.size(); i++) {
                writer.write("color" + color[i] + "_" + h + "_" + q + ".json" +"; NodeID: " + nodeID.get(color[i]) + "; Index: " + indices.get(color[i]));
                writer.newLine();
            }
            System.out.println("Indexing written to " + filePath);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    //Enter the height of a tree h from keyboard. h has to greater than or equal to 2.
    public static Byte h() {
        byte height;
        Scanner input = new Scanner(System.in);
        do {
            System.out.print("Enter the height of a tree \"h\" = ");
            while (!input.hasNextByte()) {
                System.out.print("NOTE! You have to put integer of the height \"h\" = ");
                input.next();
            }
            height = input.nextByte();
            if (height < 2) {
                System.out.println("NOTE! Enter an Integer >= 2");
            }
        } while (height < 2); //The height "h" input has to greater than or equal 2

        return height;
    }

    //Enter q from keyboard. q has to an even number.
    public static int q() {
        int qAry;
        Scanner input = new Scanner(System.in);
        do {
            System.out.print("Enter the value q of a q-ary tree \"q\" = ");
            while (!input.hasNextInt()) {
                System.out.print("NOTE! You have to put integer of the value \"q\" = ");
                input.next();
            }
            qAry = input.nextInt();
            if (qAry < 2) {
                System.out.println("NOTE! Enter an Integer >= 2");
            }
        } while (qAry < 2); //The height "h" input has to greater than or equal 2
        return qAry;
    }

    // Method to generate a random string of a specified length
    private static String getRandomString(int length) {
        byte[] randomBytes = new byte[length];
        SecureRandom secRandom = new SecureRandom();
        secRandom.nextBytes(randomBytes);
        StringBuilder result = new StringBuilder();
        for (byte b : randomBytes) {
            result.append(String.format("%02X", b));
        }
        return result.toString();
    }
}

//-----------------------------------------AncestralTreeColoringAlgorithm class---------------------------------------------------------------
class AncestralTreeColoringAlgorithm {
    NodesSet[] NodesSets;
    List<List<NumColor>> C = new ArrayList<>();

    //The algorithm can discover an ancestral coloring $\vec{c}$ of $T_q(h)$ for a feasible color sequence $\vec{c}$ in \textit{both} balanced or unbalanced sequence.
    public NodesSet[] ColoringTree(byte h, int q, List<NumColor> c) {
        int R = 1; //the root of 𝑇_q (ℎ) is 1
        NodesSets = new NodesSet [h];

        for (byte i = 0; i < h; i++) {
            int size = c.get(i).getSize();
            NodesSets[i] = new NodesSet(c.get(i).getColor(), size);
        }

        CTRecursive(R, h, q, c);

        return NodesSets;
    }

    // $R$ is the root node of the current subtree $T_q(h)$; Either $R = 1$ or $R$ has already been colored in the previous call
    // This procedure colors the $q$ children of $R$ and create feasible color sequences for $q$ sub-trees
    public void CTRecursive(long R, byte h, int q, List<NumColor> c) {
        int x = 0, index = 0;
        int[] childID = new int[q];
        List<List<NumColor>> subTrees = new ArrayList<>(q); //q vectors

        C.clear();

        //Uncomment this line to check if a sequence c is h&q-feasible
        //if (!isFeasible(h, q, c)) return;

        if (h > 0) {
            for ( long r = q * R - q + 2; r <= q * R + 1; r++){
                childID[index] = (int) r;
                index++;
            }

            //Assign Color 1 to all children; And add all children to the same color set.
            if (c.get(0).getSize() == q) {
                x = q;
                for (NodesSet s : NodesSets) {
                    if (s.getColorSet() == c.get(0).getColor()) {
                        for (int j = 0; j < q; j++){
                            s.addNode(childID[j]);
                        }
                    }
                }
            }
            //Assign Color 1 to x children and Color 2 to y children.
            else if(c.get(0).getSize() > q) {
                if (h > 2) x = Finding_x(c.get(0).getSize(), c.get(1).getSize(), c.get(2).getSize(), q);
                else x = Finding_x(c.get(0).getSize(), c.get(1).getSize(), 0, q);
                for (NodesSet s : NodesSets) {
                    if (s.getColorSet() == c.get(0).getColor()) {
                        for (int i = 0; i < x; i ++){
                            s.addNode(childID[i]);
                        }
                    }
                    if (s.getColorSet() == c.get(1).getColor()) {
                        for (int i = x; i < q; i ++){
                            s.addNode(childID[i]);
                        }
                    }
                }
            }

            //Split the feasible sequence c to q feasible sequences for q sub-trees.
            if (h > 1) {
                C = FeasibleSplit(h, q, x, c);
                for (int i = 0; i < q; i++){
                    subTrees.add(i, C.get(i));
                }

                for (int i = 0; i < q; i++){
                    Collections.sort(subTrees.get(i));
                    CTRecursive(childID[i], (byte) (h - 1), q, subTrees.get(i));
                }
            }
        }
    }

    /* This algorithm splits a ℎ-feasible sequence into q (ℎ − 1)-feasible ones, which will be used for coloring the subtrees; only works when ℎ ≥ 2.
    Note that the splitting rule (see FeasibleSplit(h, q, x, c)) ensures that if Color 𝑖 is used for a node then it will no longer be used in the subtree rooted at that node,
    hence guaranteeing the Ancestral Property.*/
    public List<List<NumColor>> FeasibleSplit(byte h, int q, int x, List<NumColor> c) {
        C.clear();
        int y = q - x;
        int c_1_prime, c_2_prime;
        int S_x = 0, S_y = 0;
        List<List<NumColor>> subTrees = new ArrayList<>(q);

        for (int i = 0; i < q; i++) {
            subTrees.add(i, new ArrayList<>(h - 1));
        }

        if (h == 2) {
            if (c.get(0).getSize() == q) {
                for (int i = 0; i < q; i++){
                    subTrees.get(i).add(new NumColor(c.get(1).getColor(), c.get(1).getSize() / q));
                }
            }
            else {
                for (int i = 0; i < q; i++){
                    if (i < x){
                        subTrees.get(i).add(new NumColor(c.get(1).getColor(), (c.get(1).getSize() - (q - x)) / x));
                    }
                    else {
                        subTrees.get(i).add(new NumColor(c.get(0).getColor(), (c.get(0).getSize() - x) / y));
                    }
                }
            }

            for (int j = 0; j < q; j++){
                Collections.sort(subTrees.get(j));
            }

            C.addAll(subTrees);
            return C;
        }
        else if (h > 2) {
            long N_subtree = (long) ((long) q*(Math.pow(q,h - 1)-1)/(q-1)); //subtree size = # nodes in each subtree except the root node
            HashMap<Integer, Integer> sortSum = new HashMap<Integer, Integer> (); //key = pos; value = recent sum
            HashMap<Integer, Integer> sortSum_x = new HashMap<Integer, Integer> (); //key = pos; value = recent sum
            HashMap<Integer, Integer> sortSum_y = new HashMap<Integer, Integer> (); //key = pos; value = recent sum

            //Case 1: 𝑐1 = q
            if (c.get(0).getSize() == q) {
                int[] a;
                int pos = 0; //position subtrees;
                int j;

                //Split c_i to q subtrees
                for (int i = 1; i < h; i++) {

                    if (i == 1){
                        a = SplitColor(q, c.get(i).getSize(), q, 1);
                        for (j = 0; j < q; j++) {
                            subTrees.get(pos).add(new NumColor(c.get(i).getColor(), a[j]));
                            sortSum.put(pos, a[j]);
                            pos++;
                        }
                    }
                    else {
                        a = SplitColor(q, c.get(i).getSize(), q, 0);
                        j = 0;
                        for(Integer key : sortSum.keySet()){
                            subTrees.get(key).add(new NumColor(c.get(i).getColor(), a[j]));
                            sortSum.put(key, sortSum.get(key) + a[j]);
                            j++;
                        }
                    }
                    // order follow by values
                    sortSum.entrySet().stream()
                            .sorted(Map.Entry.<Integer, Integer>comparingByValue())
                            .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue, (e1, e2) -> e1, LinkedHashMap::new));
                }
            }
            //Case 2: 𝑐1 > q;
            else {
                int[] b, d;
                int k, w_xi, w_yi, order, c_xi, c_yi;
                c_1_prime = c.get(0).getSize() - x;
                c_2_prime = c.get(1).getSize() - y;

                //Split c_1_prime to y subtrees
                b = SplitColor(y, c_1_prime, q, 1);
                k = 0;
                for (int j = x; j < q; j++) {
                    subTrees.get(j).add(new NumColor(c.get(0).getColor(), b[k]));
                    sortSum_y.put(k, b[k]);
                    k++;
                }

                //Split c_2_prime to x subtrees
                d = SplitColor(x, c_2_prime, q, 1);
                k = 0;
                for (int j = 0; j < x; j++) {
                    subTrees.get(j).add(new NumColor(c.get(1).getColor(), d[k]));
                    sortSum_x.put(k, d[k]);
                    k++;
                }

                S_x = c_2_prime;
                S_y = c_1_prime;

                //Start from Third color to (h - 1) Color. The final color will be the rest of the size subtree - total designed previous colors
                for (int i = 2; i < (h - 1); i++) {
                    //Split c_i to q subtrees
                    double s_xi = S_x/x;
                    double s_yi = S_y/y;
                    double s_i = s_yi - s_xi;
                    double x_i = (c.get(i).getSize() + y*s_i)/q;

                    // order follow by values
                    sortSum_x.entrySet().stream()
                            .sorted(Map.Entry.<Integer, Integer>comparingByValue())
                            .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue, (e1, e2) -> e1, LinkedHashMap::new));
                    // order follow by values
                    sortSum_y.entrySet().stream()
                            .sorted(Map.Entry.<Integer, Integer>comparingByValue())
                            .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue, (e1, e2) -> e1, LinkedHashMap::new));

                    if (s_xi > s_yi) {
                        w_xi = (int) Math.ceil(x_i);
                    }
                    else {
                        w_xi = (int) Math.floor(x_i);
                    }

                    d = SplitColor(x, x * w_xi, q, 0);
                    k = 0;
                    for (Integer key : sortSum_x.keySet()) {
                        subTrees.get(key).add(new NumColor(c.get(i).getColor(), d[k]));
                        sortSum_x.put(key, sortSum_x.get(key) + d[k]);
                        k++;
                    }

                    int sum = 0;
                    for (int l = 0; l < d.length; l++) {
                        sum += d[l];
                    }

                    c_yi = c.get(i).getSize() - sum;
                    b = SplitColor(y, c_yi, q, 0);
                    k = 0;
                    for (Integer key : sortSum_y.keySet()) {
                        subTrees.get(key + x).add(new NumColor(c.get(i).getColor(), b[k]));
                        sortSum_y.put(key, sortSum_y.get(key) + b[k]);
                        k++;
                    }

                    S_x += sum;
                    S_y += c_yi;
                }
                //Divide the final Color
                for (int j = 0; j < q; j++) {
                    if (j < x)
                    {
                        subTrees.get(j).add(new NumColor(c.get(h - 1).getColor(), (int) (N_subtree - sortSum_x.get(j))));
                    }
                    else {
                        subTrees.get(j).add(new NumColor(c.get(h - 1).getColor(), (int) (N_subtree - sortSum_y.get(j - x))));
                    }
                }
            }

            for (int i = 0; i < q; i++){
                Collections.sort(subTrees.get(i));
            }

            C.addAll(subTrees);

            return C;
        }
        else {
            System.out.println("Warming! h should be greater than or equal 2");
            return null;
        }
    }

    //Splitting c colors to x subtrees satisfied (C3)
    public static int[] SplitColor(int x, long c, int q, int order) {
        int w_prime;
        int v_prime;
        int size_w_prime;
        int size_v_prime;
        int[] a = new int[x];
        int w = (int) (c / x);
        int v = (int) (c % x);
        int z = w % (q-1);

        if (z != 0) {
            w_prime = w - z + 1;
            v_prime = w_prime + q - 1;
            size_w_prime = (x * (q - z) - v) / (q - 1);
        }
        else {
            v_prime = w + 1;
            w_prime = v_prime - q + 1;
            size_w_prime = (x - v) / (q - 1);
        }
        size_v_prime = x - size_w_prime;

        //non-decreasing order
        if (order == 1) {
            for (int i = 0; i < size_w_prime; i++){
                a[i] = w_prime;
            }
            for (int i = size_w_prime; i < x; i++){
                a[i] = v_prime;
            }
        }
        //non-increasing order
        else {
            for (int i = 0; i < size_v_prime; i++){
                a[i] = v_prime;
            }
            for (int i = size_v_prime; i < x; i++){
                a[i] = w_prime;
            }
        }

        return a;
    }

    //Finding x and y where x + y = q.
    public int Finding_x(int c1, int c2, int c3, int q){
        double c_meanx_3 = 0.0, c_meany_3 = 0.0;
        double s_x3, s_y3, s_3;
        int y, S_x, S_y;
        int a = (int) Math.ceil((q*q - c1)/(q - 1));
        int b = (int) Math.floor((c2 - q)/ (q -1));

        int max = Math.max(a, 1);
        int min = Math.min(b, q - 1);

        if (max == min) {
            return min;
        }
        else {
            // Loop common elements between [a, b] and [1, q - 1]
            for (int x = max; x <= min; x++) {
                y = q - x;
                S_x = c2 - y;
                S_y = c1 - x;
                s_x3 = S_x/x;
                s_y3 = S_y/y;
                s_3 = s_y3 - s_x3;
                c_meanx_3 = (c3 + y*s_3)/q;
                c_meany_3 = (c3 - x*s_3)/q;
                if (c_meanx_3 >= q && c_meany_3 >= q) {
                    return x;
                }
            }
        }
	return 0;
    }

    //Definition (Feasible Color Sequence). A color sequence 𝑐 of dimension ℎ is called
    //"ℎ-feasible" if after being sorted in a non-decreasing order (so that 𝑐1 ≤ 𝑐2 ≤ · · · ≤ 𝑐ℎ), it satisfies
    //the following three conditions: (C1), (C2), and (C3)
    public boolean isFeasible(byte h, int q, List<NumColor> c) {
        for (byte m = h; m > 0; m--) {
            int sum;
            sum = getTotalColorSize(m, c);
            //check (C2)
            if (m == h && sum != q*((int) Math.pow(q,m)-1)/(q-1)) {
                System.out.println("\n" + " ***** WARNING! *****");
                System.out.println("The color sequence is NOT feasible");
                System.out.println("Conflict with C2: The total size of 𝑐 is equal to the number of nodes in 𝑇 (ℎ)");
                return false;
            }
            //check (C1)
            if (sum < q*((int) Math.pow(q,m)-1)/(q-1)) {
                System.out.println("\n" + " ***** WARNING! *****");
                System.out.println("The color sequence is NOT feasible");
                System.out.println("Conflict with C1: Colors 1, 2, . . . , ℓ can be used to color all nodes in Layers 1, 2, . . . , ℓ of the perfect binary tree 𝑇 (ℎ)");
                return false;
            }
        }
        if (q != 2){
            //check (C3)
            for (byte i = 0; i < h; i++) {
                if(c.get(i).getSize()%(q-1) != 1){
                    System.out.println("\n" + " ***** WARNING! *****");
                    System.out.println("The color sequence is NOT feasible");
                    System.out.println("Conflict with C3");
                    return false;
                }
            }
        }

        return true;
    }

    //return the list of all feasible sequences
    public ArrayList<ArrayList<NumColor>> feasibleConfList(byte h, int q){
        int m = 0;  //the current position of c to be filled in
        ArrayList<NumColor> c = new ArrayList<>(h);
        ArrayList<ArrayList<NumColor>> F = new ArrayList<>();

        feasibleConfListRecursive(F, c, m, h, q);

        //test feasibility of sequences in F
        for (ArrayList<NumColor> numColors : F) {
            if (!isFeasible(h, q, numColors)) {
                System.out.println("c = " + numColors + " is NOT feasible \n");
                return null;
            }
        }
        return F;
    }

    //given c = [c_0,...,c_(h-1)], try all possibilities for c_i that still guarantees feasibility
    public void feasibleConfListRecursive(ArrayList<ArrayList<NumColor>> F, ArrayList<NumColor>  c, int m, byte h, int q){
        char[] color = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q'
                , 'R','S', 'T', 'U', 'V','W', 'X', 'Y', 'Z','0', '1', '2', '3', '4', '5', '6', '7','8', '9'};

        //if we have filled c then add c to the list F
        if (m == h) {
            ArrayList<NumColor> conf = new ArrayList<>(h);
            for (int i = 0; i < h; i++) conf.add(i, new NumColor(color[i], c.get(i).getSize()));
            F.add(conf);
            if (!isFeasible(h, q, conf)) System.out.println("INFEASIBLE");
            return;
        }

        int current_sum = 0;
        int sum = q*((int) Math.pow(q,h)-1)/(q-1);

        for (int i = 0; i <= m-1; i++) {
            current_sum += c.get(i).getSize();
        }

        int remaining_sum = sum-current_sum;
        int upper = (int) Math.floor(remaining_sum/(h-m)); //largest possible value for c_m
        int lower = (m==0)? q : (int) Math.max(c.get(m-1).getSize(), q*((int) Math.pow(q,m+1)-1)/(q-1) - current_sum); //smallest possible value for c_m

        for (int cm = lower; cm <= upper; cm += (q - 1)) {
            if (c.size() <= m) {
                c.add(m, new NumColor(color[m], cm));
            }
            else c.set(m, new NumColor(color[m], cm));
            feasibleConfListRecursive(F, c, m+1, h, q);
        }
    }

    //Print the list of all feasible sequences
    public void printAllFeasibleSeqs(ArrayList<ArrayList<NumColor>> F) {
        for (ArrayList<NumColor> numColors : F) {
            for (NumColor numColor : numColors) System.out.print(numColor.getSize() + " ");
            System.out.println();
        }
    }

    //Sum all color values
    public int getTotalColorSize(byte m, List<NumColor> c) {
        if (0 < m && m <= c.size()) {
            int sum = 0;
            for (byte i = 0; i < m; i++) {
                sum += c.get(i).getSize();
            }
            return sum;
        }
        else {
            System.out.println("Warming! m should be positive and less than or equal h");
            return 0;
        }
    }
}

//-----------------------------------------Find Sub-Indices class---------------------------------------------------------------
class SubIndices {
    private byte h; //h is the height of a tree
    private int q; //q is the number of children of a non-leaf node
    private long j; //a leaf index

    List<List<NumColor>> C = new ArrayList<>();

    public SubIndices(byte h, int q, long j) {
        this.h = h;
        this.q = q;
        this.j = j;
    }

    //Finding the path from root to leaf
    public int[] Path() {
        int[] path = new int[h];
        long[] path_nodeID = new long[h];
        int temp;

        temp = (int) (j % q);

        if (temp == 0) {
            path[h - 1] = q;
        }
        else {
            path[h - 1] = temp;
        }

        path_nodeID[h - 1] = first_nodeID(h) + j - 1;
        //Node ID from bottom to top
        for (byte i = (byte) (h - 2); i >= 0; i--) {
            path_nodeID[i] = (long) Math.ceil((double)(path_nodeID[i + 1] - 1)/q);
        }
        //Path position from top to bottom
        for (byte i = 0; i < h ; i++) {
            temp = (int) (((path_nodeID[i] - first_nodeID((i + 1)) + 1)) % q);

            if (temp == 0) {
                path[i] = q;
            }
            else {
                path[i] = temp;
            }
        }
        return path;
    }

    //Finding the path node IDs from root to leaf
    public long[] PathID() {
        long[] path_nodeID = new long[h];

        path_nodeID[h - 1] = first_nodeID(h) + j - 1;
        //Node ID from bottom to top
        for (byte i = (byte) (h - 2); i >= 0; i--) {
            path_nodeID[i] = (long) Math.ceil((double)(path_nodeID[i + 1] - 1)/q);
        }
        return path_nodeID;
    }

    //
    public int[] Indices(int[] path, long[] pathID, List<NumColor> c) {
        int[] count = new int[h];
        int[] indices = new int[h];
        int x = q;
        byte height;
        char root_col;

        for (byte l = 0; l < h - 1; l++) {
            height = (byte) (h - l);

            if (height > 0) {
                //Assign Color 1 to all children;
                if (c.get(0).getSize() == q) {
                    x = q;
                }
                //Finding x where we will assign Color 1 to x children and Color 2 to y children (x + y = q).
                else if (c.get(0).getSize() > q) {
                    if (height > 2) x = Finding_x(c.get(0).getSize(), c.get(1).getSize(), c.get(2).getSize());
                    else if (height > 1) x = Finding_x(c.get(0).getSize(), c.get(1).getSize(), 0);
                    else x = Finding_x(c.get(0).getSize(), 0, 0);
                }

                //Split the feasible sequence c to q feasible sequences for q sub-trees.
                if (height > 1) {
                    //If the recent root node color by the first or second color of the recent sequence c, the below its color will be 0
                    if (path[l] <= x) {
                        root_col = c.get(0).getColor();
                        count[find_color(c.get(0).getColor())] += path[l] - 1;
                        count[find_color(c.get(1).getColor())] += q - x;
                    }
                    else {
                        root_col = c.get(1).getColor();
                        count[find_color(c.get(1).getColor())] += path[l] - x - 1;
                        count[find_color(c.get(0).getColor())] += x;
                    }

                    C = FeasibleSplit(height, x, c);

                    for (int i = 0; i < path[l] - 1; i ++) {
                        for (int j = 0; j < height - 1; j++) {
                            if (root_col != C.get(i).get(j).getColor()) {
                                count[find_color(C.get(i).get(j).getColor())] += C.get(i).get(j).getSize();
                            }
                        }
                    }

                    c = C.get(path[l] - 1);
                    if (c.size() == 1) {
                        //root_col = c.get(0).getColor();
                        count[find_color(c.get(0).getColor())] += path[path.length - 1] - 1;
                    }
                }
            }
        }

        for (int i = 0; i < h; i++) {
            indices[i] = count[i] + 1;
            //System.out.println("indices[i] = " + indices[i]);
        }

        return indices;
    }

    public LinkedHashMap<Character, Integer> mapIndices(int[] path, long[] pathID, List<NumColor> c) {
        LinkedHashMap<Character, Integer> map = new LinkedHashMap<>();
        int[] count = new int[h];
        int x = q;
        byte height;
        char root_col;

        for (byte l = 0; l < h - 1; l++) {
            height = (byte) (h - l);

            if (height > 0) {
                //Assign Color 1 to all children;
                if (c.get(0).getSize() == q) {
                    x = q;
                }
                //Finding x where we will assign Color 1 to x children and Color 2 to y children (x + y = q).
                else if (c.get(0).getSize() > q) {
                    if (height > 2) x = Finding_x(c.get(0).getSize(), c.get(1).getSize(), c.get(2).getSize());
                    else if (height > 1) x = Finding_x(c.get(0).getSize(), c.get(1).getSize(), 0);
                    else x = Finding_x(c.get(0).getSize(), 0, 0);
                }

                //Split the feasible sequence c to q feasible sequences for q sub-trees.
                if (height > 1) {
                    //If the recent root node color by the first or second color of the recent sequence c, the below its color will be 0
                    if (path[l] <= x) {
                        root_col = c.get(0).getColor();
                        count[find_color(c.get(0).getColor())] += path[l] - 1;
                        count[find_color(c.get(1).getColor())] += q - x;
                        map.put(c.get(0).getColor(), count[find_color(c.get(0).getColor())]);
                    }
                    else {
                        root_col = c.get(1).getColor();
                        count[find_color(c.get(1).getColor())] += path[l] - x - 1;
                        count[find_color(c.get(0).getColor())] += x;
                        map.put(c.get(1).getColor(), count[find_color(c.get(1).getColor())]);
                    }

                    C = FeasibleSplit(height, x, c);

                    for (int i = 0; i < path[l] - 1; i ++) {
                        for (int j = 0; j < height - 1; j++) {
                            if (root_col != C.get(i).get(j).getColor()) {
                                count[find_color(C.get(i).get(j).getColor())] += C.get(i).get(j).getSize();
                            }
                        }
                    }

                    c = C.get(path[l] - 1);
                    if (c.size() == 1) {
                        count[find_color(c.get(0).getColor())] += path[path.length - 1] - 1;
                        map.put(c.get(0).getColor(), count[find_color(c.get(0).getColor())]);
                    }
                }
            }
        }
        return map;
    }

    //Finding first node ID in a specific layer
    public long first_nodeID(int l) {
        return (long) (Math.pow(q, l) - 1) / (q - 1) + 1;
    }

    //Finding final node ID in a specific layer
    public long final_nodeID(int l) {
        return (long) (Math.pow(q, l + 1) - 1) / (q - 1);
    }

    //Finding position of a character in a character array.
    public int find_color(char target){
        int pos = -1;
        char[] color = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q'
                , 'R','S', 'T', 'U', 'V','W', 'X', 'Y', 'Z','0', '1', '2', '3', '4', '5', '6', '7','8', '9'};

        for (int i = 0; i < color.length; i++) {
            if (color[i] == target) {
                pos = i;
                break; // Exit loop once the target is found
            }
        }
        return pos;
    }

    /* This algorithm splits a ℎ-feasible sequence into q (ℎ − 1)-feasible ones, which will be used for coloring the subtrees; only works when ℎ ≥ 2.
    Note that the splitting rule (see FeasibleSplit(h, q, x, c)) ensures that if Color 𝑖 is used for a node then it will no longer be used in the subtree rooted at that node,
    hence guaranteeing the Ancestral Property.*/
    public List<List<NumColor>> FeasibleSplit(byte h, int x, List<NumColor> c) {
        C.clear();
        int y = q - x;
        int c_1_prime, c_2_prime;
        int S_x = 0, S_y = 0;
        List<List<NumColor>> subTrees = new ArrayList<>(q);

        for (int i = 0; i < q; i++) {
            subTrees.add(i, new ArrayList<>(h - 1));
        }

        if (h == 2) {
            if (c.get(0).getSize() == q) {
                for (int i = 0; i < q; i++){
                    subTrees.get(i).add(new NumColor(c.get(1).getColor(), c.get(1).getSize() / q));
                }
            }
            else {
                for (int i = 0; i < q; i++){
                    if (i < x){
                        subTrees.get(i).add(new NumColor(c.get(1).getColor(), (c.get(1).getSize() - (q - x)) / x));
                    }
                    else {
                        subTrees.get(i).add(new NumColor(c.get(0).getColor(), (c.get(0).getSize() - x) / y));
                    }
                }
            }

            for (int j = 0; j < q; j++){
                Collections.sort(subTrees.get(j));
            }

            C.addAll(subTrees);
            return C;
        }
        else if (h > 2) {
            long N_subtree = (long) ((long) q*(Math.pow(q,h - 1)-1)/(q-1)); //subtree size = # nodes in each subtree except the root node
            HashMap<Integer, Integer> sortSum = new HashMap<Integer, Integer> (); //key = pos; value = recent sum
            HashMap<Integer, Integer> sortSum_x = new HashMap<Integer, Integer> (); //key = pos; value = recent sum
            HashMap<Integer, Integer> sortSum_y = new HashMap<Integer, Integer> (); //key = pos; value = recent sum

            //Case 1: 𝑐1 = q
            if (c.get(0).getSize() == q) {
                int[] a;
                int pos = 0; //position subtrees;
                int j;

                //Split c_i to q subtrees
                for (int i = 1; i < h; i++) {

                    if (i == 1){
                        a = SplitColor(q, c.get(i).getSize(), 1);
                        for (j = 0; j < q; j++) {
                            subTrees.get(pos).add(new NumColor(c.get(i).getColor(), a[j]));
                            sortSum.put(pos, a[j]);
                            pos++;
                        }
                    }
                    else {
                        a = SplitColor(q, c.get(i).getSize(), 0);
                        j = 0;
                        for(Integer key : sortSum.keySet()){
                            subTrees.get(key).add(new NumColor(c.get(i).getColor(), a[j]));
                            sortSum.put(key, sortSum.get(key) + a[j]);
                            j++;
                        }
                    }
                    // order follow by values
                    sortSum.entrySet().stream()
                            .sorted(Map.Entry.<Integer, Integer>comparingByValue())
                            .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue, (e1, e2) -> e1, LinkedHashMap::new));
                }
            }
            //Case 2: 𝑐1 > q;
            else {
                int[] b, d;
                int k, w_xi, w_yi, order, c_xi, c_yi;
                c_1_prime = c.get(0).getSize() - x;
                c_2_prime = c.get(1).getSize() - y;

                //Split c_1_prime to y subtrees
                b = SplitColor(y, c_1_prime, 1);
                k = 0;
                for (int j = x; j < q; j++) {
                    subTrees.get(j).add(new NumColor(c.get(0).getColor(), b[k]));
                    sortSum_y.put(k, b[k]);
                    k++;
                }

                //Split c_2_prime to x subtrees
                d = SplitColor(x, c_2_prime, 1);
                k = 0;
                for (int j = 0; j < x; j++) {
                    subTrees.get(j).add(new NumColor(c.get(1).getColor(), d[k]));
                    sortSum_x.put(k, d[k]);
                    k++;
                }

                S_x = c_2_prime;
                S_y = c_1_prime;

                //Start from Third color to (h - 1) Color. The final color will be the rest of the size subtree - total designed previous colors
                for (int i = 2; i < (h - 1); i++) {
                    //Split c_i to q subtrees
                    double s_xi = S_x/x;
                    double s_yi = S_y/y;
                    double s_i = s_yi - s_xi;
                    double x_i = (c.get(i).getSize() + y*s_i)/q;

                    // order follow by values
                    sortSum_x.entrySet().stream()
                            .sorted(Map.Entry.<Integer, Integer>comparingByValue())
                            .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue, (e1, e2) -> e1, LinkedHashMap::new));
                    // order follow by values
                    sortSum_y.entrySet().stream()
                            .sorted(Map.Entry.<Integer, Integer>comparingByValue())
                            .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue, (e1, e2) -> e1, LinkedHashMap::new));

                    if (s_xi > s_yi) {
                        w_xi = (int) Math.ceil(x_i);
                    }
                    else {
                        w_xi = (int) Math.floor(x_i);
                    }

                    d = SplitColor(x, x * w_xi, 0);
                    k = 0;
                    for (Integer key : sortSum_x.keySet()) {
                        subTrees.get(key).add(new NumColor(c.get(i).getColor(), d[k]));
                        sortSum_x.put(key, sortSum_x.get(key) + d[k]);
                        k++;
                    }

                    int sum = 0;
                    for (int l = 0; l < d.length; l++) {
                        sum += d[l];
                    }

                    c_yi = c.get(i).getSize() - sum;
                    b = SplitColor(y, c_yi, 0);
                    k = 0;
                    for (Integer key : sortSum_y.keySet()) {
                        subTrees.get(key + x).add(new NumColor(c.get(i).getColor(), b[k]));
                        sortSum_y.put(key, sortSum_y.get(key) + b[k]);
                        k++;
                    }

                    S_x += sum;
                    S_y += c_yi;
                }
                //Divide the final Color
                for (int j = 0; j < q; j++) {
                    if (j < x)
                    {
                        subTrees.get(j).add(new NumColor(c.get(h - 1).getColor(), (int) (N_subtree - sortSum_x.get(j))));
                    }
                    else {
                        subTrees.get(j).add(new NumColor(c.get(h - 1).getColor(), (int) (N_subtree - sortSum_y.get(j - x))));
                    }
                }
            }

            for (int i = 0; i < q; i++){
                Collections.sort(subTrees.get(i));
            }

            C.addAll(subTrees);

            return C;
        }
        else {
            System.out.println("Warming! h should be greater than or equal 2");
            return null;
        }
    }

    //Splitting c colors to x subtrees satisfied (C3)
    public int[] SplitColor(int x, long c, int order) {
        int w_prime;
        int v_prime;
        int size_w_prime;
        int size_v_prime;
        int[] a = new int[x];
        int w = (int) (c / x);
        int v = (int) (c % x);
        int z = w % (q-1);

        if (z != 0) {
            w_prime = w - z + 1;
            v_prime = w_prime + q - 1;
            size_w_prime = (x * (q - z) - v) / (q - 1);
        }
        else {
            v_prime = w + 1;
            w_prime = v_prime - q + 1;
            size_w_prime = (x - v) / (q - 1);
        }
        size_v_prime = x - size_w_prime;

        //non-decreasing order
        if (order == 1) {
            for (int i = 0; i < size_w_prime; i++){
                a[i] = w_prime;
            }
            for (int i = size_w_prime; i < x; i++){
                a[i] = v_prime;
            }
        }
        //non-increasing order
        else {
            for (int i = 0; i < size_v_prime; i++){
                a[i] = v_prime;
            }
            for (int i = size_v_prime; i < x; i++){
                a[i] = w_prime;
            }
        }

        return a;
    }

    //Finding x and y where x + y = q.
    public int Finding_x(int c1, int c2, int c3){
        double c_meanx_3 = 0.0, c_meany_3 = 0.0;
        double s_x3, s_y3, s_3;
        int y, S_x, S_y;
        int a = (int) Math.ceil((q*q - c1)/(q - 1));
        int b = (int) Math.floor((c2 - q)/ (q -1));

        int max = Math.max(a, 1);
        int min = Math.min(b, q - 1);

        if (max == min) {
            return min;
        }
        else {
            // Loop common elements between [a, b] and [1, q - 1]
            for (int x = max; x <= min; x++) {
                y = q - x;
                S_x = c2 - y;
                S_y = c1 - x;
                s_x3 = S_x/x;
                s_y3 = S_y/y;
                s_3 = s_y3 - s_x3;
                c_meanx_3 = (c3 + y*s_3)/q;
                c_meany_3 = (c3 - x*s_3)/q;
                if (c_meanx_3 >= q && c_meany_3 >= q) {
                    return x;
                }
            }
        }
        return 0;
    }
}

//-----------------------------------------Set of Nodes have the same color class------------------------------------------------------------
//Each set will contain all node with the same color
class NodesSet {
    private int count = 0;
    private final char colorSet;
    private final int [] addNodes; //Array of node IDs (R)

    public NodesSet(char colorSet, int size) {
        this.colorSet = colorSet;
        addNodes = new int [size];
    }

    public void addNode(int root) {
        //array start from 0, whereas node colored start from 2
        addNodes[count] = root;
        count++;
    }

    public int [] getAddNodes() {
        return addNodes;
    }

    public char getColorSet() {
        return colorSet;
    }

    public int getSize() {
        return count;
    }

    @Override
    public String toString() {
        StringBuilder roots = new StringBuilder();
        for (int addNode : addNodes) {
            roots.append(addNode).append(" ");
        }

        return roots.toString();
    }
}

//-----------------------------------------NumColor class---------------------------------------------------------------
//Stored and Sorted vector c.
class NumColor implements Comparable<NumColor> {
    private final int size;
    private final char color;

    public NumColor(char color, int size) {
        this.color = color;
        this.size = size;
    }

    public char getColor() {
        return color;
    }

    public int getSize() {
        return size;
    }

    @Override
    public int compareTo(NumColor otherNumColor) {
        return Integer.compare(getSize(), otherNumColor.getSize());
    }
}
