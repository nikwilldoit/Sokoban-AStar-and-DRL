import java.util.*;

public class Node {
    char[][] grid;
    int playerRow, playerCol;
    Node parent;
    int h;
    int g;
    int f;

    Node(char[][] grid, int r, int c, Node p, int g, int h){
        this.grid = grid;
        this.playerRow = r;
        this.playerCol = c;
        this.parent = p;
        this.g = g;
        this.h = h;
        this.f = g + h;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Node)) return false;
        Node n = (Node) o;
        return playerRow == n.playerRow &&
                playerCol == n.playerCol &&
                Arrays.deepEquals(grid, n.grid);
    }

    @Override
    public int hashCode() {
        int result = Objects.hash(playerRow, playerCol);
        result = 31 * result + Arrays.deepHashCode(grid);
        return result;
    }


    void print(){
        for(char[] row : grid){
            System.out.println(new String(row));
        }
    }
}