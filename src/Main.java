import java.util.*;

public class Main {
    private static final int[][] DIRECTIONS = {{-1, 0}, {0, 1}, {1, 0}, {0, -1}}; //up,right,down,left

    public static void main(String[] args) throws Exception {
        try{
            AstarAlgorithm();
        }catch(OutOfMemoryError e){
            throw new Exception("Out of memory. Available memory is not enough to solve this problem");
        }

    }

    //Υλοποίηση αλγορίθμου Α*
    private static void AstarAlgorithm(){

        char[][] level = {};

        Scanner sc = new Scanner(System.in);

        System.out.println("Choose the level you want: 0(very easy) 1(easy) 2(medium) 3(hard) 4(very hard) 5(No solution case)");
        System.out.println("Levels 0-4 have solutions, 5th doesn't");

        int choice = sc.nextInt();
        if (choice == 0) {
            level = new char[][]{
                    {'#', '#', '#', '#', '#', '#', '#', '#', '#', '#'},
                    {' ', '#', ' ', ' ', ' ', '#', '#', '#', '#', '#'},
                    {'#', '#', '*', '#', ' ', '#', '#', '#', '#', '#'},
                    {'#', ' ', '*', '$', ' ', '*', ' ', ' ', ' ', '#'},
                    {'#', ' ', ' ', ' ', '0', ' ', '1', ' ', ' ', '#'},
                    {'#', '#', '#', ' ', ' ', '#', ' ', '#', '#', '#'},
                    {'#', ' ', '#', '#', ' ', ' ', ' ', '#', '#', '#'},
                    {'#', '#', '#', '#', '#', '#', '#', '#', '#', '#'}
            };
        } else if (choice == 1) {
            level = new char[][]{
                    {'#', '#', '#', '#', '#', '#', '#', '#'},
                    {'#', ' ', ' ', ' ', ' ', ' ', ' ', '#'},
                    {'#', ' ', '0', ' ', '*', ' ', '$', '#'},
                    {'#', ' ', ' ', ' ', ' ', ' ', ' ', '#'},
                    {'#', ' ', '*', ' ', ' ', ' ', ' ', '#'},
                    {'#', ' ', ' ', ' ', ' ', ' ', '1', '#'},
                    {'#', ' ', ' ', ' ', ' ', ' ', ' ', '#'},
                    {'#', '#', '#', '#', '#', '#', '#', '#'}
            };
        } else if (choice == 2) {
            level = new char[][]{
                    {'#','#','#','#','#',' ',' ',' ',' ',' '},
                    {' ','#',' ',' ',' ','#',' ',' ',' ',' '},
                    {'#','#','*','#',' ','#','#','#','#','#'},
                    {'#',' ','*',' ','0',' ','*',' ',' ','#'},
                    {'#',' ',' ',' ',' ','$',' ','1',' ','#'},
                    {'#','#','#',' ',' ','#','*','#','#','#'},
                    {' ',' ','#','#',' ',' ',' ','#',' ',' '},
                    {' ',' ',' ','#','#','#','#','#','#','#'}
            };


        } else if (choice == 3) {
            level = new char[][]{
                    {' ','#','#','#','#',' ',' ',' ',' ',' '},
                    {' ','#',' ',' ','#','#','#','#','#','#'},
                    {' ','#',' ',' ',' ',' ',' ',' ',' ','#'},
                    {'#','#',' ','#',' ','#','$','0',' ','#'},
                    {'#',' ',' ','*',' ','#','#',' ','#','#'},
                    {'#',' ','*','*',' ','#',' ','1','#'},
                    {'#','#','#',' ',' ',' ','*',' ','#'},
                    {' ',' ','#','#','#','#',' ',' ','#'},
                    {' ',' ',' ',' ',' ','#','#','#','#'}
            };

        } else if (choice == 4) {
            level = new char[][]{
                    {' ', '#', '#', '#', '#', '#', '#', '#', ' ', ' '},
                    {' ', '#', ' ', ' ', '#', ' ', ' ', '#', '#', '#'},
                    {' ', '#', '0', ' ', ' ', ' ', '0', ' ', ' ', '#'},
                    {' ', '#', ' ', '$', '#', '*', '*', ' ', ' ', '#'},
                    {'#', '#', ' ', '#', '1', ' ', '#', ' ', '#', '#'},
                    {'#', ' ', ' ', '$', '$', '#', '$', ' ', '#', ' '},
                    {'#', ' ', '0', ' ', ' ', ' ', '0', ' ', '#', ' '},
                    {'#', '#', '#', '#', '#', '#', ' ', ' ', ' ', '#'},
                    {' ', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#'}

            };
        }else if(choice == 5){
            level = new char[][]{
                    {'#', '#', '#', '#', '#', '#', '#', '#', '#', '#'},
                    {'#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'},
                    {'#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'},
                    {'#', ' ', ' ', ' ', ' ', '#', ' ', '0', ' ', '#'},
                    {'#', ' ', ' ', ' ', '$', ' ', '0', '$', ' ', '#'},
                    {'#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'},
                    {'#', ' ', ' ', '1', ' ', ' ', ' ', ' ', ' ', '#'},
                    {'#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'},
                    {'#', ' ', ' ', ' ', '0', ' ', '#', ' ', '$', '#'},
                    {'#', '#', '#', '#', '#', '#', '#', '#', '#', '#'}
            };
        }


        level = makeRectangularWithBorder(level);


        System.out.println("Searching for a solution...");

        int countBox = 0;
        int countGoals = 0;
        int countPerson = 0;
        for (char[] chars : level) {
            for (int j = 0; j < level[0].length; j++) {
                if (chars[j] == '0') countBox++;
                if (chars[j] == '$') countGoals++;
                if(chars[j] == '1') countPerson++;
            }
        }
        if (countBox != countGoals) {
            System.out.println("Boxes and Goals can't match,\nNumber of free boxes at the map: " + countBox + "\n" + "Number of free goals at the map: " + countGoals);
            return;
        }

            if (countPerson > 1) {
                throw new ArrayIndexOutOfBoundsException("There is are more than 1 player on board");
            } else if (countPerson == 0) {
                throw new ArrayIndexOutOfBoundsException("There is no player on board");
            }


        int[] startP = findPlayer(level);
        Node start = new Node(copyGrid(level), startP[0], startP[1], null, 0, heuristic(level));

        PriorityQueue<Node> open = new PriorityQueue<>(Comparator.comparingInt(n -> n.f)); //μέτωπο. Προταιρεότητα στην μικρότερη f
        Set<Node> visited = new HashSet<>();    //κλειστό σύνολο

        open.add(start);
        visited.add(start);

        long startTime = System.currentTimeMillis();
            while (!open.isEmpty()) {
                Node current = open.poll();

                if (isGoal(current)) {
                    if (noMoneyOrBox(current.grid)) {
                        printSolutionPath(current);
                        System.out.println("Solution found! timeMs=" + (System.currentTimeMillis() - startTime));
                    } else {
                        continue;
                    }
                    return;
                }

                for (int dir = 0; dir < DIRECTIONS.length; dir++) {
                    int newR = current.playerRow + DIRECTIONS[dir][0];
                    int newC = current.playerCol + DIRECTIONS[dir][1];

                    if (!isValidMove(newR, newC, current.grid, dir)) continue;
                    if (isDeadlock(newR, newC, current.grid, dir)) continue;

                    char[][] newGrid = updateGrid(newR, newC, copyGrid(current.grid), dir);
                    Node child = new Node(newGrid, newR, newC, current, current.g + 1, heuristic(newGrid));

                    if (!visited.contains(child)) {
                        visited.add(child);
                        open.add(child);
                    }
                }
            }
            System.out.println("Not possible to find solution. Time: " + (System.currentTimeMillis() - startTime) + " ms");
    }

//-------------------------------------------
//βασικές μέθοδοι

    //ανίχνευση αν η κίνηση του παίχτη επιτρέπεται ή όχι
    private static boolean isValidMove(int row, int col, char[][] board, int direction) {
        //Έλεγχος ορίων γραμμής
        if (row < 0 || row >= board.length) return false;

        //Έλεγχος ορίων στήλης για αυτή τη γραμμή
        if (col < 0 || col >= board[row].length) return false;

        char targetCell = board[row][col];

        if (targetCell == '#') return false;

        if (targetCell == '0' || targetCell == '*') {
            int nextRow = row + DIRECTIONS[direction][0];
            int nextCol = col + DIRECTIONS[direction][1];

            //Έλεγχος ορίων για τη γραμμή του κουτιού
            if (nextRow < 0 || nextRow >= board.length) return false;

            //Έλεγχος αν η στήλη υπάρχει στη γραμμή του κουτιού
            if (nextCol < 0 || nextCol >= board[nextRow].length) return false;

            char afterBox = board[nextRow][nextCol];

            return afterBox != '#' && afterBox != '0' && afterBox != '*';
        }

        return true;
    }


    //Κίνηση παίχτη και update το board
    private static char[][] updateGrid(int newRow, int newCol, char[][] grid, int direction) {

        int oldRow = newRow - DIRECTIONS[direction][0];
        int oldCol = newCol - DIRECTIONS[direction][1];

        //Έλεγχος ορίων
        if (oldRow < 0 || oldRow >= grid.length || oldCol < 0 || oldCol >= grid[0].length) {
            return grid;
        }

        char oldTile = grid[oldRow][oldCol];
        char targetTile = grid[newRow][newCol];

        //Υπολογισμός τι αφήνει πίσω ο παίκτης
        if (oldTile == '+') {
            grid[oldRow][oldCol] = '$';
        } else {
            grid[oldRow][oldCol] = ' ';
        }

        //Αν ο παίκτης πάει σε κενό ή στόχο
        if (targetTile == ' ' || targetTile == '$') {
            if (targetTile == '$') {
                grid[newRow][newCol] = '+';
            } else {
                grid[newRow][newCol] = '1';
            }
            return grid;
        }

        //Αν ο παίκτης πάει να σπρώξει κουτί
        if (targetTile == '0' || targetTile == '*') {
            int boxNewRow = newRow + DIRECTIONS[direction][0];
            int boxNewCol = newCol + DIRECTIONS[direction][1];

            //Έλεγχος ορίων
            if (boxNewRow < 0 || boxNewRow >= grid.length || boxNewCol < 0 || boxNewCol >= grid[0].length) {
                return grid;
            }

            char afterBoxTile = grid[boxNewRow][boxNewCol];

            //Αν υπάρχει χώρος για να μετακινηθεί το κουτί
            if (afterBoxTile == ' ' || afterBoxTile == '$') {

                //Μετακίνησε το κουτί
                if (afterBoxTile == '$') {
                    grid[boxNewRow][boxNewCol] = '*';
                } else {
                    grid[boxNewRow][boxNewCol] = '0';
                }

                //Παίκτης μετακινείται στη θέση του κουτιού
                if (targetTile == '*') {
                    grid[newRow][newCol] = '+';
                } else {
                    grid[newRow][newCol] = '1';
                }

                return grid;
            }
        }

        if (oldTile == '+') {
            grid[oldRow][oldCol] = '+';
        } else {
            grid[oldRow][oldCol] = '1';
        }

        return grid;
    }

    //έλεγχος αν μια κίνηση είναι deadlock
    private static boolean isDeadlock(int row, int col, char[][] board, int counter) {

        for (int i = 0; i < board.length; i++) {
            for (int j = 0; j < board[0].length; j++) {

                if (i <= 0 || i >= board.length - 1 || j <= 0 || j >= board[0].length - 1) {
                    continue;
                }


                if (board[i][j] != '0') continue;
                if (board[i][j] == '*') continue;

                if (board[i][j] == '0') {

                    //Corridor deadlock check
                    if (isCorridorDeadlock(i, j, board)) {
                        return true;
                    }

                    List<int[]> wallDirections = checkFourDirections(i, j, board);

                    if (wallDirections.isEmpty()) {
                        continue;

                    } else if (wallDirections.size() == 2) {
                        if (isItCorner(board, i, j) && board[i][j] != '$') {
                            return true;
                        }

                    } else if (wallDirections.size() > 2) {
                        return true;
                    } else {
                        int[] coordinates = wallDirections.getFirst();
                        int identifier = coordinates[0];
                        boolean targetExistsUp = false;
                        boolean targetExistsdown = false;


                        if (identifier == 1) {//column case
                            boolean UpBlocked = false;
                            boolean downBlocked = false;

                            //scan row to left
                            for (int k = j; k >= 0; k--) {
                                if (board[i][k] == '#') {
                                    UpBlocked = true;
                                    break;
                                }
                                if (board[i][k] == '$') {
                                    targetExistsUp = true;
                                    break;
                                }
                            }

                            //scan row to right
                            for (int k = j; k < board[0].length; k++) {
                                if (board[i][k] == '#') {
                                    downBlocked = true;
                                    break;
                                }
                                if (board[i][k] == '$') {
                                    targetExistsdown = true;
                                    break;
                                }
                            }

                            boolean fullWalls = true;
                            for (int k = 0; k < board[0].length; k++) {
                                if (board[i][k] != '#') {
                                    fullWalls = false;
                                    break;
                                }
                            }

                            if (!targetExistsUp && !targetExistsdown && downBlocked && UpBlocked) {
                                if (fullWalls) {
                                    return true;
                                }
                            }

                        } else if (identifier == 0) {//row case
                            boolean leftBlocked = false;
                            boolean rightBlocked = false;
                            boolean targetExistsleft = false;
                            boolean targetExistsright = false;

                            //scan column left
                            for (int k = i; k >= 0; k--) {
                                if (board[k][j] == '#') {
                                    leftBlocked = true;
                                    break;
                                }
                                if (board[k][j] == '$') {
                                    targetExistsleft = true;
                                    break;
                                }
                            }
                            boolean fullWalls = true;
                            for (char[] chars : board) {
                                if (chars[j] != '#') {
                                    fullWalls = false;
                                    break;
                                }
                            }

                            //scan column right
                            for (int k = i; k < board.length; k++) {
                                if (board[k][j] == '#') {
                                    rightBlocked = true;
                                    break;
                                }
                                if (board[k][j] == '$') {
                                    targetExistsright = true;
                                    break;
                                }
                            }

                            if (!targetExistsright && rightBlocked && !targetExistsleft && leftBlocked) {
                                if (fullWalls) {
                                    return true;
                                }
                            }
                        }
                    }
                }
            }

        }
        return false;
    }


//-----------------------------------------------------------------------------
//Βοηθητικές μέθοδοι

    //deadlock περίπτωσης τούνελ
    private static boolean isCorridorDeadlock(int i, int j, char[][] board) {
        int rows = board.length;
        int cols = board[0].length;
        boolean horizontal = (j - 1 >= 0 && j + 1 < cols && board[i][j - 1] == '#' && board[i][j + 1] == '#');
        boolean vertical = (i - 1 >= 0 && i + 1 < rows && board[i - 1][j] == '#' && board[i + 1][j] == '#');

        if (!horizontal && !vertical) return false;

        int holes = 0;

        if (vertical) {
            //Έλεγχος για κουτί ή στόχο στον διαδρομο
            boolean boxExists = false;
            boolean goalExists = false;
            for (char[] value : board) {
                if (value[j] == '0') {
                    boxExists = true;
                }
                if (value[j] == '$') {
                    goalExists = true;
                }
            }
            //Έλεγχος αριστερά–δεξιά
            for (char[] chars : board) {
                if (j - 1 >= 0 && j + 1 < board[0].length) {
                    if (chars[j - 1] != '#' || chars[j + 1] != '#') {
                        holes++;
                    }
                }
            }
            return holes == 0  && !boxExists && !goalExists;
        }
        if(horizontal) {
            //Έλεγχος για κουτί ή στόχο στον διαδρομο
            boolean boxExists = false;
            boolean goalExists = false;

            for(int m = 0; m<board[0].length; m++) {
                if(board[i][m] == '0') {
                    boxExists = true;
                }
                if(board[i][m] == '$') {
                    goalExists = true;
                }
            }
            //Έλεγχος πάνω–κάτω
            for (int c = 0; c < board[0].length; c++) {
                if (i - 1 >= 0 && i + 1 < board.length) {
                    if (board[i - 1][c] != '#' || board[i + 1][c] != '#') {
                        holes++;
                    }
                }
            }
            return holes == 0 &&  !boxExists && !goalExists;
        }

        //Έλεγχος πάνω–κάτω (τρύπες σε ίδιες στήλες)
        for (int c = 0; c < board[0].length; c++) {
            if (i - 1 >= 0 && i + 1 < board.length) {
                if (board[i - 1][c] != '#' && board[i + 1][c] != '#') {
                    holes++;
                }
            }
        }
        return holes < 1;

    }


    private static boolean isItCorner(char[][] board, int i, int j) {
        int rows = board.length;
        int cols = board[0].length;
        boolean isCorner = false;

        //check boundaries before each access
        if (i - 1 >= 0 && j - 1 >= 0 && board[i - 1][j] == '#' && board[i][j - 1] == '#') {
            isCorner = true;
        } else if (i - 1 >= 0 && j + 1 < cols && board[i - 1][j] == '#' && board[i][j + 1] == '#') {
            isCorner = true;
        } else if (i + 1 < rows && j - 1 >= 0 && board[i + 1][j] == '#' && board[i][j - 1] == '#') {
            isCorner = true;
        } else if (i + 1 < rows && j + 1 < cols && board[i + 1][j] == '#' && board[i][j + 1] == '#') {
            isCorner = true;
        }

        return isCorner;
    }


    private static List<int[]> checkFourDirections(int row, int col, char[][] board) {
        List<int[]> wallDirections = new ArrayList<>();

        int rows = board.length;
        int cols = board[0].length;

        //up
        if (row - 1 >= 0 && board[row - 1][col] == '#') {
            wallDirections.add(new int[]{1});
        }

        //down
        if (row + 1 < rows && board[row + 1][col] == '#') {
            wallDirections.add(new int[]{1});
        }

        //left
        if (col - 1 >= 0 && board[row][col - 1] == '#') {
            wallDirections.add(new int[]{0});
        }

        //right
        if (col + 1 < cols && board[row][col + 1] == '#') {
            wallDirections.add(new int[]{0});
        }

        return wallDirections;
    }

    private static boolean noMoneyOrBox(char[][] grid) {
        for (char[] chars : grid) {
            for (char aChar : chars) {
                if (aChar == '0' || aChar == '$') {
                    return false;
                }
            }
        }
        return true;
    }

    private static int[] findPlayer(char[][] grid) {
        for (int r = 0; r < grid.length; r++)
            for (int c = 0; c < grid[0].length; c++) {
                if (grid[r][c] == '1' || grid[r][c] == '+') {
                    return new int[]{r, c};
                }
            }
        return new int[]{-1, -1};
    }

    private static char[][] copyGrid(char[][] grid) {
        char[][] newGrid = new char[grid.length][grid[0].length];
        for (int i = 0; i < grid.length; i++) {
            newGrid[i] = Arrays.copyOf(grid[i], grid[i].length);
        }
        return newGrid;
    }

    private static void printSolutionPath(Node goal) {
        List<Node> path = new ArrayList<>();
        Node cur = goal;
        while (cur != null) {
            path.add(cur);
            cur = cur.parent;
        }
        Collections.reverse(path);
        int step = 0;
        for (Node n : path) {
            System.out.println("Step " + (step++));
            n.print();
            System.out.println("h=" + n.h);
            System.out.println();
            System.out.println("f=" + n.f);
            System.out.println();
            ;
            System.out.println("----------------------");
        }
    }

    //Δημιουργεί νέο ορθογώνιο grid με περίγραμμα από τοίχους (#).
    //ΔΕΝ ΑΛΛΑΖΕΙ Η ΔΟΜΗ ΤΗΣ ΠΙΣΤΑΣ
    //ΠΑΡΑΔΕΙΓΜΑ : ΠΙΣΤΕΣ 1-5.
    static char[][] makeRectangularWithBorder(char[][] grid) {
        int rows = grid.length;

        //Βρίσκει ποια ειναι η μέγιστη σειρά σε μήκος
        int cols = 0;
        for (char[] row : grid)
            cols = Math.max(cols, row.length);

        //Νέος πίνακας με +2 σε κάθε διάσταση για το περίγραμμα
        char[][] newGrid = new char[rows + 2][cols + 2];

        //Αντιγραφή της πίστας και προσθήκη τοίχων στα όρια
        for (int i = 0; i < rows + 2; i++) {
            for (int j = 0; j < cols + 2; j++) {
                if (i == 0 || j == 0 || i == rows + 1 || j == cols + 1)
                    newGrid[i][j] = '#';                  //εξωτερικό περίγραμμα
                else if (j - 1 < grid[i - 1].length)
                    newGrid[i][j] = grid[i - 1][j - 1];   //αντιγραφή κελιών
                else
                    newGrid[i][j] = '#';                  // συμπλήρωση με τοίχους όπου λείπουν κελιά
            }
        }
        return newGrid;
    }


    private static boolean isGoal(Node current) {
        return current.h == 0;
    }


//----------------------------------------------------------------------
//υπολογισμός ευτρετικής

    private static int heuristic(char[][] grid) {
        List<int[]> boxes = new ArrayList<>();
        List<int[]> goals = new ArrayList<>();

        for (int r = 0; r < grid.length; r++) {
            for (int c = 0; c < grid[0].length; c++) {
                if (grid[r][c] == '0' || grid[r][c] == '*') boxes.add(new int[]{r, c});
                if (grid[r][c] == '$' || grid[r][c] == '*') goals.add(new int[]{r, c});
            }
        }

        int totalDist = 0;

        for (int[] box : boxes) {
            int minDist = Integer.MAX_VALUE;
            for (int[] goal : goals) {
                int dist = Math.abs(box[0] - goal[0]) + Math.abs(box[1] - goal[1]); //manhattan h1
                if (dist < minDist) minDist = dist;
            }
            totalDist += minDist;
        }
        int playerDist = IDSPlayertobox(grid);
        totalDist += playerDist;    //IDS h2

        return totalDist;
    }

    //Movement directions: up, right, down, left
    static int[] dRow = {-1, 0, 1, 0};
    static int[] dCol = {0, 1, 0, -1};


    static boolean isValid(char[][] level, boolean[][] visited, int row, int col) {
        return row >= 0 && col >= 0 &&
                row < level.length && col < level[0].length &&
                level[row][col] != '#' &&
                !visited[row][col];
    }

    //IDS
    public static int IDSPlayertobox(char[][] level) {
        int rows = level.length;
        int cols = level[0].length;

        int[] start = findPlayer(level);

        int maxDepth = rows * cols;

        for (int depth = 0; depth <= maxDepth; depth++) {
            boolean[][] visited = new boolean[rows][cols];
            if (DLS(level, start[0], start[1], depth, visited))
                return depth;
        }
        return 0;
    }

    //Depth Limited Search
    private static boolean DLS(char[][] level, int row, int col, int limit, boolean[][] visited) {
        if (limit < 0) return false;
        if (level[row][col] == '0') return true;

        visited[row][col] = true;

        if (limit == 0) return false;

        for (int i = 0; i < 4; i++) {
            int newRow = row + dRow[i];
            int newCol = col + dCol[i];
            if (isValid(level, visited, newRow, newCol)) {
                if (DLS(level, newRow, newCol, limit - 1, visited))
                    return true;
            }
        }
        return false;
    }
}